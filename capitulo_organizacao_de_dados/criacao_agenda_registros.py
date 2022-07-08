"""
Criação de arquivo de dado com registros
"""

from estrutarq.campo import CampoCadeiaFixo, CampoCadeiaPrefixado, \
    CampoCadeiaTerminador, CampoIntTerminador, CampoRealBinario
from estrutarq.registro import RegistroPrefixado


def main():
    registro = RegistroPrefixado(
        CampoIntTerminador(),
        CampoCadeiaTerminador(),
        CampoRealBinario(),
        CampoCadeiaPrefixado(),
        CampoCadeiaFixo(16),
    )

    arquivo_agenda = open("agenda", "wb")
    fim_dos_dados = False
    codigo = 1
    while not fim_dos_dados:
        try:
            registro.codigo.valor = codigo  # código sequencial
            codigo += 1
            registro.nome_completo.valor = input("Nome: ")
            registro.salario.valor = float(input("Salário: "))
            registro.email.valor = input("E-mail: ")
            registro.telefone.valor = input("Telefone: ")
        except EOFError:
            fim_dos_dados = True
        else:
            registro.escreva(arquivo_agenda)

    arquivo_agenda.close()


if __name__ == "__main__":
    main()
