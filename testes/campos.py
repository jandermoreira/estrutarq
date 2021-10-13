"""
Testes para classes de dados
"""

from estrutarq.campo import *

from os import system


def imprima(msg, dado):
    print(f"> {msg}: {dado} / {type(dado).__name__}")


def compare(valor1, valor2):
    print(f"{valor1} == {valor2}?", end = "")
    if valor1 == valor2:
        print("  Sim")
    else:
        print("  Não")
        exit(1)


valor_campo = {
    "cadeia": "abcABC 123_312",
    "int": -98701,
    "real": 3.1415926,
    "tempo": "1700-12-25 11:22:33",
    "data": "2021-04-22",
    "hora": "17:57:44"
}

com_comprimento = [
    CampoCadeiaFixo, CampoIntFixo, CampoRealFixo,
]

sem_comprimento = [
    CampoCadeiaTerminador, CampoIntTerminador, CampoRealTerminador,
    CampoCadeiaPrefixado, CampoIntPrefixado, CampoRealPrefixado,
    CampoIntBinario, CampoRealBinario,
    CampoDataBinario, CampoDataFixo,
    CampoHoraBinario, CampoHoraFixo,
    CampoTempoBinario, CampoTempoFixo
]


def teste(tipo_campo):
    nome = tipo_campo.__name__
    print(f"Campo: {nome}")
    if tipo_campo in com_comprimento:
        campo = tipo_campo(25)
    else:
        campo = tipo_campo()
    imprima("valor padrão do campo", campo.valor)
    info = [valor_campo[k] for k in valor_campo.keys() if k in campo.tipo][0]
    imprima("dado em uso", info)
    campo.valor = info
    print(campo)
    dado = campo.valor_para_bytes()
    imprima("valor armazenado", campo.valor)
    imprima("valor em bytes", dado)
    dado_formatado = campo.adicione_formatacao(campo.valor_para_bytes())
    imprima("valor em bytes formatado", dado_formatado)
    dado_desformatado = campo.remova_formatacao(dado_formatado)
    imprima("valor removendo o formato", dado_desformatado)
    compare(dado, dado_desformatado)
    campo.bytes_para_valor(dado)
    compare(info, campo.valor)
    imprima("valor recuperado do dado", campo.valor)
    dado_estendido = dado_formatado + b"xyzXYZ=-+_()*&$#@!"
    with open("/tmp/campo.tmp", "wb") as arquivo:
        campo.escreva(arquivo)
    with open("/tmp/campo.tmp", "rb") as arquivo:
        campo.leia(arquivo)
    imprima("valor recuperado do arquivo 1", campo.valor)
    compare(info, campo.valor)
    system("hd /tmp/campo.tmp")
    with open("/tmp/campo.tmp", "wb") as arquivo:
        arquivo.write(dado_estendido)
    with open("/tmp/campo.tmp", "rb") as arquivo:
        campo.leia(arquivo)
    imprima("valor recuperado do arquivo 2", campo.valor)
    compare(info, campo.valor)
    system("hd /tmp/campo.tmp")
    # campo.valor = info
    campo.leia_de_bytes(dado_estendido)
    imprima("valor recuperado de sequência", campo.valor)
    compare(info, campo.valor)
    if tipo_campo in com_comprimento:
        campo = tipo_campo(20, valor = info)
    else:
        campo = tipo_campo(valor = info)
    imprima("valor atribuído no construtor", campo.valor)
    compare(info, campo.valor)
    print()


def main():
    for campo in sem_comprimento + com_comprimento:
        teste(campo)


if __name__ == "__main__":
    main()
