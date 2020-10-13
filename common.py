import os
import re
import sys
import logging
import configparser


config = configparser.ConfigParser()
_config_paths = ["norbury.ini", "~/.norburyrc"]
_config_paths = map(os.path.expanduser, _config_paths)
config.read(_config_paths)
config["DEFAULT"]["data_dir"] = os.path.expanduser(config["DEFAULT"]["data_dir"])
try:
    os.mkdir(config["DEFAULT"]["data_dir"])
except FileExistsError:
    pass


def error_exit(msg, exit_code=1):
    """Print msg and exit with exit_code."""
    print(msg, file=sys.stderr)
    sys.exit(exit_code)


def main_dead_end(name):
    """Little reminder that you shouldn't be calling name in vain."""
    error_exit(f"{name} is not meant to be called directly.")


def pretty_table(table, fmt="csv", colnames=None):
    """Dumps a table as csv or ascii."""
    # convert itertor to a list of lists of strings
    all_rows = [[*map(str, row)] for row in table]
    # check the right number of optional column names were passed
    if colnames and table:
        if len(colnames) != len(all_rows[0]):
            raise IndexError
    out = []
    if fmt == "csv":
        if colnames:
            out.append(",".join(colnames))
        for row in all_rows:
            out.append(",".join(row))
        return out
    if fmt == "ascii":
        if not table and not colnames:
            return out
        # work out the width for each column
        ncol = len(colnames) if colnames else len(all_rows[0])
        col_max = [0 for _ in range(ncol)]
        for row in all_rows:
            for col in range(ncol):
                col_max[col] = max(col_max[col], len(row[col]))
        if colnames:
            for col in range(ncol):
                col_max[col] = max(col_max[col], len(colnames[col]))
        # print out each line justified and separated
        if colnames:
            ruling = ["" for _ in range(ncol)]
            justified_header = map(lambda x: x[0].ljust(x[1]), zip(colnames, col_max))
            justified_ruling = map(lambda x: x[0].ljust(x[1], "-"), zip(ruling, col_max))
            out.append(" | ".join(justified_header).rstrip())
            out.append(" | ".join(justified_ruling).rstrip())
        for row in all_rows:
            justified_row = map(lambda x: x[0].ljust(x[1]), zip(row, col_max))
            out.append(" | ".join(justified_row).rstrip())
        return out
    # unimplemented format
    return out


def read_rpm_list(filename):
    """
    Read a list of rpms from a text file.

    Tries to properly handle:
    - plain `rpm -qa` output
    - `rpm.txt` from supportconfig tarball (uses the `rpm -qa --last` section)
    """
    rpm_list = []
    with open(filename) as f:
        all_lines = f.readlines()
    if all_lines[0].startswith("#==[ Command ]===="):
        logging.debug(f"Identified {filename} as an rpm.txt from a supportconfig.")
        in_rpmqa_last = False
        for line in all_lines:
            if not in_rpmqa_last:
                in_rpmqa_last = line.startswith("# /bin/rpm -qa --last")
                continue
            if line.startswith("#"):
                break
            if not line.strip():
                break
            if m := re.match(r"^(.+?)\s", line):
                rpm_list.append(m[1])
        return rpm_list
    else:
        logging.debug(f"Assuming {filename} is just an ordinary list of rpms.")
        for line in all_lines:
            if _line := line.strip():
                rpm_list.append(_line)
    return rpm_list


if __name__ == "__main__":
    main_dead_end(__file__)
