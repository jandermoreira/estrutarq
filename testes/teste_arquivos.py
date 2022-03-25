from os import system

from estrutarq.arquivo import ArquivoSimplesFixo
from estrutarq.campo import CampoCadeiaTerminador
from estrutarq.registro import RegistroFixo


def main():
    registro = RegistroFixo(0x60,
                            ("nome", CampoCadeiaTerminador()),
                            ("sobrenome", CampoCadeiaTerminador()),
                            ("endereco", CampoCadeiaTerminador()),
                            )
    arquivo = ArquivoSimplesFixo("/tmp/arq.dat", registro, novo = True)
    registro.nome = "Jander"
    registro.sobrenome = "Moreira"
    registro.endereco = "Passeio das Palmeiras"
    print(registro.nome)

    registro.escreva(arquivo.arquivo)
    arquivo.feche()
    system("hd /tmp/arq.dat")


if __name__ == '__main__':
    main()
