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
@click.argument("package")
@click.option("--base", is_flag=False, default="*", help="search within base and modules.")
@click.option("--ascii/--csv", default=True)
def identify(package, base, ascii):
    """List products that include specified package."""
    rpm = RPM.from_name(package)
    if not rpm:
        error_exit(f"{package} does not appear to be in valid <name>-<version>-<release>.<arch>[.rpm]")
    products = None
    conn = sqlite3.connect(db)
    with conn:
        cur = conn.cursor()
        if base == "*":
            cur.execute(sccpdb.search_products_by_rpm, rpm.to_dict())
        else:
            cur.execute(sccpdb.create_product_family_temp_table, {"base_identifier": base})
            cur.execute(sccpdb.search_product_family_for_rpm, rpm.to_dict())
        products = cur.fetchall()
        cur.close()
    conn.close()
    output = pretty_table(
        products,
        colnames=["id", "product", "type", "description"],
        fmt="ascii" if ascii else "csv",
    )
    print("\n".join(output))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    if not sccpdb.checkdb(db):
        error_exit("Please initialise SCCP database with sccpsync.py.")
    app.add_command(identify, "id")
    # app.add_command(products, "products")
    # app.add_command(search, "search")
    app()
