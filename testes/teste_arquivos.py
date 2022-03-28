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
    arquivo = ArquivoSimples("/tmp/arq-teste.dat", registro, novo = True)

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

    # system("ls -l /tmp/arq-teste.dat")
    # system("hd /tmp/arq-teste.dat")

    arquivo = ArquivoSimples("/tmp/arq-teste.dat", registro)
    fim_de_arquivo = False
    print("Lendo registros sequencialmente: ", end = "")
    contador = 0
    while not fim_de_arquivo:
        # print("p", arquivo.arquivo.tell())
        try:
            registro = arquivo.leia()
        except EOFError:
            fim_de_arquivo = True
        else:
            print(f"({contador})", end = "")
            print(registro)
            contador += 1
        if contador > numero_registros + 1:
            print("Algo errado aqui com o número de leituras...")
            exit(1)
    print()

    print("Leituras aleatórias: ", end = "")
    consultas = list(range(numero_registros))
    shuffle(consultas)
    for posicao in consultas:
        try:
            registro = arquivo.leia(posicao_relativa = posicao)
        except IOError as erro:
            print(erro)
            raise IOError("Fora do intervalo")
        else:
            print(f"({posicao})", end = "")
            print("--------------\n", registro)
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
