# FFClust

## Code Dependencies
To use the code, it is necessary to install the following libraries:
- Numpy: https://numpy.org/
- Sklearn: https://scikit-learn.org/stable/
- Scipy: https://www.scipy.org/
- Networkx: https://networkx.github.io/

### OPTION 1: Dependency installation via pip3 in Ubuntu
```
pip3 install numpy
pip3 install scikit-learn
pip3 install scipy
pip3 install networkx
```

### OPTION 2: Dependency installation via apt in Ubuntu
```
sudo apt install python3-numpy
sudo apt-get install python3-sklearn
sudo apt install python3-scipy
sudo apt-get install python3-networkx
```

## Example data
In the following link a subject of the ARCHI database resampled in 21 points is available.
https://drive.google.com/drive/folders/1ZkdPRH51UeAucEZniwdJVZ65A9Du4cBz?usp=sharing

## Use example

If necessary, compile before the segmentation code in segmentation_clust_v1.2/
```
gcc -fPIC -shared  -O3 -o segmentation.so segmentation.c -fopenmp -ffast-math
```
FFclust algorithm execution:
```
python3 main.py --infile example_data/21ptos-1mfibras-ARCHI.bundles --outdir result
```
## Input parameters
- **--points**: Points to be used in map clustering **Default: 0,3,10,17,20**
- **--ks**: Number of clusters to be used for each point in K-Means for map **Default: 300, 200, 200, 200, 300**
- **--thr-seg**: Minimum threshold for segmentation in mm (in paper dRMax) **Default: 6**
- **--thr-join**: Minimum threshold for join in mm (in paper dMMax) **Default: 6**
- **--infile**: Input streamlines file (fibers must be resampled in 21 points) in format .bundles/.bundlesdata.
- **--outdir**: Directory where to place all output

## Input/output data format
### Input files
Sample subject is provided in https://drive.google.com/drive/folders/1ZkdPRH51UeAucEZniwdJVZ65A9Du4cBz?usp=sharing.
- 21ptos-1mfibras-ARCHI.bundles and 21ptos-1mfibras-ARCHI.bundledata: It is a subject of the archi database, whose fibers are resampled in 21 equidistant points.

### Output files
- finalBundles/: This folder contains all the resulting clusters separately in .bundles / .bundlesdata format.
- centroids.bundles/.bundlesdata: This file contains all the ordered centroids of the clusters. For example, the cluster 0.bundles/bundlesdata corresponds to the centroid that is in position 0 in centroids.bundles/bundlesdata
- stats.log: This file contains the execution time and the number of clusters at each stage of the algorithm.
