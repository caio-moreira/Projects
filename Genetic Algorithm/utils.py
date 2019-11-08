import math
from random import randint
from statistics import mean


def new_chromosome(size=20):
    """ Function that creates a new chromosome.

    Generates a string containing a binary chromossome.

    e.g. '101110101001' 
  
    Keyword arguments: 
        size -- size of the chromossome to be generated (default 20) 
  
    Returns: 
        chromosome -- the chromosome generated
    """

    chromosome = ''
    
    while len(chromosome) < size:
        # Odds of having a 0 or a 1 must be the same
        if randint(1, 10) < 6:
            chromosome += '0'
        else:
            chromosome += '1'

    return chromosome

def create_population(iteration):
    """ Function that creates a new population.

    Generates a list containing x chromossomes.

    In this scenario we start the population at 500 subjects,
    then it's iteratively increased by 100 using the iteration
    variable, which is passed on by as an argument.
  
    Keyword arguments: 
        iteration -- current iteration of the algorithm 
  
    Returns: 
        population -- the population generated
        pop_size -- the size of the population generated
    """

    # Settting population size accordingly 
    pop_size = 500 + (iteration * 100)

    population = []

    while len(population) < pop_size:
        chromossome = new_chromosome()
        
        population.append(chromossome)

    return population, pop_size

def get_x_y_values(chromosome):
    """ Function that gets x and y for the chromosome.

    Since each chromosome has a default size of 20, this is the
    number used to explain.

    The both halves of the chromosome are binary numbers, this
    funtion get both and turns them into the respective integer.

    After that, they are multiplied by a conversion factor to put
    both the numbers in the interval between 0 and 10, including
    both ends. Then they are subtracted from 5, moving the interval
    to the one between -5 and 5, also inclusive to both ends.

    The conversion factor is a number calculated as x/y where
        x -- maximum of the interval
        y -- maximum number that can be created with either half
                of the chromosome, being a half 10 units in lenght
                the max number is 11 1111 1111, or 1023, and that
                is represented, as in the code, by (2 ** 10) - 1.
  
    Keyword arguments: 
        chromosome -- chromosome that will have values calculated  
  
    Returns: 
        x_value -- the population generated
        y_value -- the size of the population generated
    """
    
    # The index of the chromosome's half
    # also the number to be used in the conversion factor
    half = int(len(chromosome)/2)

    # Calculating conversion factor as explained above 
    conversion_factor = 10/((2 ** half) -1)
    
    # Calculating integer value from binary
    # then following the steps as explained
    x_integer = int(chromosome[:half], 2)
    y_integer = int(chromosome[half:], 2)
    
    # Converting integers to [0, 10]
    x_converted = x_integer * conversion_factor
    y_converted = y_integer * conversion_factor
    
    # Shifting interval to [-5, 5]
    x_value = x_converted - 5
    y_value = y_converted - 5

    return x_value, y_value

def fitness(x, y):
    """ Function that calculates the fitness score.

    It is an implementation of the two-dimensional Rastrigin's function.

    The ultimate goal of the algorithm is to minimize the value of
    this function.

    It returns the fitness score of the chromosome
  
    Keyword arguments: 
        x -- the value of the x part of the chromosome
        y -- the value of the y part of the chromosome
    """

    return 20 + (x ** 2) + (y ** 2) - 10 * (math.cos(2 * math.pi * x) + math.cos(2 * math.pi * y))

def calculate_pop_fitness(population):
    """ Function that calcualtes fitness score for every subject of
    a population.

    Generates a list containing the fitness score of each member of
    the population.

    Since the fitness function is trying to be minimized,
    returns the minimum (best) fitness score for logging purposes.
    Also returns the average of all the fitness scores for logging
    purposes.
  
    Keyword arguments: 
        population -- current population of chromosomes 
  
    Returns: 
        pop_fitness -- fitness score for every subject of the population
        min(pop_fitness) -- minimum fitness score (the best of them)
        mean(pop_fitness) -- average fitness score
    """

    pop_fitness = []

    for chromosome in population:
        x, y = get_x_y_values(chromosome)
        
        pop_fitness.append(fitness(x, y))
    
    return pop_fitness, min(pop_fitness), mean(pop_fitness)
