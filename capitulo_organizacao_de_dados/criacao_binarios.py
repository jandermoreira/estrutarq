"""   Criação de arquivos com valores binários
"""
from time import localtime, strftime
from estrutarq.campo import CampoDataBinario, CampoIntBinario, CampoRealBinario


def main():
    # Dados: inteiro, real, data
    hoje = strftime("%Y-%m-%d", localtime())
    dados = [
        (0, 3321.2, "1500-04-22"),
        (1234, -1.0005, "1997-08-29"),
        (-2000, 0, hoje)
    ]

    # Gravação do arquivo
    arquivo_dados = open("binarios", "wb")
    campo_inteiro = CampoIntBinario()
    campo_real = CampoRealBinario()
    campo_data = CampoDataBinario()
    for inteiro, real, data in dados:
        campo_inteiro.valor = inteiro
        campo_inteiro.escreva(arquivo_dados)
        campo_real.valor = real
        campo_real.escreva(arquivo_dados)
        campo_data.valor = data
        campo_data.escreva(arquivo_dados)
    arquivo_dados.close()


if __name__ == "__main__":
    main()
