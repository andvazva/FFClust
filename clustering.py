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
# Narciso López López
# Andrea Vázquez Varela
#Creation date: 30/10/2019
#Last update: 11/03/2020

import multiprocessing as mp
from functools import partial
import numpy as np
from sklearn.cluster import MiniBatchKMeans
import time
from scipy import sparse
import bundleMetrics as metrics
import segmentation as seg
import networkx as nx

num_proc = mp.cpu_count()

def get_ranges(nfibers):
    total_len = nfibers
    len_groups, rest = divmod(total_len, num_proc)
    return list((n, min(n + len_groups, total_len)) for n in range(0, total_len, len_groups))

def kmeans(points,k):
    kmeans = MiniBatchKMeans(n_clusters=k,random_state=0)
    sm = sparse.csr_matrix(points)
    return kmeans.fit_predict(sm)

def parallel_kmeans(fibers,points,ks):
    selected_points = np.array(list(list(f[i] for f in fibers) for i in points))
    pool = mp.Pool(num_proc)
    results = pool.starmap(kmeans,zip(selected_points,ks))
    pool.close()
    return results

def mapping(point_clusters,r):
    fibers_map = {}
    for i in range(r[0],r[1],1):
        key = "_".join(str(point_clusters[p][i]) for p in range(len(point_clusters)))
        if key not in fibers_map:
            fibers_map[key] = [i]
        else:
            fibers_map[key].append(i)
    return fibers_map

def merge_maps(maps):
    final_map = {}
    for map in maps:
        for key, val in map.items():
            if key not in final_map:
                final_map[key] = val
            else:
                final_map[key].extend(val)
    return final_map

def parallel_mapping(point_clusters,ranges):

    partial_mapping = partial(mapping,point_clusters)
    pool = mp.Pool(num_proc)
    results = pool.map(partial_mapping, ranges)
    pool.close()
    fiber_clusters = merge_maps(results)
    return fiber_clusters

def parallel_reassignment(fibers,fiber_clusters,central_index,thr):
    size_filter = 5
    large_clusters,small_clusters,large_indices,small_indices,large_centroids,small_centroids = [], [], [], [], [], []
    small_indices = []
    for key,indices in fiber_clusters.items():
        if len(indices) > size_filter:
            large_indices.append(int(key.split("_")[central_index]))
            c = [fibers[i] for i in indices]
            large_clusters.append(c)
            large_centroids.append(metrics.centroid_mean_align(c))
        else:
            small_indices.append(int(key.split("_")[central_index]))
            c = [fibers[i] for i in indices]
            small_clusters.append(c)
            small_centroids.append(metrics.centroid_mean_align(c))
    reassignment = seg.segmentation(21,thr, large_centroids,small_centroids,len(small_centroids), len(large_centroids))
    count = 0
    num_fibers_reass = 0
    num_discarded = 0
    for small_index,large_index in enumerate(reassignment):
        fibers = small_clusters[small_index]
        if int(large_index)!=-1:
            large_clusters[large_index].extend(fibers)
            num_fibers_reass += len(fibers)
            count+=1
        else:
            if len(fibers)>2:
                recover_cluster = small_clusters[small_index]
                large_clusters.append(recover_cluster)
                large_indices.append(small_indices[small_index])
            else:
                num_discarded +=1
    return large_clusters,large_indices

def get_groups(clusters,central_index):
    groups = {}
    for i,cluster in enumerate(clusters):
        index = central_index[i]
        if index not in groups:
            groups[index] = [cluster]
        else:
            groups[index].append(cluster)
    return groups

def create_graph(centroids,thr):
    matrix_dist = metrics.matrix_dist(centroids, get_max=True)
    matrix_dist[matrix_dist>thr] = 0
    G = nx.from_numpy_matrix(matrix_dist)
    return G

def join(thr,group):
    centroids = [metrics.centroid_mean_align(c) for c in group]
    graph = create_graph(centroids,thr)
    cliques = sorted(nx.find_cliques(graph), key=len, reverse=True)
    visited = {}
    new_clusters,new_centroids = [] ,[]
    for clique in cliques:
        new_cluster = []
        for node in clique:
            if node not in visited:
                cluster = group[node]
                new_cluster.extend(cluster)
                visited[node] = True
        if len(new_cluster)>0:
            new_clusters.append(new_cluster)
            new_centroids.append(metrics.centroid_mean_align(new_cluster))
    return new_clusters,new_centroids

def parallel_join(fiber_clusters,cluster_indices,thr):
    groups = get_groups(fiber_clusters,cluster_indices)
    partial_join = partial(join,thr)
    pool = mp.Pool(num_proc)
    results = pool.map(partial_join, [g for key,g in groups.items()])
    pool.close()
    new_clusters,new_centroids = [], []
    for clust,centroids in results:
        new_clusters.extend(clust)
        new_centroids.extend([c] for c in centroids)
    return new_clusters,new_centroids


def fiber_clustering(fibers,points,ks,seg_thr,join_thr):
    init_time = time.time()
    ranges = get_ranges(len(fibers))
    log = ""
    init = time.time()
    point_clusters = parallel_kmeans(fibers,points,ks)
    log += ("Execution time of kmeans: "+str(round(time.time()-init,2))+" seconds\n")
    init = time.time()
    fiber_clusters_map = parallel_mapping(point_clusters,ranges)
    log += ("Execution time of mapping: "+str(round(time.time()-init,2))+" seconds\n")
    init = time.time()
    central_index = int((len(points) - 1)/2)
    fiber_clusters,cluster_indices = parallel_reassignment(fibers,fiber_clusters_map,central_index,seg_thr)
    log += ("Execution time of reassignment: "+str(round(time.time()-init,2))+" seconds\n")
    init = time.time()
    final_clusters,centroids = parallel_join(fiber_clusters,cluster_indices,join_thr)
    log += ("Execution time of join: "+str(round(time.time()-init,2))+" seconds\n")
    log += ("TOTAL TIME: "+str(round(time.time()-init_time,2))+" seconds\n\n")
    log += ("Number of clusters before reassignment: " + str(len(fiber_clusters_map)) + "\n")
    log += ("Number of clusters after reassignment: " + str(len(fiber_clusters)) + "\n")
    log += ("Number of FINAL CLUSTERS: " + str(len(final_clusters))+"\n")
    return final_clusters,centroids,log
