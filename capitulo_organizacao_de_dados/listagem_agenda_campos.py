#!/usr/bin/python3
#   Listagem de uma agenda simples, usando terminador


from sys import argv

from estrutarq.campo import CampoCadeiaFixo, CampoCadeiaPrefixado, \
    CampoCadeiaTerminador


def apresente_ajuda():
    """Uso do programa"""
    print(f"""Uso: {argv[0]} opção
    Opção:
        -t, --terminador:\tlistagem de campos com terminador
        -p, --prefixo:\tlistagem de campos prefixados pelo comprimento (1 byte)
        -f, --fixo:\tlistagem de campos de comprimento fixo (20 bytes)
    """)
    exit(1)


def main():
    # Tratamento das opções de linha de comando
    if len(argv) == 2:
        if argv[1] in ["-t", "--terminador"]:
            campo = CampoCadeiaTerminador()
        elif argv[1] in ["-p", "--prefixo"]:
            campo = CampoCadeiaPrefixado()
        elif argv[1] in ["-f", "--fixo"]:
            campo = CampoCadeiaFixo(25)
        else:
            apresente_ajuda()
    else:
        apresente_ajuda()

    # Listagem de todos os campos do arquivo
    arquivo_agenda = open("agenda", "rb")
    fim_de_arquivo = False
    while not fim_de_arquivo:
        try:
            campo.leia(arquivo_agenda)
        except EOFError:
            fim_de_arquivo = True
        else:
            print(campo.valor)
    arquivo_agenda.close()


if __name__ == "__main__":
    main()
