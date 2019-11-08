# Definindo a funcao que gera os indixes que vao participar do torneio
def get_tournament_indexes(tam_torneio, tam_pop):
    
    # Criando o array que recebera os indices
    participantes = []
    
    # Gerando os indices
    for i in range(0, tam_torneio):
        participantes.append(randint(0, tam_pop - 1))
        
    # Retornando o vetor final
    return participantes

# Definindo a funcao que realiza o torneio
def k_way_tournament(pop, fitness, tam_torneio, tam_pop):
    
    # Definindo o vetor que ira receber os vencedores de cada torneio
    selecionados = []
    
    # Rodando o torneio 'x' vezes, onde 'x' e o tamanho da população
    # Para que se obtenha uma nova populcao do mesmo tamanho da inicial
    for i in range(0, tam_pop):
        
        # Rodando a funcao que seleciona 'y' inteiros representando os indices a participar do torneio
        participantes = get_tournament_indexes(tam_torneio, tam_pop)
        
        # Criando o array que vai guardar os valores de fitness dos participantes
        fitness_part = []
        
        # Selecionando os valores de fitness dos participantes
        for j in participantes:
            fitness_part.append(fitness[j])
            
        # Pegando o menor valor de fitxness do torneio, ja que queremos minimizar o valor da funcao de fitness
        min_val = min(fitness_part)
        
        # Pegando o indice do maior do torneio no vetor de fitness da populacao
        vencedor = fitness.index(min_val)
        
        # Adicionando o cromossomo vencedor ao vetor 'selecionados'
        selecionados.append(pop[vencedor])
        
    return selecionados