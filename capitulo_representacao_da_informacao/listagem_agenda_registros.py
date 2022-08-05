"""
Criação de arquivo de dado com registros
"""

from estrutarq.campo import CampoCadeiaFixo, CampoCadeiaPrefixado, \
    CampoCadeiaTerminador, CampoIntTerminador, CampoRealBinario
from estrutarq.registro import RegistroPrefixado


def main():
    registro = RegistroPrefixado()
    registro.adicione_campos(
        CampoIntTerminador(),
        CampoCadeiaTerminador(),
        CampoRealBinario(),
        CampoCadeiaPrefixado(),
        CampoCadeiaFixo(16),
    )

    arquivo_agenda = open("agenda", "rb")
    fim_de_arquivo = False
    while not fim_de_arquivo:
        try:
            registro.leia(arquivo_agenda)
        except EOFError:
            fim_de_arquivo = True
        else:
            print(f"Código:   {registro.codigo}")
            print(f"Nome:     {registro.nome_completo}")
            print(f"Salário:  {registro.salario.valor:.2f} ")
            print(f"E-mail:   {registro.email}")
            print(f"Telefone: {registro.telefone}\n")
    arquivo_agenda.close()


if __name__ == "__main__":
    main()
