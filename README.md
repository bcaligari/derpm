# derpm

A collection of tools to help with:

* Querying the SCC package API.
* Establishing the provenance of RPMs from the `rpm -qa` output on a SLE server.
* Comparing the version differences between two lists of RPMs.

These scripts are written in Python 3.8 for my own entertainment and use.  They
are inspired by but in no other way related to my day job.

## rpmdiff

Report on the RPM version differences between two lists of RPMs.

### Usage

```{text}
Usage: rpmdiff.py [OPTIONS] FILE0 FILE1
```

The files can be:

* Plain output of `rpm -qa`.
* The `rpm.txt` from a `supportconfig` archive.

### Results

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

## sccp-sync

Synchronise SCC package data to local sqlite3 database.

### Usage

```{text}
Usage: sccp-sync.py [OPTIONS]

Options:
  --cleanup  Remove database and cached downloads.
  --refresh  Refresh package data from SCC.
  --nocache  Do not cache API responses.
  --anyarch  Import package data for all architectures, not just x86_64.
  --help     Show this message and exit.
```

## Implementation

### Files

* `common.py` - Configuration and functions used by other modules.
* `rpmtools.py` - Implements RPM representation classes.
* `sccpdb.py` - SCC package database SQL and general functions.
* `rpmdiff.py` - Report on the RPM version differences between two lists of RPMs.
* `sccpsync.py` - Cache the SCC Packages API to local sqlite3 database.
* `slebase.py` - Verify a list of rpms against a specific SLE base.
* `sccpq.py` - Query the local SCC packages API database.
