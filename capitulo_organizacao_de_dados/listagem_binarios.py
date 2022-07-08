"""Listagem de arquivo com campos binários.

O arquivo foi criado por uma sequência que intercala um inteiro, um real e
uma data, todos armazenados em forma binária. A listagem pega cada trio de
campos e apresenta seus valores na tela, até achar o fim do arquivo.
"""

from estrutarq.campo import CampoDataBinario, CampoIntBinario, CampoRealBinario


def main():
    arquivo_dados = open("binarios", "rb")
    fim_de_arquivo = False
    campo_inteiro = CampoIntBinario()
    campo_real = CampoRealBinario()
    campo_data = CampoDataBinario()
    while not fim_de_arquivo:
        try:
            campo_inteiro.leia(arquivo_dados)
            campo_real.leia(arquivo_dados)
            campo_data.leia(arquivo_dados)
        except EOFError:
            fim_de_arquivo = True
        else:
            print(campo_inteiro.valor)
            print(campo_real.valor)
            print(campo_data.valor)
    arquivo_dados.close()


if __name__ == "__main__":
    main()
