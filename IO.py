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
import bundleTools as bT

def create_output(path):
    bundes_dir = path+"/finalBundles"
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)
    os.mkdir(bundes_dir)
    return bundes_dir

def write_bundles(clusters,centroids,bundles_dir,out_path):
    for i,fibers in enumerate(clusters):
        bT.write_bundle(bundles_dir+"/"+str(i)+".bundles",fibers)
    bT.write_bundle(out_path+"/centroids.bundles",centroids)
