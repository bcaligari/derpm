# derpm

A collection of tools to help with:

* `sccpsync` - Caching the SCC packages API to a local sqlite3.
* `sccpq` - Querying the SCC package API via the local sqlite3 cached copy.
* `slebase` - Establishing the provenance of RPMs from the `rpm -qa` output on
   a SLE server.
* `rpmdiff` - Comparing the version differences between two lists of RPMs.

These scripts are written in Python 3.8 for my own entertainment and use.  They
are inspired by but in no other way related to my day job.

## `rpmdiff`

Report on the RPM version differences between two lists of RPMs.

```{text}
Usage: rpmdiff.py [OPTIONS] FILE0 FILE1
```

The files can be:

* Plain output of `rpm -qa`.
* The `rpm.txt` from a `supportconfig` archive.

Matching packages are listed side by side with the first column indicating
the relationship between the version from both lists:

```{text}
    ++   present in first but not second
    --   present in second but not first
    ==   present in both at same revision
    <<   version in first lower than one in second
    >>   version in first higher than one in second
    :+   multiversion install present in first but not second
    :-   multiversion install present in second but not first
    :=   multiversion install present in both
```

## `sccpsync`

Synchronise SCC package data to local sqlite3 database.

```{text}
Usage: sccp-sync.py [OPTIONS]

Options:
  --cleanup  Remove database and cached downloads.
  --refresh  Refresh package data from SCC.
  --nocache  Do not cache API responses.
  --anyarch  Import package data for all architectures, not just x86_64.
  --help     Show this message and exit.
```

## `slebase`

Identify product(s) associated with a base containing an RPM.

This is most useful to identify:

* Packages that were not included with a particular SLE product (e.g. `SLES_SAP/12.3/x86_64`).
* Packages that belong to a module and extension rather than the base product.

The output is formatted so that it can be easily `grep`ed.

```{text}
Usage: slebase.py [OPTIONS] BASE RPMLIST

  Legend:
    ? Doesn't appear to be "<name>-<version>-<release>.<arch>[.rpm]".
    - Not found in base product.
    = Found in repo of base product.
    + From a module or extension that can be enabled on base.
```

Which packages could not be found in this product:

```{text}
$ python slebase.py SLES_SAP/12.3/x86_64 rpm.txt | grep '^-'`
```

List packages which need an additional module activated:

```{text}
$ python slebase.py SLES_SAP/12.3/x86_64 rpm.txt | sed -ne '/^+/,/^$/p'`
```

## Implementation

### Known issues

### TODO

* Make it easier to call the scripts.
* Put some better error handling rather than cascade to Python exceptions.

### Files

* `common.py` - Configuration and functions used by other modules.
* `rpmtools.py` - Implements RPM representation classes.
* `sccpdb.py` - SCC package database SQL and general functions.
* `rpmdiff.py` - Report on the RPM version differences between two lists of RPMs.
* `sccpsync.py` - Cache the SCC Packages API to local sqlite3 database.
* `slebase.py` - Verify a list of rpms against a specific SLE base.
* `sccpq.py` - Query the local SCC packages API database.
