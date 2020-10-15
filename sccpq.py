import os
import sys
import json
import click
import sqlite3
import logging
import sccpdb
from common import config, pretty_table, error_exit
from rpmtools import RPM


db = f"{config['DEFAULT']['data_dir']}/{config['SCCP']['db_name']}"


@click.group()
def app():
    """Queries against a cached database of the SCC packages API."""
    pass


@click.command()
@click.option("--ascii/--csv", default=True)
def base(ascii):
    """List base products."""
    products = None
    conn = sqlite3.connect(db)
    with conn:
        cur = conn.cursor()
        cur.execute(sccpdb.list_base_products)
        products = cur.fetchall()
        cur.close()
    conn.close()
    if not products:
        error_exit("No base products found, suggest an sccpsync.")
    output = pretty_table(
        products,
        colnames=["id", "product", "type", "arch", "description"],
        fmt="ascii" if ascii else "csv",
    )
    print("\n".join(output))


@click.command()
@click.option("--base", is_flag=False, default="*", help="list only products associated with this base.")
@click.option("--ascii/--csv", default=True)
def products(base, ascii):
    """List products associated with specified base."""
    products = None
    conn = sqlite3.connect(db)
    with conn:
        cur = conn.cursor()
        if base == "*":
            cur.execute(sccpdb.list_all_products)
        else:
            cur.execute(sccpdb.list_products_by_base, {"base_product": base})
        products = cur.fetchall()
        cur.close()
    conn.close()
    if not products:
        error_exit("No base products found, suggest an sccpsync.")
    output = pretty_table(
        products,
        colnames=["id", "product", "type", "arch", "description"],
        fmt="ascii" if ascii else "csv",
    )
    print("\n".join(output))


@click.command()
@click.argument("package")
@click.option("--base", is_flag=False, default="*", help="search within base and related modules.")
@click.option("--product", is_flag=False, default="*", help="search only within product.")
@click.option("--ascii/--csv", default=True)
def identify(package, product, base, ascii):
    """List products that include specified package."""
    rpm = RPM.from_name(package)
    if not rpm:
        error_exit(f"{package} does not appear to be in valid <name>-<version>-<release>.<arch>[.rpm]")
    products = None
    conn = sqlite3.connect(db)
    query_values = rpm.to_dict()
    query_values["base_product"] = base
    query_values["product"] = product
    with conn:
        cur = conn.cursor()
        if product == "*" and base == "*":
            cur.execute(sccpdb.search_products_by_rpm, query_values)
        elif base != "*":
            cur.execute(sccpdb.create_product_family_temp_table, query_values)
            cur.execute(sccpdb.search_product_family_by_rpm, query_values)
        else:
            cur.execute(sccpdb.search_product_by_rpm, query_values)
        products = cur.fetchall()
        cur.close()
    conn.close()
    output = pretty_table(
        products,
        colnames=["id", "product", "type", "arch", "description"],
        fmt="ascii" if ascii else "csv",
    )
    print("\n".join(output))


@click.command()
@click.argument("name")
@click.option("--product", is_flag=False, default="*", help="limit to product.")
def search(product, name):
    """List the versions of a package by name."""
    conn = sqlite3.connect(db)
    packages = []
    with conn:
        cur = conn.cursor()
        if product == "*":
            cur.execute(sccpdb.search_for_all_versions, {"name": name})
        else:
            cur.execute(sccpdb.search_product_for_all_versions, {"name": name, "product": product})
        packages = cur.fetchall()
        cur.close()
    conn.close()
    rpmlist = []
    for rpm in packages:
        rpmlist.append(RPM(rpm[0], rpm[1], rpm[2], rpm[3]))
    rpmlist.sort(reverse=True)
    print("\n".join(map(str, rpmlist)))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    if not sccpdb.checkdb(db):
        error_exit("Please initialise SCCP database with sccpsync.py.")
    app.add_command(identify, "id")
    app.add_command(base, "base")
    app.add_command(products, "products")
    app.add_command(search, "search")
    app()
