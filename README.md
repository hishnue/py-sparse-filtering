py-sparse-filtering
===================

I forked this code so that I could try out some ideas about sparse filtering.  
It is a python implementation of the Sparse Filtering code by Ngiam et al.

Dependencies
------------

The main code depends on numpy and scipy's optimization toolkit. For
the demo you also need matplotlib/pylab for visualization and `scipy.io.loadmat`
for reading in the image data.

The image data is the same as the data used by Jiquan Ngiam et al., and can be
downloaded from <http://cs.stanford.edu/~jngiam/data/patches.mat>.

The graph data called "Cit-HepPh.txt" and can be found at http://snap.stanford.edu/data/cit-HepPh.html.  
Please delete the meta-data at the top of the file.  
