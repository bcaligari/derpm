# Example Usage

## Housekeeping

### Configuration

#### Create a custom configuration file

The default configuration file is `norbury.ini` in working directory.

```{text}
cp norbury.ini ~/.norburyrc
```

### Synchronising against the SCC package API

#### Populate the SCC Package DB with x86_64 products

```{text}
python sccpsync.py --refresh
```

#### Populate the SCC Package dB with all products

```{text}
python sccpsync.py --refresh --anyarch
```

### Cleaning up

#### Removing cached API requests and SCC Package DB

```{text}
python sccpsync.py --cleanup
```

## Querying the (locally cached) SCC Package API

### Base, modules, and extensions

#### List all base products

These should correspond to what the `/etc/products.d/baseproduct` softlinks to.

```{text}
python sccpq.py base
```

#### List all products

```{text}
python sccpq.py products
```

#### List all products associated with a base

A `module` or `extension` can be associated with more than one `base`.

```{text}
python sccpq.py products --base SLES_SAP/12.4/x86_64
```

### RPM provenance

#### Find all products that include an RPM

```{text}
python sccpq.py id kernel-default-4.4.180-94.130.1.x86_64
```

#### Find all products related to a base that include an RPM

```{text}
python sccpq.py id kernel-default-4.4.180-94.130.1.x86_64 --base SLES_SAP/12.3/x86_64
```

#### Search for an RPM within a specific product

```{text}
python sccpq.py id kernel-default-4.4.180-94.130.1.x86_64 --product SLES_SAP/12.3/x86_64
```

### Available versions of a package

#### Search for all versions and architecture of an RPM by name

```{text}
python sccpq.py search kernel-default
```

#### Search for an RPM by name in a given product

```{text}
python sccpq.py search kernel-default --product SLES_SAP/12.5/x86_64
```

## Working with lists of RPMs

### Checking provenance of packages against a SLE product

#### List packages not found in a product or its associated modules

```{text}
python slebase.py SLES_SAP/12.3/x86_64 rpm.txt | grep '^-'`
```

#### List packages which need an additional module activated

```{text}
python slebase.py SLES_SAP/12.3/x86_64 rpm.txt | sed -ne '/^+/,/^$/p'`
```

### Differences between two lists of RPMs

#### Do a diff between two `rpm -qa` outputs

```{text}
python rpmdiff.py rpmqa.zypper-dup.txt rpmqa.fully-updated.txt
```
