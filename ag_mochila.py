import random
import numpy as np
from operator import itemgetter

#http://artemisa.unicauca.edu.co/~johnyortega/instances_01_KP/



def ler_instancia(arquivo):
    with open(arquivo) as arq:
        linhas = arq.readlines()
        instancia = {}
        instancia['numero_itens'] = int(linhas[0].split()[0])
        instancia['capacidade'] = int(linhas[0].split()[1])
        instancia['itens'] = []
        
        for linha in linhas[1:instancia['numero_itens']+1]:
            item = {}
            item['valor'] = int(linha.split()[0])
            item['peso'] = int(linha.split()[1])
            instancia['itens'].append(item)
        
    return instancia
   
def selecionar_individuos(populacao):
    populacao_ordenada = sorted(populacao, key=itemgetter('aptidao'), reverse=True)
    
    return populacao_ordenada[:SELECIONADOS]

def criar_individuo(representacao, instancia):
    individuo = {}
    individuo['representacao'] = representacao
    individuo['aptidao'] = grau_aptidao(individuo, instancia)
    
    return individuo

def reproduzir(populacao, ponto_corte, instancia):
    tamanho = int(len(populacao)/2)
    for i in range(tamanho):
        paiA = populacao[random.randint(0, tamanho - 1)]['representacao']
        paiB = populacao[random.randint(0, tamanho - 1)]['representacao']
        filhoA = paiA.copy()
        filhoB = paiB.copy()
        filhoA[ponto_corte:] = paiB[ponto_corte:]
        filhoB[ponto_corte:] = paiA[ponto_corte:]
        populacao.append(criar_individuo(filhoA, instancia))
        populacao.append(criar_individuo(filhoB, instancia))
    
    return populacao

def aplicar_mutacao(populacao, instancia):
    comprimento_cromossomo = instancia['numero_itens']
    individuos_mutantes = random.sample(range(len(populacao) - 1), MUTANTES)
    for individuo in individuos_mutantes:
        gene = random.randint(0, comprimento_cromossomo - 1)
        if populacao[individuo]['representacao'][gene] == 1: 
            populacao[individuo]['representacao'][gene] = 0
        else:
            populacao[individuo]['representacao'][gene] = 1
        populacao[individuo]['aptidao'] = grau_aptidao(populacao[individuo], instancia)
        
    return populacao
    
def gerar_populacao_inicial_aleatoria(instancia, tamanho_populacao):
    populacao = []
    tamanho_cromossomo = instancia['numero_itens']
    for _ in range(tamanho_populacao):
        representacao_aleatoria = np.random.choice([0,1], tamanho_cromossomo, p=[0.9, 0.1])
        individuo = criar_individuo(representacao_aleatoria, instancia)
        populacao.append(individuo)
    
    return populacao
 
def grau_aptidao(individuo, instancia):
    grau = 0
    for i, gene in enumerate(individuo['representacao']):
        grau = grau + (gene * instancia['itens'][i]['valor'])   

    return grau


def avaliar_solucao(solucao_otima, populacao, instancia):
    solucao_atual = populacao[0]['aptidao']
    viavel = solucao_viavel(populacao[0]['representacao'], instancia)
    if solucao_atual > solucao_otima and viavel:
        return solucao_atual
    
    return solucao_otima
        

def solucao_viavel(individuo, instancia):
    peso_total = 0
    for i, gene in enumerate(individuo):
        peso_total = peso_total + (gene * instancia['itens'][i]['peso'])   
        if peso_total > instancia['capacidade']:
            return False

    return True


''' Parâmetros do Algoritmo Genético '''
TAMANHO_POPULACAO = 10
NUMERO_GERACOES = 10
TAXA_SELECAO = 0.5
TAXA_MUTACAO = 0.05

SELECIONADOS = int(TAMANHO_POPULACAO * TAXA_SELECAO)
MUTANTES = int(TAMANHO_POPULACAO * TAXA_MUTACAO)


''' Programa Principal '''
def main():
    solucao_otima = -1
    instancia = ler_instancia(f"./instancias/f1_l-d_kp_10_269")
    comprimento_cromossomo = instancia['numero_itens']
    
    populacao = gerar_populacao_inicial_aleatoria(instancia, TAMANHO_POPULACAO)
    for geracao in range(NUMERO_GERACOES):
        ponto_corte = random.randint(0, comprimento_cromossomo - 1)
        individuos_selecionados = selecionar_individuos(populacao)
        solucao_otima = avaliar_solucao(solucao_otima, populacao, instancia)
        print(f"Geração {geracao+1} - Melhor solução: {solucao_otima}")
        populacao = reproduzir(individuos_selecionados, ponto_corte, instancia)
        populacao = aplicar_mutacao(populacao, instancia)




if __name__ == "__main__":
    main()
