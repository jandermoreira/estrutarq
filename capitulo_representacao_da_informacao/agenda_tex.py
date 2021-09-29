"""Criação de 'tabular' para Latex

"""
def main():
    fim_dos_dados = False
    while not fim_dos_dados:
        try:
            nome = input()
            email = input()
            telefone = input()
            mes_nascimento = input()
            ano_nascimento = input()
        except EOFError:
            fim_dos_dados = True
        else:
            print(f"{nome} & {email} & {telefone} & "
            f"{mes_nascimento} & {ano_nascimento} \\\\")


if __name__ == "__main__":
    main()
