from os import system

from estrutarq.arquivo import ArquivoSimplesFixo
from estrutarq.campo import CampoCadeiaTerminador

def main():
    arquivo = ArquivoSimplesFixo("/tmp/arq.dat", 10)
    print(arquivo.nome_arquivo)
    campo = CampoCadeiaTerminador()
    campo.valor = "Jander"
    campo.escreva(arquivo.arquivo)
    arquivo.feche()
    system("hd /tmp/arq.dat")


if __name__ == '__main__':
    main()
