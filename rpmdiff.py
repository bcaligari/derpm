import click
from rpmtools import RPMlist
from common import pretty_table, read_rpm_list, error_exit
from pathlib import Path


def all_rpm_names(a, b):
    """Sorted list of all package names from two RPMlists."""
    return sorted(list(set(a._rpms.keys()) | set(b._rpms.keys())), key=str.casefold)


def all_rpm_archs(a, b, name):
    """Sorted list of all architectures from two RPMs."""
    return sorted(list(set(a.get_archs(name)) | set(b.get_archs(name))))


def diff_report(a, b):
    """Compare against another list of RPMs and generate a report"""
    # Build a sorted list of the package names in both lists
    results = []
    for name in all_rpm_names(a, b):
        for arch in all_rpm_archs(a, b, name):
            code = "??"
            a_vers = a.get_versions(name, arch)
            b_vers = b.get_versions(name, arch)
            if max(len(a_vers), len(b_vers)) == 1:
                # single occurrence of RPM
                a_str = f"{a_vers[0][0]}-{a_vers[0][1]}" if len(a_vers) else ""
                b_str = f"{b_vers[0][0]}-{b_vers[0][1]}" if len(b_vers) else ""
                if len(a_vers) == 1 and len(b_vers) == 0:
                    code = "++"
                elif len(a_vers) == 0 and len(b_vers) == 1:
                    code = "--"
                else:
                    if a_vers == b_vers:
                        code = "=="
                    elif a_vers < b_vers:
                        code = "<<"
                    else:
                        code = ">>"
                results.append([code, name, arch, a_str, b_str])
            else:
                # multiversion RPM territory (e.g. kernel)
                all_vers = sorted(list(set(a_vers) | set(b_vers)))
                for ver in all_vers:
                    (a_str, b_str) = ("", "")
                    ver_str = f"{ver[0]}-{ver[1]}"
                    if ver in set(a_vers) and ver in set(b_vers):
                        (a_str, b_str) = (ver_str, ver_str)
                        code = ":="
                    elif ver in set(a_vers):
                        a_str = ver_str
                        code = ":+"
                    else:
                        b_str = ver_str
                        code = ":-"
                    results.append([code, name, arch, a_str, b_str])
    return results


@click.command()
@click.argument("file0")
@click.argument("file1")
def main(file0, file1):
    """
    Version diff between two lists of RPMs.

    \b
    Legend:
      ++   present in first but not second
      --   present in second but not first
      ==   present in both at same revision
      <<   version in first lower than one in second
      >>   version in first higher than one in second
      :+   multiversion install present in first but not second
      :-   multiversion install present in second but not first
      :=   multiversion install present in both
    """
    rpm_lists = dict()
    for file_name in (file0, file1):
        try:
            rpm_lists[file_name] = RPMlist.from_name_list(read_rpm_list(file_name))
        except FileNotFoundError:
            error_exit(f"{file_name} does not appear to exist.")
    report = diff_report(rpm_lists[file0], rpm_lists[file1])
    print(
        "\n".join(
            pretty_table(
                report,
                colnames=["", "package", "arch", Path(file0).name, Path(file1).name],
                fmt="ascii",
            )
        )
    )
    return 0


if __name__ == "__main__":
    main(None, None)
