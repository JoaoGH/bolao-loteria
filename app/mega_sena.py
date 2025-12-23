import random


class MegaSena():

    def __init__(self, numeros_da_sorte, qtd_dezenas=6):
        if qtd_dezenas not in self.get_tabela_precos():
            raise ValueError(
                f"Quantidade de dezenas inválida. Escolha entre {min(self.get_tabela_precos().keys())} e {max(self.get_tabela_precos().keys())}.")

        self.numeros_da_sorte = sorted(numeros_da_sorte)
        self.qtd_dezenas = qtd_dezenas
        self.numeros_globais_usados = []

    def get_valor_aposta(self):
        return self.get_tabela_precos()[self.qtd_dezenas]

    def get_tabela_precos(self):
        return {
            6: 6,
            7: 42,
            8: 168,
            9: 504,
            10: 1260,
            11: 2772,
            12: 5544,
            13: 10296,
            14: 18018,
            15: 30030,
            16: 48048,
            17: 74256,
            18: 111384,
            19: 162792,
            20: 232560,
        }

    def simular_custos(self, total_pessoas):
        """
        Gera uma lista de opções de custos.
        Retorna uma lista de dicionários com as opções.
        """
        valor_unitario = self.get_valor_aposta()
        opcoes = []

        for qtd_jogos in range(1, total_pessoas + 1):
            valor_total = valor_unitario * qtd_jogos
            valor_pessoa = valor_total / total_pessoas

            opcoes.append({
                'id': qtd_jogos,
                'jogos': qtd_jogos,
                'total': valor_total,
                'por_pessoa': valor_pessoa,
                'divisao_exata': valor_pessoa.is_integer()
            })
        return opcoes

    def gerar_bolao(self, quantidade_jogos):
        """Gera a lista final de jogos aplicando as regras."""
        self.numeros_globais_usados = []

        jogos = self._distribuir_numeros_sorte(quantidade_jogos)

        jogos_completos = []
        for jogo in jogos:
            self._completar_jogo(jogo)
            jogos_completos.append(sorted(jogo))

        return jogos_completos

    def _distribuir_numeros_sorte(self, quantidade_jogos):
        jogos = [[] for _ in range(quantidade_jogos)]
        pool = self.numeros_da_sorte[:]
        random.shuffle(pool)

        idx = 0
        for numero in pool:
            if len(jogos[idx]) < self.qtd_dezenas and 1 <= numero <= 60:
                jogos[idx].append(numero)
                self.numeros_globais_usados.append(numero)

            idx += 1
            if idx >= quantidade_jogos:
                idx = 0
                random.shuffle(pool)
        return jogos

    def _completar_jogo(self, jogo):
        permite_sequencia = True
        tentativas_falhas = 0

        while len(jogo) < self.qtd_dezenas:
            ignorar_regras = tentativas_falhas > 50
            novo_numero = self._buscar_numero_valido(jogo, permite_sequencia, ignorar_regras)

            if novo_numero:
                jogo.append(novo_numero)
                self.numeros_globais_usados.append(novo_numero)

                if (novo_numero + 1 in jogo) or (novo_numero - 1 in jogo):
                    permite_sequencia = False
                tentativas_falhas = 0
            else:
                tentativas_falhas += 1
                if tentativas_falhas > 20: permite_sequencia = True

    def _buscar_numero_valido(self, jogo_atual, permite_sequencia, ignorar_regras=False):
        for _ in range(100):
            n = random.randint(1, 60)

            if n in jogo_atual: continue
            if ignorar_regras: return n

            if n in self.numeros_globais_usados: continue
            if [x // 10 for x in jogo_atual].count(n // 10) >= 2: continue
            if [x % 10 for x in jogo_atual].count(n % 10) >= 2: continue

            if not permite_sequencia:
                if (n + 1 in jogo_atual) or (n - 1 in jogo_atual): continue

            return n
        return None
