import click
import sys
import json
import requests
import base64
import os
import pathlib
import binascii
import logging
import sqlite3
import sccpdb
from common import config


def cache_cleanup(cachedir):
    """Cleans a directory from filenames that correctly un-base64"""
    d = pathlib.Path(cachedir)
    for f in d.iterdir():
        if f.is_file() and not f.is_symlink():
            s = None
            try:
                s = base64.b64decode(str(f.parts[-1]))
            except binascii.Error:
                logging.debug(f"Not a base64: {str(f.parts[-1])}")
            if s:
                logging.debug(f"Unlinking {str(f)}")
                f.unlink()


def sccp_cleanup(db, cachedir):
    try:
        os.unlink(db)
    except FileNotFoundError:
        pass
    cache_cleanup(cachedir)


def get_json_from_url(url, headers={}, cachedir=None, retries=2):
    """
    Downloads a url and optionally caches the results.

    If 'cachedir' is not None then the url is cached locally
    and not retrieved again.
    """
    json_data = None
    base64url = bytes.decode(base64.b64encode(str.encode(url)))
    logging.debug(f"url: {url}")
    if cachedir:
        logging.debug(f"cache-filename: {cachedir}/{base64url}")
        try:
            os.mkdir(cachedir)
        except FileExistsError:
            pass
        try:
            with open(f"{cachedir}/{base64url}") as f:
                json_data = json.load(f)
                logging.debug(f"retrieving from cache")
        except FileNotFoundError:
            pass
    if not json_data:
        logging.debug(f"downloading from source")
        while not json_data and retries >= 0:
            if retries < 2:
                logging.info(f"retrying download")
            with requests.Session() as s:
                retries -= 1
                r = s.get(url, headers=headers)
                if r:
                    json_data = r.json()
        if cachedir:
            with open(f"{cachedir}/{base64url}", "w") as f:
                json.dump(json_data, f, indent=4)
    return json_data


def initdb(db, baseurl, accept, anyarch=False, cachedir=None):
    """
    Initialise products and packages data from the SCC API.

    If not anyarch then only x86_64 products are synced.

    If cachedir not None then API responses are cached.
    """
    fault = False
    product_json = get_json_from_url(f"{baseurl}/products", {"Accept": accept}, cachedir)
    conn = sqlite3.connect(db)
    conn.execute(sccpdb.drop_products)
    conn.execute(sccpdb.drop_packages)
    conn.execute(sccpdb.drop_base2products)
    conn.execute(sccpdb.drop_package2products)
    conn.execute(sccpdb.create_products)
    conn.execute(sccpdb.create_packages)
    conn.execute(sccpdb.create_base2products)
    conn.execute(sccpdb.create_package2products)
    conn.commit()
    with conn:
        for base_product in product_json["data"]:
            if not anyarch and base_product["architecture"] != "x86_64":
                continue
            conn.execute(
                sccpdb.insert_products,
                (
                    base_product["id"],
                    base_product["name"],
                    base_product["identifier"],
                    base_product["type"],
                    1 if base_product["free"] else 0,
                    base_product["edition"],
                    base_product["architecture"],
                ),
            )
            print(f"Importing package data for {base_product['identifier']}")
            package_json = get_json_from_url(
                f"{baseurl}/packages?product_id={base_product['id']}",
                {"Accept": accept},
                cachedir,
            )
            if package_json:
                for package in package_json["data"]:
                    conn.execute(
                        sccpdb.insert_packages,
                        (
                            package["id"],
                            package["name"],
                            package["arch"],
                            package["version"],
                            package["release"],
                        ),
                    )
                    for product in package["products"]:
                        conn.execute(
                            sccpdb.insert_base2products,
                            (base_product["id"], product["id"]),
                        )
                        conn.execute(
                            sccpdb.insert_package2products,
                            (package["id"], product["id"]),
                        )
                        conn.execute(
                            sccpdb.insert_products,
                            (
                                product["id"],
                                product["name"],
                                product["identifier"],
                                product["type"],
                                1 if product["free"] else 0,
                                product["edition"],
                                product["architecture"],
                            ),
                        )
            else:
                print("Empty dataset received, re-run database init.")
                logging.warning("Empty dataset received, re-run database init.")
                fault = True
    conn.commit()
    conn.close()
    if fault:
        sys.exit(1)
    else:
        sys.exit(0)


@click.command()
@click.option("--cleanup", is_flag=True, help="Remove database and cached downloads.")
@click.option("--refresh", is_flag=True, help="Refresh package data from SCC.")
@click.option("--nocache", is_flag=True, help="Do not cache API responses.")
@click.option(
    "--anyarch",
    is_flag=True,
    help="Import package data for all architectures, not just x86_64.",
)
def main(cleanup, refresh, nocache, anyarch):
    """Synchronise SCC package data to local sqlite3 database."""
    db_file = sccpdb.db_file
    cache_dir = f"{config['DEFAULT']['data_dir']}/{config['SCCP']['cache_subdir']}"
    baseurl = config["SCCP"]["api_base"]
    accept = config["SCCP"]["accept"]
    if cleanup or refresh:
        sccp_cleanup(db_file, cache_dir)
    if cleanup and not refresh:
        sys.exit(0)
    initdb(db_file, baseurl, accept, anyarch, None if nocache else cache_dir)
    return 0


if __name__ == "__main__":
    main(None, None, None, None)
