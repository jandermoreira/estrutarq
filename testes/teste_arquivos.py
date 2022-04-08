from random import sample, shuffle
from time import process_time

from estrutarq.arquivo import ArquivoSimples
from estrutarq.campo import *
from estrutarq.registro import *

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


def teste(registro_teste):
    relatorio = "\n*** " + registro_teste.tipo + '\n'
    print(registro_teste.tipo)
    arquivo = ArquivoSimples("/tmp/arq-teste.dat", registro_teste, novo = True)

    numero_registros = 500
    while len(dados) < numero_registros:
        dados.extend(dados)
    print(len(dados))

    print("Escrevendo registros: ", end = "")
    contador = 0
    inicio = process_time()
    for nome, sobrenome, endereco in sample(dados, numero_registros):
        registro_teste.numero.valor = contador
        registro_teste.nome.valor = nome
        registro_teste.sobrenome.valor = sobrenome
        registro_teste.endereco.valor = endereco
        # print(".", end = "")
        # print(f"({contador}, {registro_teste.numero})", end = "")
        arquivo.escreva(registro_teste)
        contador += 1
    fim = process_time()
    print()
    arquivo.feche()
    relatorio += f"Criado em {(fim - inicio):.3f} segundos\n"

    # system("ls -l /tmp/arq-teste.dat")
    # system("hd /tmp/arq-teste.dat")

    arquivo = ArquivoSimples("/tmp/arq-teste.dat", registro_teste)
    fim_de_arquivo = False
    print("Lendo registros sequencialmente: ", end = "")
    contador = 0
    inicio = process_time()
    while not fim_de_arquivo:
        # print("p", arquivo.arquivo.tell())
        try:
            registro_teste = arquivo.leia()
        except EOFError:
            fim_de_arquivo = True
        else:
            # print(".", end = "")
            # print(f"({contador}, {registro_teste.numero})", end = "")
            igual(contador, registro_teste.numero.valor)
            contador += 1
        if contador > numero_registros + 1:
            print("Algo errado aqui com o número de leituras...")
            exit(1)
    fim = process_time()
    print()
    relatorio += f"Acesso sequencial em {(fim - inicio):.3f} segundos\n"

    print("Leituras aleatórias: ", end = "")
    inicio = process_time()
    consultas = list(range(numero_registros))
    shuffle(consultas)
    for posicao in consultas:
        try:
            registro_teste = arquivo.leia(posicao_relativa = posicao)
        except IOError as erro:
            print(erro)
            raise IOError("Fora do intervalo")
        else:
            # print(f"({posicao}, {registro_teste.numero})", end = "")
            # print(".", end = "")
            igual(posicao, registro_teste.numero.valor)
    fim = process_time()
    arquivo.feche()
    relatorio += f"Acesso aleatório em {(fim - inicio):.3f} segundos\n"

    print()
    return relatorio

    # system("hd /tmp/arq.dat")


def main():
    lista_testes = [
        RegistroFixo(
            60,
            ("numero", CampoIntBinario()),
            ("nome", CampoCadeiaTerminador()),
            ("sobrenome", CampoCadeiaPrefixado()),
            ("endereco", CampoCadeiaTerminador()),
        ),
        RegistroBruto(
            ("numero", CampoIntBinario()),
            ("nome", CampoCadeiaFixo(12)),
            ("sobrenome", CampoCadeiaTerminador()),
            ("endereco", CampoCadeiaTerminador()),
        ),
        RegistroTerminador(
            ("numero", CampoIntBinario()),
            ("nome", CampoCadeiaTerminador()),
            ("sobrenome", CampoCadeiaPrefixado()),
            ("endereco", CampoCadeiaPrefixado()),
        ),
        RegistroPrefixado(
            ("numero", CampoIntBinario()),
            ("nome", CampoCadeiaFixo(12)),
            ("sobrenome", CampoCadeiaTerminador()),
            ("endereco", CampoCadeiaTerminador()),
        ),
    ]
    msg = ""
    for registro in lista_testes:
        msg += teste(registro)
    print(msg)


if __name__ == '__main__':
    main()
