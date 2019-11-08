from random import randint


def mutate(chromosome, gene_index):
    """ Function that mutates the gene. 
  
    Keyword arguments: 
        chromosome -- the current chromosome
        gene_index -- position of the mutant-to-be gene
  
    Returns: 
        mutant -- chromosome after mutation
    """

    # Storing the value of the mutant-to-be gene
    gene = int(chromosome[gene_index])

    # Calculating new value for the gene
    new_gene = str(abs(gene - 1))
    
    # Mutating
    mutant = (
        chromosome[:gene_index]
        + new_gene
        + chromosome[gene_index+1:]
    )

    return mutant

# Definindo a funcao de mutacao
def mutation(population, probability=0.000001):
    """ Function that checks for mutation and calls for it. 
  
    Keyword arguments: 
        population -- the current population of chromosomes
        probability -- probability of any gene of a chromosome to
            undergo mutation (default 0.000001)
  
    Returns: 
        pop_after_mutation -- population after mutations
    """

    pop_after_mutation = []
    
    for chromosome in population:
        # Iterating through every gene in a chromosome
        for gene_index in range(len(chromosome)):
            if randint(1, 100000000) <= probability * 100000000:
                chromosome = mutate(chromosome, gene_index)

        # Appending new chromosome, mutant or not
        pop_after_mutation.append(chromosome)

    return pop_after_mutation