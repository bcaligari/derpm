import random
from rpmtools import VerTuple, RPM, RPMlist

version_tuple_strings = ["0.5.1", "0.7.3+150+suse.529bc38"]

version_tuple_pairs_eq = [
    ("0.5.0", "0.5.0"),
    ("0.a.1", "0.a.1"),
    ("b.0.17", "b.0.17"),
]

version_tuple_pairs_lt = [
    ("0.5.0", "1.5.0"),
    ("0.5.0", "0.10.0"),
    ("0.5", "0.5.1"),
    ("0.5.1", "0.5.a"),
]

rpm_list_sorted = [
    "bc-1.06.95-6.56.x86_64",
    "cifs-utils-6.9-9.6.1.x86_64",
    "gdk-pixbuf-loader-rsvg-2.40.20-5.6.1.x86_64",
    "kernel-default-3.12.28-4.6.x86_64",
    "kernel-default-3.12.32-33.1.x86_64",
    "kernel-default-3.12.36-38.1.x86_64",
    "kernel-default-3.12.38-44.1.x86_64",
    "kernel-default-3.12.39-47.1.x86_64",
    "kernel-default-3.12.43-52.6.1.x86_64",
    "kernel-default-3.12.44-52.10.1.x86_64",
    "kernel-default-3.12.44-52.18.1.x86_64",
    "kernel-default-3.12.48-52.27.1.x86_64",
    "kernel-default-3.12.49-11.1.x86_64",
    "kernel-default-3.12.51-52.31.1.x86_64",
    "kernel-default-3.12.51-52.34.1.x86_64",
    "kernel-default-3.12.51-52.39.1.x86_64",
    "kernel-default-3.12.51-60.20.2.x86_64",
    "kernel-default-3.12.51-60.25.1.x86_64",
    "kernel-default-3.12.53-60.30.1.x86_64",
    "kernel-default-3.12.55-52.42.1.x86_64",
    "kernel-default-3.12.55-52.45.1.x86_64",
    "kernel-default-3.12.57-60.35.1.x86_64",
    "kernel-default-3.12.59-60.41.2.x86_64",
    "kernel-default-3.12.59-60.45.2.x86_64",
    "kernel-default-3.12.60-52.49.1.x86_64",
    "kernel-default-3.12.60-52.54.2.x86_64",
    "kernel-default-3.12.60-52.57.1.x86_64",
    "kernel-default-3.12.60-52.60.1.x86_64",
    "kernel-default-3.12.60-52.63.1.x86_64",
    "kernel-default-3.12.61-52.66.1.x86_64",
    "kernel-default-3.12.61-52.69.2.x86_64",
    "kernel-default-3.12.61-52.72.1.x86_64",
    "kernel-default-3.12.61-52.77.1.x86_64",
    "kernel-default-3.12.61-52.80.1.x86_64",
    "kernel-default-3.12.61-52.83.1.x86_64",
    "kernel-default-3.12.61-52.86.1.x86_64",
    "kernel-default-3.12.61-52.89.1.x86_64",
    "kernel-default-3.12.61-52.92.1.x86_64",
    "kernel-default-3.12.61-52.101.1.x86_64",
    "kernel-default-3.12.61-52.106.1.x86_64",
    "kernel-default-3.12.61-52.111.1.x86_64",
    "kernel-default-3.12.61-52.119.1.x86_64",
    "kernel-default-3.12.61-52.122.1.x86_64",
    "kernel-default-3.12.61-52.125.1.x86_64",
    "kernel-default-3.12.61-52.128.1.x86_64",
    "kernel-default-3.12.61-52.133.1.x86_64",
    "kernel-default-3.12.61-52.136.1.x86_64",
    "kernel-default-3.12.61-52.141.1.x86_64",
    "kernel-default-3.12.61-52.146.1.x86_64",
    "kernel-default-3.12.61-52.149.1.x86_64",
    "kernel-default-3.12.61-52.154.1.x86_64",
    "kernel-default-3.12.62-60.62.1.x86_64",
    "kernel-default-3.12.62-60.64.8.2.x86_64",
    "kernel-default-3.12.67-60.64.18.1.x86_64",
    "kernel-default-3.12.67-60.64.21.1.x86_64",
    "kernel-default-3.12.67-60.64.24.1.x86_64",
    "kernel-default-3.12.69-60.64.29.1.x86_64",
    "kernel-default-3.12.69-60.64.32.1.x86_64",
    "kernel-default-3.12.69-60.64.35.1.x86_64",
    "kernel-default-3.12.74-60.64.40.1.x86_64",
    "kernel-default-3.12.74-60.64.45.1.x86_64",
    "kernel-default-3.12.74-60.64.48.1.x86_64",
    "kernel-default-3.12.74-60.64.51.1.x86_64",
    "kernel-default-3.12.74-60.64.54.1.x86_64",
    "kernel-default-3.12.74-60.64.57.1.x86_64",
    "kernel-default-3.12.74-60.64.60.1.x86_64",
    "kernel-default-3.12.74-60.64.63.1.x86_64",
    "kernel-default-3.12.74-60.64.66.1.x86_64",
    "kernel-default-3.12.74-60.64.69.1.x86_64",
    "kernel-default-3.12.74-60.64.82.1.x86_64",
    "kernel-default-3.12.74-60.64.85.1.x86_64",
    "kernel-default-3.12.74-60.64.88.1.x86_64",
    "kernel-default-3.12.74-60.64.93.1.x86_64",
    "kernel-default-3.12.74-60.64.96.1.x86_64",
    "kernel-default-3.12.74-60.64.99.1.x86_64",
    "kernel-default-3.12.74-60.64.104.1.x86_64",
    "kernel-default-3.12.74-60.64.107.1.x86_64",
    "kernel-default-3.12.74-60.64.110.1.x86_64",
    "kernel-default-3.12.74-60.64.115.1.x86_64",
    "kernel-default-3.12.74-60.64.118.1.x86_64",
    "kernel-default-3.12.74-60.64.121.1.x86_64",
    "kernel-default-3.12.74-60.64.124.1.x86_64",
    "kernel-default-4.4.21-69.1.x86_64",
    "kernel-default-4.4.21-81.3.x86_64",
    "kernel-default-4.4.21-84.1.x86_64",
    "kernel-default-4.4.21-90.1.x86_64",
    "kernel-default-4.4.38-93.1.x86_64",
    "kernel-default-4.4.49-92.11.1.x86_64",
    "kernel-default-4.4.49-92.14.1.x86_64",
    "kernel-default-4.4.59-92.17.3.x86_64",
    "kernel-default-4.4.59-92.20.2.x86_64",
    "kernel-default-4.4.59-92.24.2.x86_64",
    "kernel-default-4.4.73-5.1.x86_64",
    "kernel-default-4.4.73-7.1.x86_64",
    "kernel-default-4.4.74-92.29.1.x86_64",
    "kernel-default-4.4.74-92.32.1.x86_64",
    "kernel-default-4.4.74-92.35.1.x86_64",
    "kernel-default-4.4.74-92.38.1.x86_64",
    "kernel-default-4.4.82-6.3.1.x86_64",
    "kernel-default-4.4.82-6.6.1.x86_64",
    "kernel-default-4.4.82-6.9.1.x86_64",
    "kernel-default-4.4.90-92.45.1.x86_64",
    "kernel-default-4.4.90-92.50.1.x86_64",
    "kernel-default-4.4.92-6.18.1.x86_64",
    "kernel-default-4.4.92-6.30.1.x86_64",
    "kernel-default-4.4.103-6.33.1.x86_64",
    "kernel-default-4.4.103-6.38.1.x86_64",
    "kernel-default-4.4.103-92.53.1.x86_64",
    "kernel-default-4.4.103-92.56.1.x86_64",
    "kernel-default-4.4.114-92.64.1.x86_64",
    "kernel-default-4.4.114-92.67.1.x86_64",
    "kernel-default-4.4.114-94.11.3.x86_64",
    "kernel-default-4.4.114-94.14.1.x86_64",
    "kernel-default-4.4.120-92.70.1.x86_64",
    "kernel-default-4.4.120-94.17.1.x86_64",
    "kernel-default-4.4.121-92.73.1.x86_64",
    "kernel-default-4.4.121-92.80.1.x86_64",
    "kernel-default-4.4.121-92.85.1.x86_64",
    "kernel-default-4.4.121-92.92.1.x86_64",
    "kernel-default-4.4.121-92.95.1.x86_64",
    "kernel-default-4.4.121-92.98.1.x86_64",
    "kernel-default-4.4.121-92.101.1.x86_64",
    "kernel-default-4.4.121-92.104.1.x86_64",
    "kernel-default-4.4.121-92.109.2.x86_64",
    "kernel-default-4.4.121-92.114.1.x86_64",
    "kernel-default-4.4.121-92.117.1.x86_64",
    "kernel-default-4.4.121-92.120.1.x86_64",
    "kernel-default-4.4.121-92.125.1.x86_64",
    "kernel-default-4.4.121-92.129.1.x86_64",
    "kernel-default-4.4.121-92.135.1.x86_64",
    "kernel-default-4.4.121-92.138.1.x86_64",
    "kernel-default-4.4.121-92.141.1.x86_64",
    "kernel-default-4.4.126-94.22.1.x86_64",
    "kernel-default-4.4.131-94.29.1.x86_64",
    "kernel-default-4.4.132-94.33.1.x86_64",
    "kernel-default-4.4.138-94.39.1.x86_64",
    "kernel-default-4.4.140-94.42.1.x86_64",
    "kernel-default-4.4.143-94.47.1.x86_64",
    "kernel-default-4.4.155-94.50.1.x86_64",
    "kernel-default-4.4.156-94.57.1.x86_64",
    "kernel-default-4.4.156-94.61.1.x86_64",
    "kernel-default-4.4.156-94.64.1.x86_64",
    "kernel-default-4.4.162-94.69.2.x86_64",
    "kernel-default-4.4.162-94.72.1.x86_64",
    "kernel-default-4.4.175-94.79.1.x86_64",
    "kernel-default-4.4.176-94.88.1.x86_64",
    "kernel-default-4.4.178-94.91.2.x86_64",
    "kernel-default-4.4.180-94.97.1.x86_64",
    "kernel-default-4.4.180-94.100.1.x86_64",
    "kernel-default-4.4.180-94.103.1.x86_64",
    "kernel-default-4.4.180-94.107.1.x86_64",
    "kernel-default-4.4.180-94.113.1.x86_64",
    "kernel-default-4.4.180-94.116.1.x86_64",
    "kernel-default-4.4.180-94.121.1.x86_64",
    "kernel-default-4.4.180-94.124.1.x86_64",
    "kernel-default-4.4.180-94.127.1.x86_64",
    "kernel-default-4.4.180-94.130.1.x86_64",
    "kernel-default-4.12.14-23.1.x86_64",
    "kernel-default-4.12.14-25.3.1.x86_64",
    "kernel-default-4.12.14-25.6.1.x86_64",
    "kernel-default-4.12.14-25.13.1.x86_64",
    "kernel-default-4.12.14-25.16.1.x86_64",
    "kernel-default-4.12.14-25.19.1.x86_64",
    "kernel-default-4.12.14-25.22.1.x86_64",
    "kernel-default-4.12.14-25.25.1.x86_64",
    "kernel-default-4.12.14-25.28.1.x86_64",
    "kernel-default-4.12.14-94.41.1.x86_64",
    "kernel-default-4.12.14-95.3.1.x86_64",
    "kernel-default-4.12.14-95.6.1.x86_64",
    "kernel-default-4.12.14-95.13.1.x86_64",
    "kernel-default-4.12.14-95.16.1.x86_64",
    "kernel-default-4.12.14-95.19.1.x86_64",
    "kernel-default-4.12.14-95.24.1.x86_64",
    "kernel-default-4.12.14-95.29.1.x86_64",
    "kernel-default-4.12.14-95.32.1.x86_64",
    "kernel-default-4.12.14-95.37.1.x86_64",
    "kernel-default-4.12.14-95.40.1.x86_64",
    "kernel-default-4.12.14-95.45.1.x86_64",
    "kernel-default-4.12.14-95.48.1.x86_64",
    "kernel-default-4.12.14-95.51.1.x86_64",
    "kernel-default-4.12.14-95.54.1.x86_64",
    "kernel-default-4.12.14-95.57.1.x86_64",
    "kernel-default-4.12.14-95.60.1.x86_64",
    "kernel-default-4.12.14-120.1.x86_64",
    "kernel-default-4.12.14-122.7.1.x86_64",
    "kernel-default-4.12.14-122.12.1.x86_64",
    "kernel-default-4.12.14-122.17.1.x86_64",
    "kernel-default-4.12.14-122.20.1.x86_64",
    "kernel-default-4.12.14-122.23.1.x86_64",
    "kernel-default-4.12.14-122.26.1.x86_64",
    "kernel-default-4.12.14-122.29.1.x86_64",
    "kernel-default-4.12.14-122.32.1.x86_64",
    "kernel-default-4.12.14-122.37.1.x86_64",
    "kernel-default-4.12.14-150.14.2.x86_64",
    "kernel-default-4.12.14-150.17.1.x86_64",
    "kernel-default-4.12.14-150.22.1.x86_64",
    "kernel-default-4.12.14-150.27.1.x86_64",
    "kernel-default-4.12.14-150.32.1.x86_64",
    "kernel-default-4.12.14-150.35.1.x86_64",
    "kernel-default-4.12.14-150.38.1.x86_64",
    "kernel-default-4.12.14-150.41.1.x86_64",
    "kernel-default-4.12.14-150.47.1.x86_64",
    "kernel-default-4.12.14-150.52.1.x86_64",
    "kernel-default-4.12.14-150.55.1.x86_64",
    "kernel-default-4.12.14-150.58.1.x86_64",
    "kernel-default-4.12.14-195.1.x86_64",
    "kernel-default-4.12.14-197.4.1.x86_64",
    "kernel-default-4.12.14-197.7.1.x86_64",
    "kernel-default-4.12.14-197.10.1.x86_64",
    "kernel-default-4.12.14-197.15.1.x86_64",
    "kernel-default-4.12.14-197.18.1.x86_64",
    "kernel-default-4.12.14-197.21.1.x86_64",
    "kernel-default-4.12.14-197.26.1.x86_64",
    "kernel-default-4.12.14-197.29.1.x86_64",
    "kernel-default-4.12.14-197.34.1.x86_64",
    "kernel-default-4.12.14-197.37.1.x86_64",
    "kernel-default-4.12.14-197.40.1.x86_64",
    "kernel-default-4.12.14-197.45.1.x86_64",
    "kernel-default-4.12.14-197.48.1.x86_64",
    "kernel-default-4.12.14-197.51.1.x86_64",
    "kernel-default-4.12.14-197.56.1.x86_64",
    "kernel-default-5.3.18-22.2.x86_64",
    "kernel-default-5.3.18-24.9.1.x86_64",
    "kernel-default-5.3.18-24.12.1.x86_64",
    "kernel-default-5.3.18-24.15.1.x86_64",
    "libdatrie1-0.2.4-17.19.x86_64",
    "libsamba-passdb0-4.6.16+git.237.40a3f495f75-3.55.1.x86_64",
    "libsamba-passdb0-4.6.16+git.237.40a3f495f75-3.57.1.x86_64",
    "libsamba-passdb0-4.6.16+git.237.40a3f495f76-3.55.1.x86_64",
    "libsamba-passdb0-4.6.17+git.237.40a3f495f75-3.57.1.x86_64",
    "libtevent0-0.9.34-3.6.1.x86_64",
    "make-4.0-4.1.x86_64",
    "python3-argcomplete-1.9.2-4.3.1.noarch",
    "resource-agents-4.0.1+git.1495055229.643177f1-2.48.2.x86_64",
]

