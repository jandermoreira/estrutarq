from os import system

from estrutarq.arquivo import ArquivoSimplesFixo


def main():
    arquivo = ArquivoSimplesFixo("/tmp/arq.dat", 10)
    print(arquivo.nome_arquivo)
    arquivo.feche()
    system("hd /tmp/arq.dat")


if __name__ == '__main__':
    main()
