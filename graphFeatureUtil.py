import numpy as np
import scipy
import scipy.sparse
import random

class graph:
 def __init__(self, fileName):
  f = open(fileName)
  print "beginning preprocessing"
  coordPairs = [tuple(x.split()) for x in f.readlines()]
  a, b = zip(*coordPairs)
  # The numbers identifying the vertices dont have any particular structure
  # so we need to make sure that they are labeled with numbers {0 to #vertices}
  # so that the coo_matrix constructor doesn't make a matrix that is too big or something.  
  i = list(set(a).union(set(b)))
  # the line below is what takes all the time
  # but it helps speed things up as .index() is really slow
  i2 = {x:i.index(x) for x in i} 
  a = np.array([i2[x] for x in a])
  b = np.array([i2[x] for x in b])
  print "done preprocessing"
  print "number of vertices" , max(a) + 1
  print "number of edges" , len(a)
  sparseCooDataMatrix = scipy.sparse.coo_matrix((np.ones(len(a)),(a,b)))
  self.sparseCscDataMatrix = scipy.sparse.csc_matrix(sparseCooDataMatrix)
  print "matrix shape" , sparseCooDataMatrix.shape 
 def generateFeatures(self, n):
  """Computes a series of vectors, v_i, w_i with i between 1 and n
  based of the bg graph.
  The entry (v_i)_j is the number of paths beginning at vertex j of length i.
  The entry (w_i)_j is the number of paths ending at vertex j of length i.
  These vectors are concatenated to form one giant feature , sample matrix.  
  2*n is the number of features produced for each vertex
  """
  A = self.sparseCscDataMatrix
  result = [A.sum(axis = 0).tolist()[0]]
  result.append(A.sum(axis = 1).T.tolist()[0])
  for i in range(1,n):
   print "start mult"
   A = A*self.sparseCscDataMatrix
   print "end mult, start sums"
   result.append(A.sum(axis = 0).tolist()[0])
   result.append(A.sum(axis = 1).T.tolist()[0])
   print "end sums"
  return np.vstack(result)
 def generateRandomSignalGraph(self, featureSize):
  """Returns a graph g, so that when g is added to the dataMatrix it makes a clique.  
  """
  vs = random.sample(range(self.sparseCscDataMatrix.shape[0]), featureSize)
  # Only want the edges that are not already present.
  # A little slow, but my signal graphs should be small enough.  
  extraEdgeCoords = [ (x,y) for x in vs for y in vs if not self.sparseCscDataMatrix[x,y]]
  print "len(extraEdgeCoords)", len(extraEdgeCoords)
  a, b = zip(*extraEdgeCoords)
  a = np.array(a)
  b = np.array(b)
  signalCooMatrix = scipy.sparse.coo_matrix((np.ones(len(a)),(a,b)), shape = self.sparseCscDataMatrix.shape)
  return scipy.sparse.csc_matrix(signalCooMatrix)
 def generateSignalPlusBGFeatures(self,n, signalSize):
  """Computes a series of vectors, v_i, w_i with i between 1 and n
  based off the bg graph plus a random complete signal graph.  
  The entry (v_i)_j is the number of paths beginning at vertex j of length i.
  The entry (w_i)_j is the number of paths ending at vertex j of length i.
  These vectors are concatenated to form one giant feature , sample matrix.  
  2*n is the number of features produced for each vertex
  signalSize is the number of vertices in the signal graph.  
  """
  B = self.sparseCscDataMatrix + self.generateRandomSignalGraph(signalSize)
  A = B
  result = [A.sum(axis = 0).tolist()[0]]
  result.append(A.sum(axis = 1).T.tolist()[0])
  for i in range(1,n):
   print "start mult"
   A = A*B 
   print "end mult, start sums"
   result.append(A.sum(axis = 0).tolist()[0])
   result.append(A.sum(axis = 1).T.tolist()[0])
   print "end sums"
  return np.vstack(result)
  
if __name__ == "__main__":
 g = graph("Cit-HepPh.txt")
 print g.generateSignalPlusBGFeatures(2,10).shape
 
