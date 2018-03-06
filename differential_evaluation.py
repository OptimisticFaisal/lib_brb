# ------------------------------------------------------------------------------+
#
#   Nathan A. Rooy
#   A simple, bare bones, implementation of differential evolution with Python
#   August, 2017
#
# ------------------------------------------------------------------------------+

# --- IMPORT DEPENDENCIES ------------------------------------------------------+

import random


# --- EXAMPLE COST FUNCTIONS ---------------------------------------------------+

def func1(x):
	# Sphere function, use any bounds, f(0,...,0)=0
	return sum([x[i] ** 2 for i in range(len(x))])


def func2(x):
	# Beale's function, use bounds=[(-4.5, 4.5),(-4.5, 4.5)], f(3,0.5)=0.
	term1 = (1.500 - x[0] + x[0] * x[1]) ** 2
	term2 = (2.250 - x[0] + x[0] * x[1] ** 2) ** 2
	term3 = (2.625 - x[0] + x[0] * x[1] ** 3) ** 2
	return term1 + term2 + term3
# --- FUNCTIONS ----------------------------------------------------------------+

def ensure_bounds(vec, bounds):
	vec_new = []
	# cycle through each variable in vector
	for i in range(len(vec)):

		# variable exceedes the minimum boundary
		if vec[i] < bounds[i][0]:
			vec_new.append(bounds[i][0])

		# variable exceedes the maximum boundary
		if vec[i] > bounds[i][1]:
			vec_new.append(bounds[i][1])

		# the variable is fine
		if bounds[i][0] <= vec[i] <= bounds[i][1]:
			vec_new.append(vec[i])

	return vec_new
def parameter_correction(vec, bounds):
	corrected_parameter_vector = []
	for i in range(len(vec)):
		if bounds[i][0]<=vec[i]<=bounds[i][1]:
			corrected_parameter_vector.append(vec[i])
		else:
			temp = vec[i]+mutate*(bounds[i][0]+bounds[i][1])
			temp = temp/(2*mutate+1)
			corrected_parameter_vector.append(vec[i])
	return corrected_parameter_vector


# --- MAIN ---------------------------------------------------------------------+

def main(cost_func, bounds, popsize, mutate, recombination, maxiter):
	# --- INITIALIZE A POPULATION (step #1) ----------------+

	population = []
	for i in range(0, popsize):
		indv = []
		for j in range(len(bounds)):
			temp = bounds[j][0]+(bounds[j][1]-bounds[j][0])*random.uniform(bounds[j][0],bounds[j][1])
			indv.append(temp)
			# indv.append(random.uniform(bounds[j][0], bounds[j][1]))
		population.append(indv)

	# --- SOLVE --------------------------------------------+

	# cycle through each generation (step #2)
	for i in range(1, maxiter + 1):
		print('GENERATION:', i)


		gen_scores = []  # score keeping

		# cycle through each individual in the population
		for j in range(0, popsize):

			# --- MUTATION (step #3.A) ---------------------+

			# select three random vector index positions [0, popsize), not including current vector (j)
			canidates = range(0, popsize)
			canidates.remove(j)
			random_index = random.sample(canidates, 3)

			x_1 = population[random_index[0]]
			x_2 = population[random_index[1]]
			x_3 = population[random_index[2]]
			x_t = population[j]  # target individual

			# subtract x3 from x2, and create a new vector (x_diff)
			x_diff = [x_2_i - x_3_i for x_2_i, x_3_i in zip(x_2, x_3)]

			# multiply x_diff by the mutation factor (F) and add to x_1
			v_donor = [x_1_i + mutate * x_diff_i for x_1_i, x_diff_i in zip(x_1, x_diff)]
			# v_donor = ensure_bounds(v_donor, bounds)

			# --- RECOMBINATION (step #3.B) ----------------+

			v_trial = []
			for k in range(len(x_t)):
				crossover = random.random()
				if crossover <= recombination:
					v_trial.append(v_donor[k])

				else:
					v_trial.append(x_t[k])
			# v_trial = ensure_bounds(v_trial,bounds)
			v_trial = parameter_correction(v_trial,bounds)

			# --- GREEDY SELECTION (step #3.C) -------------+

			score_trial = cost_func(v_trial)
			score_target = cost_func(x_t)

			if score_trial < score_target:
				population[j] = v_trial
				gen_scores.append(score_trial)
				print('   >', score_trial, v_trial)


			else:
				print('   >', score_target, x_t)

				gen_scores.append(score_target)

		# --- SCORE KEEPING --------------------------------+

		gen_avg = sum(gen_scores) / popsize  # current generation avg. fitness
		gen_best = min(gen_scores)  # fitness of best individual
		gen_sol = population[gen_scores.index(min(gen_scores))]  # solution of best individual

		print('      > GENERATION AVERAGE:', gen_avg)

		print('      > GENERATION BEST:', gen_best)

		print('         > BEST SOLUTION:', gen_sol, '\n')


	return gen_sol


# --- CONSTANTS ----------------------------------------------------------------+

cost_func = func1  # Cost function
bounds = [(-1, 1), (-1, 1)]  # Bounds [(x1_min, x1_max), (x2_min, x2_max),...]
popsize = 10  # Population size, must be >= 4
mutate = 0.5  # Mutation factor [0,2]
recombination = 0.7  # Recombination rate [0,1]
maxiter = 20  # Max number of generations (maxiter)

# --- RUN ----------------------------------------------------------------------+

main(cost_func, bounds, popsize, mutate, recombination, maxiter)

# --- END ----------------------------------------------------------------------+