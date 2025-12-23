import random
from abc import ABC, abstractmethod


class LoteriaBase(ABC):

    def __init__(self, numeros_da_sorte, qtd_dezenas, max_numero_universo):
        """
        :param numeros_da_sorte: Lista de números selecionados arbitrariamente.
        :param qtd_dezenas: Quantos números serão jogados.
        :param max_numero_universo: Maior número possível.
        """
        self.numeros_da_sorte = sorted(numeros_da_sorte)
        self.qtd_dezenas = qtd_dezenas
        self.max_numero = max_numero_universo
        self.numeros_globais_usados = [] # histórico do bolão

    @property
    @abstractmethod
    def TABELA_PRECOS(self):
        """Cada tipo de jogo deve definir a tabela de preços por quantidade de números jogados"""
        pass

    @property
    def usar_filtro_global(self):
        """
        Define se deve tentar evitar repetir números entre jogos diferentes do mesmo bolão
        Padrão: True.
        """
        return True

    def get_valor_aposta(self):
        if self.qtd_dezenas not in self.TABELA_PRECOS:
            raise ValueError(f"Qtd de dezenas inválida para este jogo. Opções: {list(self.TABELA_PRECOS.keys())}")
        return self.TABELA_PRECOS[self.qtd_dezenas]

    def simular_custos(self, total_pessoas):
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
        self.numeros_globais_usados = []
        jogos = self._distribuir_numeros_sorte(quantidade_jogos)

        jogos_completos = []
        for jogo in jogos:
            self._completar_jogo(jogo)
            jogos_completos.append(sorted(jogo))
        return jogos_completos

    def _distribuir_numeros_sorte(self, quantidade_jogos):
        jogos = [[] for _ in range(quantidade_jogos)]

        # Filtra números da sorte que não cabem no universo (ex: num 58 na Lotofacil)
        pool = [n for n in self.numeros_da_sorte if n <= self.max_numero]

        # Se não tiver números válidos, retorna vazio para preencher aleatório depois
        if not pool: return jogos

        random.shuffle(pool)
        idx = 0
        for numero in pool:
            if len(jogos[idx]) < self.qtd_dezenas:
                jogos[idx].append(numero)
                if self.usar_filtro_global:
                    self.numeros_globais_usados.append(numero)

            idx += 1
            if idx >= quantidade_jogos:
                idx = 0
                random.shuffle(pool)
        return jogos

    def _completar_jogo(self, jogo):
        permite_sequencia = True
        tentativas = 0

        while len(jogo) < self.qtd_dezenas:
            ignorar_regras = tentativas > 50  # Mecanismo de segurança

            # Busca número candidato
            candidato = self._buscar_candidato(jogo, permite_sequencia, ignorar_regras)

            if candidato:
                jogo.append(candidato)
                if self.usar_filtro_global:
                    self.numeros_globais_usados.append(candidato)

                # Regra básica de sequência (1, 2, 3...)
                if (candidato + 1 in jogo) or (candidato - 1 in jogo):
                    permite_sequencia = False
                tentativas = 0
            else:
                tentativas += 1
                if tentativas > 20:
                    permite_sequencia = True  # Relaxa regra de sequência

    def _buscar_candidato(self, jogo_atual, permite_sequencia, ignorar_regras):
        for _ in range(100):
            n = random.randint(1, self.max_numero)

            # Verificações obrigatórias (não podem ser ignoradas)
            if n in jogo_atual: continue

            if ignorar_regras: return n

            # Regra Global (Evitar repetir números que já saíram em OUTROS jogos)
            if self.usar_filtro_global and n in self.numeros_globais_usados:
                continue

            # Regra de Sequência Simples
            if not permite_sequencia:
                if (n + 1 in jogo_atual) or (n - 1 in jogo_atual): continue

            # Regras Específicas da Criança (Mega ou Lotofacil)
            if not self._validar_regras_especificas(n, jogo_atual):
                continue

            return n
        return None

    @abstractmethod
    def _validar_regras_especificas(self, numero, jogo_atual):
        """Método que as filhas devem implementar com suas regras estatísticas."""
        pass