#!/usr/bin/env python
#
# Copyright 2010 Alexandre Fiori
# based on the original Tornado by Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import re
import sys
import platform
import setuptools
from distutils import log

requires = ["twisted"]

def version_cmp(version1, version2):
    """
    Return True if version1 is less greater than version2
    """
    def normalize(v):
        return [int(x) for x in re.sub(r'(\.0+)*$','', v).split(".")]
    return normalize(version1) < normalize(version2)

# Avoid installation problems on old RedHat distributions (ex. CentOS 5)
# http://stackoverflow.com/questions/7340784/easy-install-pyopenssl-error
py_version = platform.python_version()

if (version_cmp(str(py_version), str('2.6'))):
    distname, version, _id = platform.dist()
else:
    distname, version, _id = platform.linux_distribution()

is_redhat = distname in ["CentOS", "redhat"]
if is_redhat and version and StrictVersion(version) < StrictVersion('6.0'):
    requires.append("pyopenssl==0.12")
else:
    requires.append("pyopenssl")

extra = dict(extras_require={'ssl': requires})

try:
    from setuptools.command import egg_info
    egg_info.write_toplevel_names
except (ImportError, AttributeError):
    pass
else:
    """
    'twisted' should not occur in the top_level.txt file as this
    triggers a bug in pip that removes all of twisted when a package
    with a twisted plugin is removed.
    """
    def _top_level_package(name):
        return name.split('.', 1)[0]

    def _hacked_write_toplevel_names(cmd, basename, filename):
        pkgs = dict.fromkeys(
            [_top_level_package(k)
                for k in cmd.distribution.iter_distribution_names()
                if _top_level_package(k) != "twisted"
            ]
        )
        cmd.write_file("top-level names", filename, '\n'.join(pkgs) + '\n')

    egg_info.write_toplevel_names = _hacked_write_toplevel_names


setuptools.setup(
    name="cyclone",
    version="1.2",
    author="fiorix",
    author_email="fiorix@gmail.com",
    url="http://cyclone.io/",
    license="http://www.apache.org/licenses/LICENSE-2.0",
    description="Non-blocking web server for Python. "
                "Tornado API as a Twisted protocol.",
    keywords="python non-blocking web server twisted facebook tornado",
    packages=["cyclone", "twisted.plugins", "cyclone.tests", "cyclone.testing"],
    package_data={"twisted": ["plugins/cyclone_plugin.py"],
                  "cyclone": ["appskel_default.zip",
                              "appskel_foreman.zip",
                              "appskel_signup.zip"]},
    scripts=["scripts/cyclone"],
    **extra
)

try:
    from twisted.plugin import IPlugin, getPlugins
    list(getPlugins(IPlugin))
except Exception as e:
    log.warn("*** Failed to update Twisted plugin cache. ***")
    log.warn(str(e))
