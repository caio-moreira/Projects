from random import randint


def get_tournament_indexes(bracket_size, pop_size):
    """ Function that randomly selects the indexes to be on the tournament. 
  
    Keyword arguments: 
        bracket_size -- size of the tournament bracket,
            the number of contestants
        pop_size -- size of the population
  
    Returns: 
        contestants -- indexes of the contestants
    """

    contestants = []

    while len(contestants) < bracket_size:
        contestants.append(randint(0, pop_size - 1))

    return contestants

# Definindo a funcao que realiza o torneio
def k_way_tournament(population, pop_size, pop_fitness, bracket_size):
    """ Function that returns the a new population of winners.

    The new population has the same size of the old one, so there
    are pop_size tournaments, each winner will be appended to the
    new population. 

    For each iteration of the tournament it's selected k indexes to
    participate, k being equal to bracket_size, then the best among
    those indexes is selected to the new population.

    Since we are trying to minimize the fitness function, we select
    the contestant with the lowest fitness score.
  
    Keyword arguments: 
        population -- current population of chromossomes
        pop_size -- size of the population
        pop_fitness -- fitness scores for every member of
            the current population
        bracket_size -- size of the tournament bracket,
            the number of contestants
  
    Returns: 
        pop_after_tournaments -- population made up of the winner
        of each tournament
    """
    
    pop_after_tournaments = []
    
    while len(pop_after_tournaments) < pop_size:
        
        contestants = get_tournament_indexes(bracket_size, pop_size)
        
        # Array that will store the fitness score of the contestants
        contestant_fitness = []
        
        # Getting the fitness score for each contestant
        for contestant in contestants:
            contestant_fitness.append(pop_fitness[contestant])

        # Selecting the fitness score that 'wins' (the lowest)
        winner_fitness = min(contestant_fitness)
        
        # Selecting the contestant index of the winner score
        winner_contestant_index = contestant_fitness.index(winner_fitness)

        # Selecting winner index
        winner_index = contestants[winner_contestant_index]
        
        # Appending the winner to the new population
        pop_after_tournaments.append(population[winner_index])
        
    return pop_after_tournaments