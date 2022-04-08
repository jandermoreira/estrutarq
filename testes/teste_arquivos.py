from os import system
from time import process_time
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


def igual(valor1, valor2):
    if valor1 != valor2:
        print("**", valor1, "!=", valor2)
        exit(1)


def teste(registro):
    print(registro.tipo)
    arquivo = ArquivoSimples("/tmp/arq-teste.dat", registro, novo = True)

    numero_registros = 500
    while len(dados) < numero_registros:
        dados.extend(dados)
    print(len(dados))

    print("Escrevendo registros: ", end = "")
    contador = 0
    for nome, sobrenome, endereco in sample(dados, numero_registros):
        registro.numero.valor = contador
        registro.nome.valor = nome
        registro.sobrenome.valor = sobrenome
        registro.endereco.valor = endereco
        # print(f"({contador}, {registro.numero})", end = "")
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
            # print(f"({contador}, {registro.numero})", end = "")
            igual(contador, registro.numero.valor)
            contador += 1
        if contador > numero_registros + 1:
            print("Algo errado aqui com o número de leituras...")
            exit(1)
    print()

    print("Leituras aleatórias: ", end = "")
    inicio = process_time()
    consultas = list(range(numero_registros))
    shuffle(consultas)
    for posicao in consultas:
        try:
            registro = arquivo.leia(posicao_relativa = posicao)
        except IOError as erro:
            print(erro)
            raise IOError("Fora do intervalo")
        else:
            # print(f"({posicao}, {registro.numero})", end = "")
            igual(posicao, registro.numero.valor)
    fim = process_time()
    arquivo.feche()

    print()

    return f"Tempo para registro {registro.tipo}: " + \
           f"{(fim - inicio):.3f} segundos\n"
    # system("hd /tmp/arq.dat")


def main():
    lista_testes = [
        RegistroFixo(
            500,
            ("numero", CampoIntBinario()),
            ("nome", CampoCadeiaTerminador()),
            ("sobrenome", CampoCadeiaPrefixado()),
            ("endereco", CampoCadeiaTerminador()),
        ),
        # RegistroBruto(
        #     ("numero", CampoIntBinario()),
        #     ("nome", CampoCadeiaFixo(12)),
        #     ("sobrenome", CampoCadeiaTerminador()),
        #     ("endereco", CampoCadeiaTerminador()),
        # ),
        # RegistroTerminador(
        #     ("numero", CampoIntBinario()),
        #     ("nome", CampoCadeiaTerminador()),
        #     ("sobrenome", CampoCadeiaPrefixado()),
        #     ("endereco", CampoCadeiaPrefixado()),
        # ),
        # RegistroPrefixado(
        #     ("numero", CampoIntBinario()),
        #     ("nome", CampoCadeiaFixo(12)),
        #     ("sobrenome", CampoCadeiaTerminador()),
        #     ("endereco", CampoCadeiaTerminador()),
        # ),
    ]
    msg = ""
    for registro in lista_testes:
        msg += teste(registro)
    print(msg)


if __name__ == '__main__':
    main()
