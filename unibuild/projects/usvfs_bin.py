# Copyright (C) 2015 Sebastian Herbord.  All rights reserved.
# Copyright (C) 2016 - 2019 Mod Organizer contributors.
#
# This file is part of Mod Organizer.
#
# Mod Organizer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mod Organizer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mod Organizer.  If not, see <http://www.gnu.org/licenses/>.
import logging
import os.path
import shutil
import sys
from glob import glob

from config import config
from unibuild import Project
from unibuild.modules import build, github, urldownload

install_path = config["paths"]["install"]
download_path = config["paths"]["download"]
arch = "x64" if config['architecture'] == 'x86_64' else "x86"
if config['architecture'] == 'x86_64':
    usvfs_bin = Project("usvfs_bin")
else:
    usvfs_bin = Project("usvfs_bin_32")


def appveyor_url(filename,sysarch):
    return "https://ci.appveyor.com/api/projects/Modorganizer2/usvfs/artifacts/{0}?job=Platform:%20{1}".format(
                                                                                                            filename,
                                                                                                            sysarch)


def copy_usvfs_files(context):
    if not os.path.exists(os.path.join(install_path, "libs")):
        os.mkdir(os.path.join(install_path, "libs"))
    for f in glob(os.path.join(download_path, "usvfs_{}.lib".format(arch))):
        shutil.copy(f, os.path.join(install_path, "libs"))
    if not os.path.exists(os.path.join(install_path, "bin")):
        os.mkdir(os.path.join(install_path, "bin"))
    for f in glob(os.path.join(download_path, "usvfs_{}.dll".format(arch))):
        shutil.copy(f, os.path.join(install_path, "bin"))
    for f in glob(os.path.join(download_path, "usvfs_proxy_{}.exe".format(arch))):
        shutil.copy(f, os.path.join(install_path, "bin"))
    if not os.path.exists(os.path.join(install_path, "pdb")):
        os.mkdir(os.path.join(install_path, "pdb"))
    for f in glob(os.path.join(download_path, "usvfs_proxy_{}.pdb".format(arch))):
        shutil.copy(f, os.path.join(install_path, "pdb"))
    for f in glob(os.path.join(download_path, "usvfs_{}.pdb".format(arch))):
        shutil.copy(f, os.path.join(install_path, "pdb"))
    return True


usvfs_bin \
    .depend(build.Execute(copy_usvfs_files)
    .depend(urldownload.URLDownload(appveyor_url("lib/usvfs_{}.pdb".format(arch), "{}".format(arch)))
    .depend(urldownload.URLDownload(appveyor_url("lib/usvfs_{}.dll".format(arch), "{}".format(arch)))
    .depend(urldownload.URLDownload(appveyor_url("lib/usvfs_{}.lib".format(arch), "{}".format(arch)))
    .depend(urldownload.URLDownload(appveyor_url("bin/usvfs_proxy_{}.exe".format(arch), "{}".format(arch)))
    .depend(urldownload.URLDownload(appveyor_url("bin/usvfs_proxy_{}.pdb".format(arch), "{}".format(arch)))))))))



