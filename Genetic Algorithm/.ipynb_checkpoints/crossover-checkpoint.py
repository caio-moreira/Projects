# Definindo a funcao que so realizara o cruzamento
def cross(x, y, masc):
    
    # Criando cromossomos auxiliares que receberao o valores finais
    aux_x = ''
    aux_y = ''
    
    # Realizando o cruzamento
    for i, gene in enumerate(masc):
        
        # 'Trocando' os dois genes caso o gene da mascara seja '1'
        # No caso, se for '1', os genes serao adicionados no cromossomo auxiliar nao correspondente
        if gene == '1':
            aux_x += y[i]
            aux_y += x[i]
        else:
            aux_x += x[i]
            aux_y += y[i]
    
    # Retornando os cromossomos cruzados
    return aux_x, aux_y

# Definindo a funcao de cruzamento 
def uniform_crossover(pop, tam_pop, prob):
    
    # Criando o vetor que recebera a populacao final
    pop_cruz = []
    
    # Passando por todos os indices de 2 em 2, ja que sao selecionados cruzamentos de 2
    for i in range(0, tam_pop, 2):
        
        # Se o tamanho da populacao for impar, chegaremos ao ultimo elemento
        # No caso, o atual sera o ultimo, e como usamos o proximo elemento e o ultimo nao tem proximo, finalizamos clonando
        if i == tam_pop - 1:
            pop_cruz.append(pop[i])
            break
        
        # Rodando a probabilidade, caso seja negativo, maior que a fatia decidida, clonam-se os dois cromossomos
        # O comando 'continue' pula o resto do codigo e segue para a proxima iteracao do laco
        if randint(1, 100) > prob * 100:
            pop_cruz.append(pop[i])
            pop_cruz.append(pop[i + 1])
            continue
        
        # Definindo um cromossomo 'mascara' que recebera o valor retornado pela funcao que cria cromossomos randomicos
        # Este cromossomo sera binario (0 ou 1), onde for '1' ocorrera cruzamento 
        cromossomo_masc = gera_cromossomo()  

        # Chamando a funcao que realiza o cruzamento e salvando os resultados nas variaveis auxiliares
        crom1_aux, crom2_aux = cross(pop[i], pop[i + 1], cromossomo_masc)

        # Adicionando os dois cromossomos auxiliares ao vetor 'pop_cruz'
        pop_cruz.append(crom1_aux)
        pop_cruz.append(crom2_aux)

    # Retornando o vetor com a populacao final
    return pop_cruz 