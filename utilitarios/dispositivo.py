"""Rotinas utilitárias gerais
"""
from os import fstat, remove
from tempfile import mkstemp


def comprimento_de_bloco(diretorio: str = None):
    """
    Determina o comprimento_bloco de um bloco do dispositivo externo, tendo como
    referência aquele onde está o diretório temporário do sistema (parãmetro
    igual a None); se um diretório em que haja direito de criação de arquivos
    for informado, então o dispostivo em que ele está será utilizado.
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
