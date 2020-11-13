%define  modulename jaraco.classes

Name:    python3-module-%modulename
Version: 3.1.0
Release: alt2

Summary: Utility functions for Python class constructs
License: MIT
Group:   Development/Python3
URL:     https://github.com/jaraco/jaraco.classes

BuildRequires(pre): rpm-build-python3
BuildRequires: python3-dev python3-module-setuptools_scm
BuildRequires: python3-module-setuptools
BuildRequires: python3-module-tox
BuildRequires: python3-module-pytest
BuildRequires: python3-module-pytest-flake8
BuildRequires: python3-module-black
BuildRequires: python3-module-pytest-cov
BuildArch: noarch
Source:  %name-%version.tar
Patch0: %name-%version-%release.patch

%description
%summary

%prep
%setup
%patch0 -p1

%build
export SETUPTOOLS_SCM_PRETEND_VERSION=%version
%python3_build

%install
export SETUPTOOLS_SCM_PRETEND_VERSION=%version
%python3_install

%check
export SETUPTOOLS_SCM_PRETEND_VERSION=%version
export PIP_NO_INDEX=YES
export TOXENV=py%{python_version_nodots python3}
# remove pyproject.toml
#rm pyproject.toml
# replace pytest executable name
sed -i 's|pytest |py.test3 |g' tox.ini
# cancel docbuild tests
sed -i 's|\.\[docs\]||g' tox.ini
sed -i 's|\(.*\)sphinx|#\1 py3_sphinx|g' tox.ini

sed -i '/\[testenv\]$/a whitelist_externals =\
    \/bin\/cp\
    \/bin\/sed\
setenv =\
    _PYTEST_BIN = %_bindir\/py.test3\
commands_pre =\
    \/bin\/cp {env:_PYTEST_BIN:} \{envbindir\}\/py.test3' tox.ini

tox.py3 --sitepackages -vv

%files
%python3_sitelibdir/jaraco/*
%python3_sitelibdir/%{modulename}*
%python3_sitelibdir/*.egg-info
%exclude %python3_sitelibdir/jaraco/__init__*
%exclude %python3_sitelibdir/jaraco/__pycache__/__init__*

%changelog
* Thu Nov 12 2020 Danil Shein <dshein@altlinux.org> 3.1.0-alt2
- new version

* Tue Dec 03 2019 Anton Farygin <rider@altlinux.ru> 2.0-alt1
- first build for ALT

