# Implementation notes

## Layout

* `common.py` - Configuration and functions used by other modules.
* `rpmtools.py` - Implements RPM representation classes.
* `sccpdb.py` - SCC package database SQL and general functions.
* `rpmdiff.py` - Report on the RPM version differences between two lists of RPMs.
* `sccpsync.py` - Cache the SCC Packages API to local sqlite3 database.
* `slebase.py` - Verify a list of rpms against a specific SLE base.
* `sccpq.py` - Query the local SCC packages API database.

## Known issues

## TODO

* Make it easier to call the scripts.
* Better handle some frequent error conditions.
