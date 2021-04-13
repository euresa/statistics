"""perumutation_test.py 
	This script simulates a permulation test for two hardcoded lists of numbers.
	Author: Sam Eure, Jan 13, 2021.
	Requires a Random and NumPy modules."""

from random import shuffle

A = [230, -1350, -1580, -400, -760]
B =  [970, 110, -50, -190, -200]
N = 1000 #The number of permutation samples. Larger -> more accurate result. 


AB = A + B
m = len(A)
n = len(B)

def mean(list1):
	return(sum(list1)/len(list1))

def mean_tester(sample1, sample2):
	E1 = mean(sample1)
	E2 = mean(sample2)
	return(abs(E1 - E2))

def median_tester(sample1, sample2):
	E1 = np.median(sample1)
	E2 = np.median(sample2)
	return(abs(E1 - E2))

t_obs = tester(A,B)

positives = 0.0
for i in range(N):
	shuffle(AB)
	new_A = AB[:m]
	new_B = AB[m:]
	new_test = mean_tester(new_A, new_B)
	if new_test > t_obs:
		positives = positives + 1



print("p-value:", positives/N)

