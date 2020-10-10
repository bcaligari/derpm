import re
import logging


class VerTuple(object):
    """An orderable dot or plus sign separated tuple."""

    def __init__(self, ver_string):
        self._str = ver_string  # to preserve + or . delimiters
        self._elements = re.split(r"[.+]", ver_string)

    def _compare(self, other):
        for i in range(max(len(self._elements), len(other._elements))):
            a = self._elements[i] if i < len(self._elements) else None
            b = other._elements[i] if i < len(other._elements) else None
            if a is None:
                return -1
            if b is None:
                return 1
            if a.isnumeric() and b.isnumeric():
                if int(a) < int(b):
                    return -1
                elif int(a) > int(b):
                    return 1
            else:
                if a < b:
                    return -1
                elif a > b:
                    return 1
        return 0

    def __lt__(self, other):
        return self._compare(other) == -1

    def __eq__(self, other):
        return self._compare(other) == 0

    def __gt__(self, other):
        return self._compare(other) == 1

    def __le__(self, other):
        return self._compare(other) != 1

    def __ge__(self, other):
        return self._compare(other) != -1

    def __str__(self):
        return self._str

    def __hash__(self):
        return hash(self._str)


class RPM(object):
    """An RPM object representation."""

    def __init__(self, name, version, release, arch):
        """Initialise RPM from constituent filename parts."""
        self._name = name
        self._version = VerTuple(version)
        self._release = VerTuple(release)
        self._arch = arch

    @classmethod
    def from_name(cls, fullname):
        """Initialise RPM from <name>-<version>-<release>.<arch>[.rpm]"""
        fullname = fullname.strip()
        fullname = re.sub(r"\.rpm$", "", fullname)
        m = re.match(r"^(.+)-(.+)-(.+?)\.([a-z][a-z0-9_]+?)$", fullname)
        if m:
            return cls(m[1], m[2], m[3], m[4])
        else:
            return None

    @classmethod
    def from_dict(cls, rpm):
        """Initialise RPM from dict of parts"""
        return cls(rpm["name"], rpm["version"], rpm["release"], rpm["arch"])

    def __lt__(self, other):
        return (self._name, self._version, self._release, self._arch) < (
            other._name,
            other._version,
            other._release,
            other._arch,
        )

    def __eq__(self, other):
        return (self._name, self._version, self._release, self._arch) == (
            other._name,
            other._version,
            other._release,
            other._arch,
        )

    def __repr__(self):
        return repr((self._name, self._version, self._release, self._arch))

    def __str__(self):
        return f"{self._name}-{self._version}-{self._release}.{self._arch}"


class IterRPMlist(object):
    """Iterator for RPMlist"""

    def __init__(self, rpmdict):
        raw_list = []
        for name in rpmdict:  # str
            for arch in rpmdict[name]:  # str
                for version in rpmdict[name][arch]:
                    for release in rpmdict[name][arch][version]:  # VerTuple
                        raw_list.append((name, version, release, arch))  # VerTuple
        raw_list.sort()
        self._rpmlist = [f"{rpm[0]}-{rpm[1]}-{rpm[2]}.{rpm[3]}" for rpm in raw_list]
        self._idx = 0

    def __next__(self):
        if self._idx < len(self._rpmlist):
            next_rpm = self._rpmlist[self._idx]
            self._idx += 1
            return next_rpm
        else:
            raise StopIteration


class RPMlist(object):
    """A queryable collection of rpms."""

    def __init__(self, rpmlist):
        """Initialise an RPMlist"""
        self._rpms = dict()
        for rpm in rpmlist:
            if not rpm._name in self._rpms:
                self._rpms[rpm._name] = dict()
            if not rpm._arch in self._rpms[rpm._name]:
                self._rpms[rpm._name][rpm._arch] = dict()
            if not rpm._version in self._rpms[rpm._name][rpm._arch]:
                self._rpms[rpm._name][rpm._arch][rpm._version] = list()
            self._rpms[rpm._name][rpm._arch][rpm._version].append(rpm._release)

    def __iter__(self):
        """Return an Iterator so we can iterate over it like a boss."""
        return IterRPMlist(self._rpms)

    def get_archs(self, name):
        """Get list of architectures for a name."""
        return self._rpms[name].keys() if name in self._rpms else list()

    def get_versions(self, name, arch):
        """Get list of versions for a name and arch."""
        versions = []
        if name in self._rpms:
            if arch in self._rpms[name]:
                for version in self._rpms[name][arch]:
                    for release in self._rpms[name][arch][version]:
                        versions.append(tuple([version, release]))
        return versions

    @classmethod
    def from_name_list(cls, rpm_list):
        """Build a list of RPM objects from a list of rpm names."""
        rpms = []
        for name in rpm_list:
            rpm = RPM.from_name(name)
            if not rpm:
                logging.warning(f"Unable to parse {name}.")
            else:
                rpms.append(rpm)
        return cls(rpms)


if __name__ == "__main__":
    pass
