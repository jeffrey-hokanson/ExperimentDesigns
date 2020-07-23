import numpy as np
import psdr
import json
from itertools import product
from joblib import Memory
from joblib import Parallel, delayed
from tqdm import tqdm
memory = Memory('.cache', verbose = False)


@memory.cache
def generate_minimax_square(N, seed):
	np.random.seed(seed)
	domain = psdr.BoxDomain(0*np.zeros(2), np.ones(2))

	# Generate a design
	try:
		X = psdr.minimax_lloyd(domain, N, maxiter = 500, xtol = 1e-9, verbose = False)

		# Compute the disc diameter to cover the domain
		V = psdr.voronoi_vertex(domain, X)
		D = psdr.cdist(X, V)
		radius = np.max(np.min(D, axis= 0))

		# save the file
		design = {
			'author': 'Jeffrey M. Hokanson',
			'notes': f'psdr.minimax_lloyd seed={seed}, maxiter=500, xtol = 1e-9',
			'objective': 'minimax',
			'metric': 'l2',
			'domain': 'square',
			'radius': radius,
			'X': X.tolist()
		}
	except:
		design = {
			'radius': np.inf
		}

	print(f"M: {N:4d} \t seed {seed:4d} finished") 
	return design
	#with open('square_%04d.dat' % N, 'w') as f:
	#	json.dump(design, f)	


if __name__ == '__main__':
	Ms = np.arange(11,51)
	seeds = np.arange(100)
	M_seed = product(Ms, seeds)
	
	# We first iterate through all designs, caching the result
	with Parallel(n_jobs = 30) as parallel:
		#iterator = tqdm(M_seed, total = len(Ms)*len(seeds))
		iterator = M_seed
		parallel(delayed(generate_minimax_square)(*args) for args in iterator)

	# Then we dump the best of each to disk

	for M in Ms:
		radius = [generate_minimax_square(M, seed)['radius'] for seed in seeds]
		best_seed = np.argmin(radius)
		design = generate_minimax_square(M, best_seed)
		with open(f'../designs/minimax/l2/square_{M:04d}.json', 'w') as f:
			json.dump(design, f)


