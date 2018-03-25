import numpy as np
#Develop a covaraince from the matached points
#Perform SVD- Get USV
#rotation is found out from VU'

def find_rotation(clsoestPoint, original):
	covariance = np.dot(np.transpose(clsoestPoint), original)
	U, s, V = np.linalg.svd(covariance)
	rotation = np.dot(V,np.transpose(U))
	return rotation

