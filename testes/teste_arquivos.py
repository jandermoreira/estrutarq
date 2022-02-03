from os import system

from estrutarq.arquivo import Arquivo


def main():
    arquivo = Arquivo("/tmp/arq.dat", novo = True)
    print(arquivo)
    arquivo.feche()
    system("hd /tmp/arq.dat")


if __name__ == '__main__':
    main()
