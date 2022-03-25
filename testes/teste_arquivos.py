from os import system

from estrutarq.arquivo import ArquivoSimplesFixo
from estrutarq.campo import CampoCadeiaTerminador
from estrutarq.registro import RegistroFixo


def main():
    registro = RegistroFixo(0x60,
                            ("nome", CampoCadeiaTerminador(valor = "AB")),
                            ("sobrenome", CampoCadeiaTerminador()),
                            ("endereco", CampoCadeiaTerminador()),
                            )
    arquivo = ArquivoSimplesFixo("/tmp/arq.dat", registro, novo = True)
    registro.nome.valor = "Jander"
    registro.sobrenome.valor = "Moreira"
    registro.endereco.valor = "Passeio das Palmeiras"
    print(registro.nome)

    registro.escreva(arquivo.arquivo)
    arquivo.feche()
    system("hd /tmp/arq.dat")


if __name__ == '__main__':
    main()
