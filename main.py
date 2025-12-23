from app.mega_sena import MegaSena


def main():
    NUMEROS_SELECIONADOS = [13, 6, 37, 27, 17, 31, 58, 41, 28, 10, 45, 2]
    NUMEROS_SELECIONADOS.sort()

    print(f"Números da sorte base: {NUMEROS_SELECIONADOS}\n")

    try:
        qtd_pessoas = int(input("Total de pessoas: "))
        qtd_dezenas = int(input("Quantas dezenas jogar: "))
        megasena = MegaSena(NUMEROS_SELECIONADOS, qtd_dezenas)

        opcoes = megasena.simular_custos(qtd_pessoas)

        print(f"\n--- OPÇÕES DE BOLÃO ({qtd_dezenas} dezenas) ---")
        for i, op in enumerate(opcoes):
            indicado = " <--- RECOMENDADO" if op['divisao_exata'] else ""
            print(f"Opcao {i + 1:02d} {indicado}")
            print(f"Fazendo {op['jogos']} jogo(s) de {qtd_dezenas} DEZENAS sai por R$ {op['total']:.2f} no total.")
            print("Valor por pessoa: R$ " + f"{op['por_pessoa']: .2f}")
            print("------------------------------------\n")

        escolha = int(input("\nDigite o número da Opção desejada: "))

        if escolha <= 1 or escolha >= len(opcoes):
            raise ValueError("Opção inválida.")

        opcao_selecionada = opcoes[escolha - 1]
        qtd_jogos = opcao_selecionada['jogos']
        print(f"\nGerando {qtd_jogos} jogos...")
        jogos_gerados = megasena.gerar_bolao(qtd_jogos)

        print("\n" + "=" * 40)
        print(f"   JOGOS GERADOS ({qtd_dezenas} Dezenas)")
        print("=" * 40)

        for i, jogo in enumerate(jogos_gerados):
            jogo_formatado = ", ".join(f"{n:02d}" for n in jogo)
            print(f"Jogo {i + 1:02d}: [{jogo_formatado}]")

        print("-" * 40)
        print(f"Custo Total: R$ {opcao_selecionada['total']:.2f}")
        print(f"Por Pessoa:  R$ {opcao_selecionada['por_pessoa']:.2f}")
        print("=" * 40)

    except ValueError as e:
        print(f"\nErro de valor: {e}")
    except Exception as e:
        print(f"\nErro inesperado: {e}")


if __name__ == '__main__':
    main()