rpm_list_invalids = [
    "??????????????????",
    "your computer is slow!!",
    "",
    "# this is a comment",
    "this-is-bad-6.6.6-2.2.2.2.2.rpm",
]


def test_vertuple_cmp():
    for s in version_tuple_strings:
        assert str(VerTuple(s)) == s

    for (l, r) in version_tuple_pairs_eq:
        assert VerTuple(l) == VerTuple(r)
        assert VerTuple(l) <= VerTuple(r)
        assert VerTuple(l) >= VerTuple(r)
        assert not VerTuple(l) < VerTuple(r)
        assert not VerTuple(l) > VerTuple(r)

    for (l, r) in version_tuple_pairs_lt:
        assert not VerTuple(l) == VerTuple(r)
        assert not VerTuple(r) == VerTuple(l)
        assert VerTuple(l) < VerTuple(r)
        assert not VerTuple(r) < VerTuple(l)
        assert VerTuple(l) <= VerTuple(r)
        assert not VerTuple(r) <= VerTuple(l)
        assert not VerTuple(l) > VerTuple(r)
        assert VerTuple(r) > VerTuple(l)
        assert not VerTuple(l) >= VerTuple(r)
        assert VerTuple(r) >= VerTuple(l)


def test_rpm_name_clean():
    for s in rpm_list_sorted:
        assert s == str(RPM.from_name(s))


def test_rpm_name_strip_noise():
    """Parse rpm names with edge white space and .rpm extension"""
    for s in rpm_list_sorted:
        assert s == str(RPM.from_name(f" \t  {s}.rpm\t\t\t   "))


def test_rpm_invalids():
    for s in rpm_list_invalids:
        assert type(RPM.from_name(s)) == type(None)


def test_rpm_sorting():
    rpm_list_unsorted = rpm_list_sorted.copy()
    random.shuffle(rpm_list_unsorted)
    RPM_list = [*map(RPM.from_name, rpm_list_unsorted)]
    RPM_list.sort()
    rpm_list_hopefully_sorted = [*map(str, RPM_list)]
    assert tuple(rpm_list_hopefully_sorted) == tuple(rpm_list_sorted)


def test_rpmlist_sorting():
    rpm_list_unsorted = rpm_list_sorted.copy()
    random.shuffle(rpm_list_unsorted)
    rpmlist = RPMlist.from_name_list(rpm_list_unsorted)
    assert tuple([*rpmlist]) == tuple(rpm_list_sorted)
