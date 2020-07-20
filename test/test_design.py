import numpy as np
import psdr
import json

def check_minimax_l2_design(design):
	r""" This checks the design for consistency. 
	It does not check if there is an improvment
	"""

	if design['domain'] == 'square':
		domain = psdr.BoxDomain(np.zeros(2), np.ones(2))
	else:
		raise AssertionError('domain type "%s" not recognized' % design['domain'])


	assert design['metric'] == 'l2', "Expected metric 'l2', got '%s'" % design['metric']
	assert design['objective'] == 'minimax', "Expected objective 'minimax', got '%s'" % design['objective']


	X = np.array(design['X'])

	assert X.shape[1] == len(domain), "Points are in a different dimensional space than the domain" 
	assert np.all(domain.isinside(X)), "All points must be inside the domain"
	 
	# Check the objective value
	V = psdr.voronoi_vertex(domain, X)
	D = psdr.cdist(X, V)
	radius = np.max(np.min(D, axis= 0))

	
	print("Measured radius", '%20.15e' % radius)
	print("Reported radius", '%20.15e' % design['radius'])
	assert np.isclose(radius, design['radius'], rtol = 1e-10, atol = 1e-10)

if __name__ == '__main__':
	
	with open('../designs/minimax/l2/square_0010.dat', 'r') as f:
		design = json.load(f)

	check_minimax_l2_design(design)	
