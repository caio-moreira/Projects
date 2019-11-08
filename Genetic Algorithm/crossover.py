from random import randint
import utils


def cross(chrom_1, chrom_2, mask):
    """ Function that runs the crossover.

    For any given pair of chromosomes there's a random mask
    and the crossover will happen between the two of them where
    there's a number 1 in the mask.

    All 3 of them (chrom_1, chrom_2 and mask) must have
    the same size.

    e.g. chrom_1 = '10101', chrom_2 = '01010', mask = '01010'
    results will be '11111' and '00000'
  
    Keyword arguments: 
        chrom_1 -- chromosome 1 
        chrom_2 -- chromosome 2
        mask -- random chromosome to run the crossover
  
    Returns: 
        chrom_1_after_cross -- chromosome 1 after crossing over
        chrom_2_after_cross -- chromosome 2 after crossing over
    """

    chrom_1_after_cross = ''
    chrom_2_after_cross = ''
    
    for i, gene in enumerate(mask):
        if gene == '1':
            chrom_1_after_cross += chrom_2[i]
            chrom_2_after_cross += chrom_1[i]
        else:
            chrom_1_after_cross += chrom_1[i]
            chrom_2_after_cross += chrom_2[i]
    
    return chrom_1_after_cross, chrom_2_after_cross

def uniform_crossover(population, pop_size, probability=0.75):
    """ Function that checks for crossover and calls for it. 
  
    Keyword arguments: 
        population -- current chromosome population 
        pop_size -- size of the population
        probability -- probability of any two chromosomes to undergo
            uniform crossover (default 0.75)
  
    Returns: 
        pop_after_crossover -- population after crossing over
    """
    
    pop_after_crossover = []
    
    # Iterating through every pair of chromosomes
    for i in range(0, pop_size, 2):
        
        # If the population size is an odd number
        # this snippet sets the crossover to happen
        # between the last two chromosomes
        # yes, in this scenario the second to last
        # might undergo crossover twice
        # but it's first crossover will be ignored,
        # since it will be removed from the final list
        if i == pop_size - 1:
            pop_after_crossover.pop()
            i -= 1
        
        # Checking if the odds are against crossing over
        # if they are, continuing to next iteration
        # after appending the current pair of chromosomes
        # untouched
        if randint(1, 100) > probability * 100:
            pop_after_crossover.append(population[i])
            pop_after_crossover.append(population[i + 1])

            continue
        
        # Generating a mask for the uniform crossover 
        chromosome_mask = utils.new_chromosome(len(population[i]))  

        chrom_1, chrom_2 = cross(population[i], population[i + 1], chromosome_mask)

        pop_after_crossover.append(chrom_1)
        pop_after_crossover.append(chrom_2)

    # Retornando o vetor com a populacao final
    return pop_after_crossover