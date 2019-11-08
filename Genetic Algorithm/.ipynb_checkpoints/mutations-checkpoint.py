# Definindo a funcao que realiza a mutacao
def realiza_mutacao(cromossomo, gene):

    # Criando o cromossomo auxiliar para realizar a mutacao
    crom_aux = ''

    # Adicionando a parte anterior ao gene mutante ao cromossomo auxiliar
    crom_aux += cromossomo[:gene]

    # Adicionando o gene mutante com a troca ja feita
    crom_aux += str(abs(int(cromossomo[gene]) - 1))
    
    # Adicionando o restante do cromossomo inicial ao auxiliar
    crom_aux += cromossomo[gene + 1:]
    
    # Retornando o cromossomo mutante
    return crom_aux

# Definindo a funcao de mutacao
def mutacao(pop, tam_pop, prob):
    
    # Criando o vetor que recebera a populacao final
    pop_muta = []
    
    # Rodando a probabilidade para todos os cromossomos da populacao
    for cromossomo in pop:
            
        # Criando o cromossomo auxiliar como copia do atual
        crom_aux = cromossomo
      
        # Rodando a probabilidade para todos os genes de um dado cromossomo
        for index_gene, gene in enumerate(cromossomo):
          
            if randint(1, 1000000) <= prob * 1000000:
            
                # Mutando o gene
                crom_aux = realiza_mutacao(crom_aux, index_gene)

        # Adicionando o cromossomo auxiliar na populacao
        pop_muta.append(crom_aux)
        
    # Retornando a populacao mutada
    return pop_muta