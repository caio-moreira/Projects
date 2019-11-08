import utils
import crossover
import mutation
import tournament


def genetic_algorithm(k):
    """ Function that actually runs the Genetic Algorithm. 
  
    Keyword arguments: 
        k -- number of iterations to run the algorithm for 
  
    Returns: 
        best_log and avg_log -- Both contain k lists, each containing
            x integers, where x is the number of generations on that
            iteration, that represent the best and average fitness
            score for each generation, respectively
        pop_size_log -- List containing k integers, each being the
            size of the population on that iteration
    """
    
    best_log = []
    avg_log = []
    pop_size_log = []
    
    for iteration in range(0, k):
        # Lists that will hold the 
        gen_best_log = []
        gen_avg_log = []

        # Defining number of generations and probabilities
        gen_number = 25
        crossover_probability = 0.75
        mutation_probability = 0.0001

        # Starting population
        population, pop_size = utils.create_population(iteration)
        
        pop_size_log.append(pop_size)
        
        # Defining the size of the tournament's bracket
        # the k in k-way tournament
        tournament_bracket_size = round(pop_size/20)

        # Iterating through all generations
        for j in range(0, gen_number):
            
            # Calculating the fitness score for every
            # subject in the population and saving the
            # best and the average score
            pop_fitness, best, average = utils.calculate_pop_fitness(population) 

            gen_best_log.append(best)
            gen_avg_log.append(average)

            # Preventing the algorithm to go all the way through
            # during the last iteration, since that population
            # won't be recorded anyways
            if j == gen_number - 1:
                break
            
            # Calling the tournament, crossover and mutation function
            # and overwriting the current population with the new one
            population = tournament.k_way_tournament(population, pop_size, pop_fitness, tournament_bracket_size)
            population = crossover.uniform_crossover(population, pop_size, crossover_probability)
            population = mutation.mutation(population, mutation_probability)

        best_log.append(gen_best_log)
        avg_log.append(gen_avg_log)
    
    return best_log, avg_log, pop_size_log