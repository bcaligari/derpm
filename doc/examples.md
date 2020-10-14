# Example Usage

## Querying the SLE

### Base, modules, and extensions

### RPM provenance

### Available versions of a package

## Working with lists of RPMs

### Checking provenance of packages against a SLE product

#### List packages not found in a product or its associated modules

```{text}
python slebase.py SLES_SAP/12.3/x86_64 rpm.txt | grep '^-'`
```

#### List packages which need an additional module activated.

```{text}
python slebase.py SLES_SAP/12.3/x86_64 rpm.txt | sed -ne '/^+/,/^$/p'`
```
