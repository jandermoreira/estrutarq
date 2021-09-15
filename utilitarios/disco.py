"""Rotinas utilitárias gerais
"""
from os import fstat, remove
from tempfile import mkstemp


def comprimento_de_bloco(diretorio: str = None):
    descritor, nome_arquivo = mkstemp(dir = diretorio)
    comprimento = fstat(descritor).st_blksize
    remove(nome_arquivo)
    return comprimento


# def main():
#     print(f"Tamanho do bloco: {comprimento_de_bloco()}")
#
# if __name__ == "__main__":
#     main()