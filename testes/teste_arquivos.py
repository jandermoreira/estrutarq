from os import system

from estrutarq.arquivo import ArquivoSimples
from estrutarq.campo import *
from estrutarq.registro import *

from random import sample, shuffle

nomes = ["jander", "jonatan", "jurandir", "zilda", "olivia", "elisa"]
sobrenomes = ["moreira", "caseli", "lima", "medeiros", "anversa"]
enderecos = ["passeio das palmeiras", "rua XV", "carlos botelho"]

dados = [[nome, sobrenome, endereco]
         for nome in nomes
         for sobrenome in sobrenomes
         for endereco in enderecos]


def teste(registro):
    arquivo = ArquivoSimples("/tmp/arq.dat", registro, novo = True)

    numero_registros = 2

    print("Escrevendo registros: ", end = "")
    contador = 0
    for nome, sobrenome, endereco in sample(dados, numero_registros):
        print(f"({contador})", end = "")
        registro.numero.valor = contador
        registro.nome.valor = nome
        registro.sobrenome.valor = sobrenome
        registro.endereco.valor = endereco
        arquivo.escreva(registro)
        contador += 1
    print()
    arquivo.feche()

    arquivo = ArquivoSimples("/tmp/arq.dat", registro)
    fim_de_arquivo = False
    print("Lendo registros sequencialmente: ", end = "")
    contador = 0
    while not fim_de_arquivo:
        try:
            registro = arquivo.leia()
        except EOFError:
            fim_de_arquivo = True
        else:
            print(f"({contador})", end = "")
            print(registro)
            contador += 1
        if contador > numero_registros + 1:
            print("Algo errado aqui...")
            exit(1)
    print()

    # print("Leituras aleatórias: ", end = "")
    # consultas = list(range(numero_registros))
    # shuffle(consultas)
    # for posicao in consultas:
    #     print(f"({posicao})", end = "")
    #     try:
    #         registro = arquivo.leia(posicao_relativa = posicao)
    #     except IOError as erro:
    #         print(erro)
    #         raise erro
    #     else:
    #         print("--------------\n", registro)
    arquivo.feche()

    print()
    # system("hd /tmp/arq.dat")


def main():
    lista_testes = [
        # RegistroFixo(
        #     50,
        #     ("numero", CampoIntBinario()),
        #     ("nome", CampoCadeiaTerminador()),
        #     ("sobrenome", CampoCadeiaPrefixado()),
        #     ("endereco", CampoCadeiaTerminador()),
        # ),
        RegistroTerminador(
            ("numero", CampoIntBinario()),
            ("nome", CampoCadeiaTerminador()),
            ("sobrenome", CampoCadeiaPrefixado()),
            ("endereco", CampoCadeiaTerminador()),
        ),
    ]
    for registro in lista_testes:
        teste(registro)


if __name__ == '__main__':
    main()
