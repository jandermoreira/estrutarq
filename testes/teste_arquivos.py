from os import system

from estrutarq.arquivo import ArquivoSimplesFixo
from estrutarq.campo import CampoCadeiaTerminador
from estrutarq.registro import RegistroFixo


def main():
    registro = RegistroFixo(60,
                            ("nome", CampoCadeiaTerminador()),
                            ("sobrenome", CampoCadeiaTerminador()),
                            ("endereco", CampoCadeiaTerminador()),
                            )
    arquivo = ArquivoSimplesFixo("/tmp/arq.dat", registro, novo = True)
    registro.nome.valor = "Jan\x00der"
    registro.sobrenome.valor = "Mo\xfereira"
    registro.endereco.valor = "Passeio das\x1bPalmeiras"
    arquivo.escreva(registro)
    arquivo.feche()

    arquivo = ArquivoSimplesFixo("/tmp/arq.dat", registro)
    registro = arquivo.leia()
    arquivo.feche()
    print(registro)

    system("hd /tmp/arq.dat")


if __name__ == '__main__':
    main()
