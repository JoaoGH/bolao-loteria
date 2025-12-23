import random
import os
from collections import Counter

NUMEROS_SELECIONADOS = [13, 6, 37, 27, 17, 31, 58, 41, 28, 10, 45, 2]
NUMEROS_SELECIONADOS.sort()
TOTAL_DEZENAS_JOGO = 7
VALOR_JOGO = 35
MAX_REPETIDOS = 0
total_repetidos = 0
numeros_globais = []

def select_total_jogos(total_pessoas):
    opcoes = []
    for i, it in enumerate(range(1, total_pessoas)):
        valor = VALOR_JOGO * it
        valor_pessoa = valor / total_pessoas
        indicado = (" - INDICADO " if valor_pessoa.is_integer() else "")
        print("\nOpcao {} {}".format(i+1, indicado))
        print("------------------------------------")
        print("Fazendo {} jogos de 7 DEZENAS sai por R$ {} no total.".format(it, f"{valor: .2f}"))
        print("Valor por pessoa: R$ " + f"{valor_pessoa: .2f}")
        print("------------------------------------")
        opcoes.append([it, valor, valor_pessoa])
    
    print('\n')
    opc = int(input("Seleciona opção e jogo: "))
    
    return opcoes[opc - 1]

def criar_jogos(total_jogos, numeros_jogados):
    for _ in range(0,total_jogos):
        random.shuffle(numeros_jogados)
    
    tamanho_grupo = len(numeros_jogados) // total_jogos
    resto = len(numeros_jogados) % total_jogos

    jogos = []
    inicio = 0
    for i in range(total_jogos):
        fim = inicio + tamanho_grupo + (1 if i < resto else 0)
        jogos.append(numeros_jogados[inicio:fim])
        inicio = fim

    for jogo in jogos:
        #print(jogo)
        completa_jogo(jogo)
        #jogo.sort()
        #print(jogo)
        numeros_globais.sort()
        #print(numeros_globais)
        #print('-')

    return jogos

def completa_jogo(jogo):
    permite_sequencia = True

    while len(jogo) < TOTAL_DEZENAS_JOGO:
        numero_randomico = get_novo_numero(jogo, permite_sequencia)
        
        if numero_randomico + 1 in jogo or numero_randomico - 1 in jogo:
            permite_sequencia = False
        
        jogo.append(numero_randomico)

    numeros_globais.extend(jogo)

    return jogo

def get_novo_numero(numeros_jogados, permite_sequencia):    
    while True:
        n = random.randint(1, 60)
        for _ in range(10):
            n = random.randint(1, 60)
        
        if n in NUMEROS_SELECIONADOS:
            continue

        if n in numeros_jogados:
            continue
        
        if n in numeros_globais:
            continue

        mesma_dezena_count = sum(1 for x in numeros_jogados if x // 10 == n // 10)
        if mesma_dezena_count > 1:
            continue

        mesma_unidade = Counter(x % 10 for x in numeros_jogados)[n%10]
        if mesma_unidade > 1:
            continue

        if permite_sequencia == False and (n + 1 in numeros_jogados or n - 1 in numeros_jogados):
            continue

        return n

pessoas = int(input("Total de pessoas: "))
total_jogos, valor_total, valor = select_total_jogos(pessoas)

MAX_REPETIDOS = total_jogos

os.system('cls')

print("Total de jogos feitos: {}".format(total_jogos))
print("Total de pessoas jogando: {}".format(pessoas))
print("Numeros pre selecionados: {}".format(NUMEROS_SELECIONADOS))
print("Valor total: R$ {}".format(f"{valor_total: .2f}"))
print("Valor por pessoa: R$ {}".format(f"{valor: .2f}"))

numeros_jogados = []
jogos = criar_jogos(total_jogos, NUMEROS_SELECIONADOS)
print('\nJogos:')
for i, jogo in enumerate(jogos):
    jogo.sort()
    numeros_jogados.extend(jogo)
    print("Jogo {}: {}".format(i + 1, jogo))