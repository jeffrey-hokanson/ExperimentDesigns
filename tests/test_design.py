import numpy as np
import psdr
import json
import pytest
import sys, os
import re
import urllib.request
from functools import lru_cache

try:
	check = os.environ['EXP_DESIGN_CHECK']
	assert check in ['all', 'novel']
except KeyError:
	check = 'novel'
except AssertionError as e:
	print(" 'EXP_DESIGN_CHECK' should either be 'all' or 'novel' ")
	raise e


try: 
	MAINDIR = os.environ['EXP_DESIGN_MAINDIR']
except:
	MAINDIR = '.'


def get_current_design(fname):
	origin_master = "https://raw.githubusercontent.com/jeffrey-hokanson/ExperimentDesigns/master/"
	path = origin_master + fname
	with urllib.request.urlopen(path) as response:	
		design = json.loads(response.read())
	return design

def get_new_design(fname):
	with open( os.path.join(MAINDIR,fname), 'r') as f:
		design = json.load(f)
	return design

def list_designs(root):
	# Generate list of designs 
	design_files = []
	for r, d, f in os.walk(os.path.join(MAINDIR, 'designs/',root)):
		for fname in f:
			if fname.endswith('.json'):
				design_files.append(os.path.join(r, fname))
			else:
				raise AssertionError("Invalid format for a design")
	return design_files


@lru_cache()
def check_designs(root, check):
	design_files = list_designs(root)

	if check == 'all':
		return design_files

	assert check == 'novel'	

	filtered_design_files = []
	for df in design_files:
		try:
			old_design = get_current_design(df)
			new_design = get_new_design(df)
			if new_design != old_design:
				filtered_design_files.append(df)
		
		except urllib.error.HTTPError:
			# If we don't have an existing file, we check it
			filtered_design_files.append(df)

	return filtered_design_files

@pytest.mark.parametrize("fname", check_designs("minimax/l2", check) )
def test_minimax_l2_design(fname):
	r""" This checks the design for consistency. 
	It does not check if there is an improvment
	"""

	print(f"Loading design '{fname}'")
	
	design = get_new_design(fname)

	if design['domain'] == 'square':
		domain = psdr.BoxDomain(np.zeros(2), np.ones(2))
	else:
		raise AssertionError('domain type "%s" not recognized' % design['domain'])


	assert design['metric'] == 'l2', "Expected metric 'l2', got '%s'" % design['metric']
	assert design['objective'] == 'minimax', "Expected objective 'minimax', got '%s'" % design['objective']


	X = np.array(design['X'])
	M = int(re.search(r'_(.*?).json', fname).group(1))

	assert X.shape[0] == M, f"Number of points does not match the file name: name suggests {M}, files has {X.shape[0]}"
	assert X.shape[1] == len(domain), "Points are in a different dimensional space than the domain" 
	assert np.all(domain.isinside(X)), "All points must be inside the domain"
	 
	# Check the objective value
	V = psdr.voronoi_vertex(domain, X)
	D = psdr.cdist(X, V)
	radius = np.max(np.min(D, axis= 0))

	
	print("Measured radius", '%20.15e' % radius)
	print("Reported radius", '%20.15e' % design['radius'])
	assert np.isclose(radius, design['radius'], rtol = 1e-10, atol = 1e-10)


@pytest.mark.parametrize("fname", check_designs("minimax/l2", check) )
def test_minimax_l2_design_improvement(fname):

	new_design = get_new_design(fname)
	try:
		old_design = get_current_design(fname)	
		print(f"Old design radius {old_design['radius']:20.15e}")
		print(f"New design radius {new_design['radius']:20.15e}")
		assert new_design['radius'] <= old_design['radius'], "The new design does not decrease the radius balls covering the domain"
	except urllib.error.HTTPError:
		print("No existing design found")


if __name__ == '__main__':
	print("Checking designs: check=", check)
	for d in check_designs('minimax/l2', check):
		print(d)
