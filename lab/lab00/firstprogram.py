from operator import floordiv, mod

def divide_exact(n, d):
	return floordiv(n, d), mod(n, d)

q, r = divde_exact(2013, 10)

def absolute_value(x):
	if x<0:
		return -x
	elif x == 0:
		return 0
	else:
		return x
	