def main(k):
    
    # Criando os logs de melhor, media e populacao inicial
    best_log = []
    mean_log = []
    pop_ini_log = []
    
    for i in range(0, k):
    
        # Criando um vetor para guardar todos os melhores valores de fitness para cada geracao
        melhor_log = []

        # Criando um vetor para guardar a media dos valores de fitness para cada geracao
        media_log = []

        # Definindo o numero de geracoes ate que o algortimo pare de rodar
        nro_geracoes = 25

        # Definindo a probabilidade de haver cruzamento
        prob_cruz = 0.75

        # Definindo a probabilidade de haver mutacao
        prob_mut = 0.0001

        # Criando a populacao inicial
        pop, tam_pop = cria_pop_ini(i)
        
        # Adicionando o tamanho ao respectivo log
        pop_ini_log.append(tam_pop)
        
        # Definindo o tamanho da "chave" do torneio
        tam_torneio = round(len(pop)/20)

        # Comecando o algoritmo para todas as geracoes
        for j in range(0, nro_geracoes):
            
            # Calculando os valores de fitness para a populacao e sua media e minimo para log
            pop_fitness, melhor, media = calc_pop_fitness(pop) 

            # Adicionando os valores de maior e media aos respectivos logs
            melhor_log.append(melhor)
            media_log.append(media)

            # Adicionando clausula para evitar que sejam rodados na ultima geracao, para economizar processamento
            if j == nro_geracoes - 1:
                break
            
            # Rodando a funcao de selecao
            pop = k_way_tournament(pop, pop_fitness, tam_torneio, len(pop))
            
            # Rodando a funcao de cruzamento para cada dois numeros
            pop = uniform_crossover(pop, len(pop), prob_cruz)
            
            # Rodando a funcao de mutacao
            pop = mutacao(pop, len(pop), prob_mut)

        # Adicionando o melhor e media aos respectivos logs
        best_log.append(melhor_log)
        mean_log.append(media_log)
    
    return best_log, mean_log, pop_ini_log