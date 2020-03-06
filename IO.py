# Copyright (C) 2019  Andrea Vázquez Varela

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

#Authors:
# Narciso López López
# Andrea Vázquez Varela
#Creation date: 30/10/2019
#Last update: 31/10/2019

import shutil
import os
import IOFibers as IOF

def create_output(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)
    return path

def read_bundles(path):
    bundles, names = IOF.read_bundles(path)
    return bundles[0]

def write_bundles(clusters,centroids,bundles_dir,out_path):
    IOF.write_bundles(out_path+"/finalClusters.bundles",clusters)
    IOF.write_bundles(out_path+"/centroids.bundles",[centroids])
