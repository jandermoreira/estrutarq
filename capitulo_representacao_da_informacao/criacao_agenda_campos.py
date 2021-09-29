"""Criação de agenda simples

"""
from sys import argv

from estrutarq.campo import CampoBruto, CampoCadeiaFixo, \
    CampoCadeiaPrefixado, CampoCadeiaTerminador


def apresente_ajuda():
    """Uso do programa"""
    print(f"""Uso: {argv[0]} opção
    Opção:
        -b, --bruto:\tescrita sem organização de campo (campo bruto)
        -t, --terminador:\tescrita com uso de terminador de campo
        -p, --prefixo:\tescrita com campo prefixado pelo comprimento (1 byte)
        -f, --fixo:\tescrita com campos de comprimento0 fixo (20 bytes)
        -h, --help:\tapresenta esta ajuda 
    """)
    exit(1)


def main():
    # Tratamento das opções de linha de comando
    if len(argv) == 2:
        if argv[1] in ["-b", "--bruto"]:
            campo = CampoBruto()
        elif argv[1] in ["-t", "--terminador"]:
            campo = CampoCadeiaTerminador()
        elif argv[1] in ["-p", "--prefixo"]:
            campo = CampoCadeiaPrefixado()
        elif argv[1] in ["-f", "--fixo"]:
            campo = CampoCadeiaFixo(25)
        else:
            apresente_ajuda()
    else:
        apresente_ajuda()

    # Gravação da agenda a partir dos dado
    arquivo_agenda = open("agenda", "wb")
    fim_dos_dados = False
    while not fim_dos_dados:
        try:
            nome = input("Nome: ")
            email = input("E-mail: ")
            telefone = input("Telefone: ")
            mes_nascimento = input("Mês de nascimento: ")
            ano_nascimento = input("Ano de nascimento: ")
        except EOFError:
            fim_dos_dados = True
        else:
            campo.valor = nome
            campo.escreva(arquivo_agenda)
            campo.valor = email
            campo.escreva(arquivo_agenda)
            campo.valor = telefone
            campo.escreva(arquivo_agenda)
            campo.valor = mes_nascimento
            campo.escreva(arquivo_agenda)
            campo.valor = ano_nascimento
            campo.escreva(arquivo_agenda)
    arquivo_agenda.close()


if __name__ == "__main__":
    main()
