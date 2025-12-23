from app.loteria_base import LoteriaBase


class Lotofacil(LoteriaBase):
    TABELA_PRECOS = {
        15: 3.5,
        16: 56,
        17: 476,
        18: 2856,
        19: 13566,
        20: 54264,
    }

    def __init__(self, numeros_da_sorte, qtd_dezenas=15):
        super().__init__(numeros_da_sorte, qtd_dezenas, max_numero_universo=25)

    @property
    def usar_filtro_global(self):
        """
        Sobrescreve para False.
        Na Lotofácil (15 de 25), se fizermos 2 jogos já usaríamos 30 números.
        É matematicamente impossível não repetir números entre jogos.
        """
        return False

    def _validar_regras_especificas(self, n, jogo_atual):
        """
        Regras da Lotofácil:
        Como o espaço é apertado (15 em 25), as regras são mais soltas.
        Podemos limitar para não encher demais uma linha só (ex: 1,2,3,4,5).
        """
        # Na lotofácil, as linhas são 1-5, 6-10, 11-15...
        # Uma "dezena" aqui é complexa, vamos simplificar verificando linhas do volante
        # Linha 1 (1-5), Linha 2 (6-10), etc.

        linha_atual = (n - 1) // 5
        numeros_na_mesma_linha = [x for x in jogo_atual if (x - 1) // 5 == linha_atual]

        # Evita preencher a linha inteira (5 números), tenta manter max 4
        # Mas permite se o jogo estiver quase acabando para não travar
        if len(numeros_na_mesma_linha) >= 4:
            # Só bloqueia estritamente se tivermos espaço sobrando no jogo
            if len(jogo_atual) < 12:
                return False

        return True