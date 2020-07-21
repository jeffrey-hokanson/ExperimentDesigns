import numpy as np
import psdr
import json

def generate_minimax_square(N = 10, seed = 0):
	domain = psdr.BoxDomain(0*np.zeros(2), np.ones(2))

	# Generate a design
	X = psdr.minimax_lloyd(domain, N, maxiter = 500, xtol = 1e-7, verbose = True)

	#X = domain.sample(N)

	# Compute the disc diameter to cover the domain
	V = psdr.voronoi_vertex(domain, X)
	D = psdr.cdist(X, V)
	radius = np.max(np.min(D, axis= 0))

	# save the file
	design = {
		'author': 'Jeffrey M. Hokanson',
		'objective': 'minimax',
		'metric': 'l2',
		'domain': 'square',
		'radius': radius,
		'X': X.tolist()
	}

	with open('square_%04d.dat' % N, 'w') as f:
		json.dump(design, f)	


if __name__ == '__main__':
	generate_minimax_square()
