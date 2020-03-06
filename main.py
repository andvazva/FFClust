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
#Last update: 06/03/2020

import argparse
import clustering
import IO
import numpy as np
import logging

def main():
    parser = argparse.ArgumentParser(description='Perform clustering on a dataset of streamlines')
    parser.add_argument('--points', nargs='*', type=int, default=list((0,3,10,17,20)),
                        help='Points to be used in map clustering')
    parser.add_argument('--ks', nargs='*', type=int, default=list((300, 200, 200, 200, 300)),
                        help='Number of clusters to be used for each point in K-Means for map')
    parser.add_argument('--thr-seg', type=float, default=6,
                        help='Minimum threshold for segmentation')
    parser.add_argument('--thr-join', type=float, default=6,
                        help='Minimum threshold for join')
    parser.add_argument('--outdir',
                        help='Directory where to place all output')
    parser.add_argument('--infile', help='Input streamlines file')
    args = parser.parse_args()

    bundles_dir = IO.create_output(args.outdir)

    fibers = IO.read_bundles(args.infile)
    clusters,centroids,log = clustering.fiber_clustering(fibers,args.points,args.ks,args.thr_seg,args.thr_join)

    logging.basicConfig(level = logging.INFO, filename = args.outdir+"/stats.log")
    logging.info(log)

    IO.write_bundles(clusters,centroids,bundles_dir,args.outdir)


if __name__=="__main__":
    main()