import click
import sqlite3
import sccpdb
from common import config, read_rpm_list, error_exit
from rpmtools import RPM


def prodsort(prods, base):
    """dedup a product list and put the base first"""
    # We need to dedup as some packages may appear more than once
    # in the same product.  This is a feature not a bug.
    p = set(prods)
    if base in prods:
        return [base, *(p - {base})]
    else:
        return [*p]


@click.command()
@click.argument("base")
@click.argument("rpmlist")
def main(base, rpmlist):
    """
    Identify product(s) associated with a base containing an RPM.

    \b
    Legend:
      ? Doesn't appear to be "<name>-<version>-<release>.<arch>[.rpm]".
      - Not found in base product.
      = Found in repo of base product.
      + From a module or extension that can be enabled on base.
    """
    db = f"{config['DEFAULT']['data_dir']}/{config['SCCP']['db_name']}"
    if not sccpdb.checkdb(db):
        error_exit("Please initialise SCCP database with sccpsync.py.")
    conn = sqlite3.connect(db)
    with conn:
        cur = conn.cursor()
        try:
            rpm_list = read_rpm_list(rpmlist)
        except FileNotFoundError:
            error_exit(f"{rpmlist} does not appear to exit.")
        cur.execute(sccpdb.create_product_family_temp_table, {"base_identifier": base})
        for line in rpm_list:
            rpm = RPM.from_name(line)
            prods = []
            if not rpm:
                key = "?"
            else:
                cur.execute(sccpdb.search_family_for_rpm, rpm.to_dict())
                prods = [p[8] for p in cur.fetchall()]
                if prods:
                    if base in prods:
                        key = "="
                    else:
                        key = "+"
                else:
                    key = "-"
            print(f"{key} {rpm}")
            for prod in prodsort(prods, base):
                print(f"    {str(prod)}")
            print()
        cur.close()
    conn.close()


if __name__ == "__main__":
    main(None, None)
