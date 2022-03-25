"""Rotinas utilitárias gerais
"""
from os import fstat, remove
from tempfile import mkstemp


def comprimento_de_bloco(diretorio: str = None):
    """
    Determina o comprimento_bloco de um bloco de disco, tendo como referência
    o disco onde está o diretório temporário do sistema; para outro
    disco, é preciso informar um diretório nesse disco em que haja direito
    de criação de arquivos.
    :param diretorio: um diretório no disco a ser verificado
    :return: o tamanho do bloco no disco

    Efeitos colaterais: é criado um arquivo temporário, que em seguida
    é removido.
    """
    descritor, nome_arquivo = mkstemp(dir = diretorio)
    comprimento = fstat(descritor).st_blksize
    remove(nome_arquivo)
    return comprimento


def main():
    print(f"Tamanho do bloco: {comprimento_de_bloco()}")

if __name__ == "__main__":
    main()