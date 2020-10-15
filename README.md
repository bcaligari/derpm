# derpm

A collection of tools to help with some of the frustrations trying to find where
an RPM came from and working through lists of RPMs.  Mostly relevant for the SLES
world for versions 12+.

* `sccpsync` - Caching the SCC packages API to a local sqlite3.
* `sccpq` - Querying the SCC package API via the local sqlite3 cached copy.
* `slebase` - Establishing the provenance of RPMs from the `rpm -qa` output on
   a SLE server.
* `rpmdiff` - Comparing the version differences between two lists of RPMs.

These scripts are written in Python 3.8 for my own entertainment and use.  They
are inspired by, but in no other way related, to my day job.

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

## `sccpq`

Query the local cache of the SCC package API.

### `sccpq base`

```{text}
Usage: sccpq.py base [OPTIONS]

  List base products.

Options:
  --ascii / --csv
  --help           Show this message and exit.
```

The `base` product is what should be soft linked in `/etc/products.d/baseproduct`.
The other products should be `modules` or `extensions`.

### `sccpq products`

```{text}
Usage: sccpq.py products [OPTIONS]

  List products associated with specified base.

Options:
  --base TEXT      list only products associated with this base.
  --ascii / --csv
  --help           Show this message and exit.
```

The same `module` or `extension` may be associated with more than one `base`.

### `sccpq id`

```{text}
Usage: sccpq.py id [OPTIONS] PACKAGE

  List products that include specified package.

Options:
  --base TEXT      search within base and related modules.
  --product TEXT   search only within product.
  --ascii / --csv
  --help           Show this message and exit.
```

### `sccpq search`

Search for a package by name regardless of architecture.  Search can be limited
to a single product (base, module, or extension).

```{text}
Usage: sccpq.py search [OPTIONS] NAME

  List the versions of a package by name.

Options:
  --product TEXT  limit to product.
  --help          Show this message and exit.
```
