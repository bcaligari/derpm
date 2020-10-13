import sqlite3
from common import config, main_dead_end

db_file = f"{config['DEFAULT']['data_dir']}/{config['SCCP']['db_name']}"

drop_products = "DROP TABLE IF EXISTS products"

drop_packages = "DROP TABLE IF EXISTS packages"

drop_base2products = "DROP TABLE IF EXISTS base2products"

drop_package2products = "DROP TABLE IF EXISTS package2products"


create_products = """
    CREATE TABLE IF NOT EXISTS products (
        id              INTEGER PRIMARY KEY,
        name            TEXT,
        identifier      TEXT,
        type            TEXT,
        free            INTEGER,
        edition         TEXT,
        architecture    TEXT
    )
"""


insert_products = """
    INSERT OR IGNORE INTO products (id, name, identifier, type, free, edition, architecture)
    VALUES (?, ?, ?, ?, ?, ?, ?)
"""


list_base_products = """
    SELECT id, identifier, type, name FROM products WHERE type = 'base' ORDER BY id
"""


get_base_product_id_by_identifier = """
    SELECT id, identifier, type FROM products WHERE type = 'base' AND identifier = :identifier
"""


list_all_products = """
    SELECT id, identifier, type, architecture, name FROM products ORDER BY id
"""


create_packages = """
    CREATE TABLE IF NOT EXISTS packages (
        id              INTEGER PRIMARY KEY,
        name            TEXT,
        arch            TEXT,
        version         TEXT,
        release         TEXT
    )
"""
insert_packages = """
    INSERT OR IGNORE INTO packages (id, name, arch, version, release)
    VALUES (?, ?, ?, ?, ?)
"""


create_base2products = """
    CREATE TABLE IF NOT EXISTS base2products (
        base            INTEGER NOT NULL,
        product         INTEGER NOT NULL,
        UNIQUE (base, product)
    )
"""


insert_base2products = """
    INSERT OR IGNORE INTO base2products (base, product)
    VALUES (?, ?)
"""


list_products_by_base = """
    SELECT base.id, base.identifier, base.architecture, prod.id, prod.architecture, prod.identifier, prod.type, prod.name, base2products.base, base2products.product
    FROM ((base2products
    INNER JOIN products base ON base.id = base2products.base)
    INNER JOIN products prod ON prod.id = base2products.product)
    WHERE base.identifier = :base_product
    ORDER BY prod.id
"""


create_package2products = """
    CREATE TABLE IF NOT EXISTS package2products (
        package         INTEGER NOT NULL,
        product         INTEGER NOT NULL,
        UNIQUE (package, product)
    )
"""


insert_package2products = """
    INSERT OR IGNORE INTO package2products (package, product)
    VALUES (?, ?)
"""


search_products_by_rpm = """
    SELECT products.id, products.identifier, products.type, products.name
        FROM ((packages
        INNER JOIN package2products ON packages.id = package2products.package)
        INNER JOIN products ON products.id = package2products.product)
        WHERE packages.name = :name
            AND packages.version = :version
            AND packages.release = :release
            AND packages.arch = :arch
"""


create_product_family_temp_table = """
    CREATE TEMP TABLE prod_family AS
    SELECT pf_id, pf_identifier, pf_type, pf_name FROM (
        SELECT base.id, base.identifier, prod.id as pf_id, prod.identifier as pf_identifier, prod.type as pf_type, prod.name as pf_name, base2products.base, base2products.product
        FROM ((base2products
        INNER JOIN products base ON base.id = base2products.base)
        INNER JOIN products prod ON prod.id = base2products.product)
        WHERE base.identifier = :base_identifier
        ORDER BY prod.id)
"""


search_product_family_for_rpm = """
    SELECT temp.prod_family.pf_id, temp.prod_family.pf_identifier, temp.prod_family.pf_type, temp.prod_family.pf_name
        FROM ((packages
        INNER JOIN package2products ON packages.id = package2products.package)
        INNER JOIN temp.prod_family ON temp.prod_family.pf_id = package2products.product)
        WHERE packages.name = :name
            AND packages.version = :version
            AND packages.release = :release
            AND packages.arch = :arch
"""


search_family_for_all_versions = """
    SELECT packages.id, packages.name, packages.version, packages.release, packages.arch,
            package2products.package, package2products.product,
            temp.prod_family.pf_id, temp.prod_family.pf_identifier, temp.prod_family.pf_type, temp.prod_family.pf_name
        FROM ((packages
        INNER JOIN package2products ON packages.id = package2products.package)
        INNER JOIN temp.prod_family ON temp.prod_family.pf_id = package2products.product)
        WHERE packages.name = :name
            AND packages.arch = :arch
"""


search_for_all_versions = """
    SELECT packages.id, packages.name, packages.version, packages.release, packages.arch
        FROM packages
        WHERE packages.name = :name
            AND packages.arch = :arch
"""


def checkdb(db):
    """Trivial check to see if the database exists and is populated"""
    rows = 0
    try:
        conn = sqlite3.connect(db)
    except sqlite3.Error:
        return False
    try:
        rows = conn.execute("SELECT COUNT(*) FROM base2products")
    except sqlite3.Error:
        conn.close()
        return False
    if rows == 0:
        return False
    conn.close()
    return True


if __name__ == "__main__":
    main_dead_end(__file__)
