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
#Creation date: 06/03/2020
#Last update: 06/03/2020

import os
import re
import struct 
import numpy as np

byte_order = "DCBA"

def check_errors(path):
    if not (os.path.splitext(path)[1]) == ".bundles":
        print("A file with extension .bundles is required")
        exit(-1)
    if not (os.path.exists(path+"data")):
        print("The .bundlesdata file is missed")
        exit(-1)    

def read_header(path):
    f = open(path,"r")
    lines = f.readlines()
    nfibers = int(re.findall('\d+', lines[4])[0])
    data_path = os.path.splitext(path)[0]+(lines[5].split("\'")[-2].replace('*',''))
    dim = int(re.findall('\d+', lines[7])[0])
    bun_string = lines[2].split("[")[1].split(",")
    bnames = list(n.replace("'","") for i,n in enumerate(bun_string) if i % 2 == 0)[:-1]
    intervals = list(int(i.replace("]","")) for j,i in enumerate(bun_string) if j % 2 != 0)
    byte_order = (lines[3].split("\'")[-2])
    if byte_order == "DCBA":
        byte_order = "little"
    elif byte_order == "ABCD":
        byte_order = "big"
    f.close()
    return data_path, dim, nfibers, bnames, intervals, byte_order

def read_data(data_path,dim,nfibers,bnames,intervals,byte_order):
    intervals.append(nfibers)
    f = open(data_path,"rb")
    bundles = []
    for i in range(len(intervals)-1):
        nfibers_bun = intervals[i+1]-intervals[i]
        bundle = []
        for j in range(nfibers_bun):
            npoints = int.from_bytes(f.read(4), byteorder=byte_order)
            ndata = dim * npoints
            fiber = np.frombuffer(f.read(4*ndata),'f')
            bundle.append(np.resize(fiber,(npoints,dim)))
        bundles.append(np.array(bundle))
    f.close()
    return np.array(bundles)

def read_bundles(path):
    data_path, dim, nfibers, bnames, intervals, byte_order = read_header(path)
    return read_data(data_path,dim,nfibers,bnames,intervals, byte_order), bnames

def write_header(path,bnames,intervals,dim,nfibers):
    f = open(path,"w")
    f.write("attributes = {\n    'binary' : 1,\n    'bundles' : ")
    f.write(str([val for pair in zip(bnames, intervals) for val in pair])+",\n")
    f.write("    'byte_order' : "+'\''+byte_order+'\',\n')
    f.write("    'curves_count' : "+str(nfibers)+",\n")
    f.write("    'data_file_name' : "+"\'*"+os.path.splitext(path+"data")[1]+"\',\n")
    f.write("    'format' : 'bundles_1.0',\n")
    f.write("    'space_dimension' : "+str(dim)+"\n  }")
    f.close()

def write_data(data_path,bundles,dim):
    f = open(data_path,"wb")
    for b in bundles:
        for fiber in b:
            f.write(np.array([len(fiber)],dtype=np.int32).tostring())
            f.write(fiber.ravel().tostring())
    f.close()

def write_bundles(path,bundles,bnames=None):
    if bnames == None:
        bnames = [''+str(i)+'' for i in range(len(bundles))]
    bnames = [''+n.strip()+'' for n in bnames]
    data_path = path+"data"
    dim = len(bundles[0][0][0])
    nfibers = sum(len(b) for b in bundles)
    intervals = [0]
    for i in range(1,len(bundles),1):
        intervals.append(intervals[i-1]+len(bundles[i-1])) 

    write_header(path,bnames,intervals,dim,nfibers)
    write_data(data_path,bundles,dim)
