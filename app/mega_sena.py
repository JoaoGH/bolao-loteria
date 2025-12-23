from app.loteria_base import LoteriaBase


class MegaSena(LoteriaBase):
    TABELA_PRECOS = {
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

    def __init__(self, numeros_da_sorte, qtd_dezenas=6):
        super().__init__(numeros_da_sorte, qtd_dezenas, max_numero_universo=60)

    def _validar_regras_especificas(self, n, jogo_atual):
        """
        Regras da Mega:
        1. Max 2 números na mesma dezena (linha).
        2. Max 2 números com mesmo final (coluna).
        """
        # Regra Dezena (Ex: 10, 14, 18 -> Bloqueia o terceiro)
        dezenas = [x // 10 for x in jogo_atual]
        if dezenas.count(n // 10) >= 2:
            return False

        # Regra Unidade (Ex: 01, 11, 21 -> Bloqueia o terceiro)
        unidades = [x % 10 for x in jogo_atual]
        if unidades.count(n % 10) >= 2:
            return False

        return True
