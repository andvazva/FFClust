# -*- coding: utf-8 -*-

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
# Andrea Vázquez Varela
# Narciso López López
#Creation date: 15/10/2019
#Last update: 27/03/2020

import numpy as np
from random import choice
import math

def is_inverted(f1,f2):
	dist_00 = np.linalg.norm(f1[0]-f2[0])
	dist_020 = np.linalg.norm(f1[0]-f2[20])
	if dist_00 > dist_020:
		return True
	else:
		return False

def align_fibers(bundle):
	new_fibers = [bundle[0]]
	f1 = bundle[0]
	for f2 in bundle[1:]:
		if is_inverted(f1,f2):
			new_fibers.append(f2[::-1])
		else:
			new_fibers.append(f2)
	return np.asarray(new_fibers)

def centroid_mean_align(bundle):
	fibers = align_fibers(bundle)
	return np.asarray(sum(fibers)/len(fibers))

def matrix_dist(streamlines, get_max=True, get_mean=False):
    x = np.asarray(streamlines)
    distances = ((np.stack((x,x[:,::-1]))[:,None]-x[:,None])**2).sum(axis=4)
    if get_max and get_mean:
        max_distances = np.sqrt(distances.max(axis=3).min(axis=0))
        mean_distances = np.sqrt(distances.mean(axis=3).min(axis=0))
        return max_distances, mean_distances
    elif get_max:
        return np.sqrt(distances.max(axis=3).min(axis=0))
    elif get_mean:
        return  np.sqrt(distances.mean(axis=3).min(axis=0))
    else:
        print('error, should return atleast one matrix')

def fiber_length_21(f):
	return(np.linalg.norm(f[0]-f[1])*21)

def calc_centroid(input_fibers):
	input_fibers = sorted(input_fibers, key =fiber_length_21)
	lindex = math.floor((len(input_fibers)-1)*0.6)
	uindex = math.floor((len(input_fibers)-1)*0.8)
	long_fibers = [f for i,f in enumerate(input_fibers) if i>=lindex and i<uindex]
	if len(long_fibers) == 0:
		return choice(input_fibers)
	nfibers = math.floor(len(long_fibers)*0.1)
	fibers_10 = [choice(long_fibers) for i in range(nfibers)]
	if len(fibers_10) == 0:
		return choice(long_fibers)
	dist_matrix = matrix_dist(fibers_10)
	min_dist = 1000
	selected_fiber = -1
	for i,row in enumerate(dist_matrix):
		sum_row = sum(row)
		if sum_row < min_dist:
			min_dist = sum_row
			selected_fiber = i
	return(fibers_10[selected_fiber])
