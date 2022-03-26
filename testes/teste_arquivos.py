from os import system

from estrutarq.arquivo import ArquivoSimplesFixo
from estrutarq.campo import *
from estrutarq.registro import *

from random import sample

nomes = ["jander", "jonatan", "jurandir", "zilda", "olivia", "elisa"]
sobrenomes = ["moreira", "caseli", "lima", "medeiros", "anversa"]
enderecos = ["passeio das palmeiras", "rua XV", "carlos botelho"]

dados = [[nome, sobrenome, endereco]
         for nome in nomes
         for sobrenome in sobrenomes
         for endereco in enderecos]


def main():
    registro = RegistroFixo(50,
        ("nome", CampoCadeiaTerminador()),
        ("sobrenome", CampoCadeiaPrefixado()),
        ("endereco", CampoCadeiaTerminador()),
    )
    arquivo = ArquivoSimplesFixo("/tmp/arq.dat", registro, novo = True)

    numero_registros = 30
    for nome, sobrenome, endereco in sample(dados, numero_registros):
        registro.nome.valor = nome
        registro.sobrenome.valor = sobrenome
        registro.endereco.valor = endereco
        arquivo.escreva(registro)
    arquivo.feche()

    # registro.adicione_campos(("rnn", CampoIntBinario()))
    arquivo = ArquivoSimplesFixo("/tmp/arq.dat", registro)
    fim_de_arquivo = False
    while not fim_de_arquivo:
        try:
            registro = arquivo.leia()
        except EOFError:
            fim_de_arquivo = True
        else:
            print("-----------------")
            print(registro)
    arquivo.feche()

    print()
    system("hd /tmp/arq.dat")


if __name__ == '__main__':
    main()
