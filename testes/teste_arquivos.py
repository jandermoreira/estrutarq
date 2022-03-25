from os import system

from estrutarq.arquivo import ArquivoSimplesFixo
from estrutarq.campo import CampoCadeiaTerminador


def main():
    arquivo = ArquivoSimplesFixo("/tmp/arq.dat", 10, novo = True)
    print(arquivo.nome_arquivo)
    campo = CampoCadeiaTerminador(valor = "123")

    campo.escreva(arquivo.arquivo)
    arquivo.feche()
    system("hd /tmp/arq.dat")


if __name__ == '__main__':
    main()
