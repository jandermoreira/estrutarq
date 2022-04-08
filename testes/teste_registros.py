#
# Teste com registros
#

from os import remove, system
from sys import stdout
from random import randint, sample

from estrutarq.campo import *
from estrutarq.registro import *

lista_campos = [
    ("fix", "nome", CampoCadeiaFixo, "Jander"),
    ("var", "sobrenome", CampoCadeiaPrefixado, "Moreira"),
    ("var", "apelido", CampoCadeiaTerminador, "olieli"),
    ("var", "data1", CampoDataBinario, "1967-01-24"),
    ("-", "data2", CampoDataFixo, "1967-01-20"),
    ("var", "hora1", CampoHoraBinario, "00:12:13"),
    ("-", "hora2", CampoHoraFixo, "11:12:13"),
    ("-", "int1", CampoIntBinario, 1238),
    ("fix", "int2", CampoIntFixo, 1236),
    ("var", "int3", CampoIntPrefixado, 1230),
    ("var", "int4", CampoIntTerminador, 1231),
    ("var", "real1", CampoRealBinario, 123.2),
    ("fix", "real2", CampoRealFixo, 123.3),
    ("var", "real3", CampoRealPrefixado, 123.5),
    ("var", "real4", CampoRealTerminador, 123.6),
    ("var", "tempo1", CampoTempoBinario, "2000-01-24 11:12:13"),
    ("-", "tempo2", CampoTempoFixo, "1900-01-24 11:12:13"),
]

lista_registros = [
    ("fix", RegistroFixo),
    ("var", RegistroPrefixado),
    ("var", RegistroBruto),
    ("var", RegistroTerminador),
]


def crie_registro():
    tipo_comprimento, tipo_registro = sample(lista_registros, 1)[0]
    if tipo_comprimento == "fix":
        registro = tipo_registro(300)
        registro_base = tipo_registro(300)
    else:
        registro = tipo_registro()
        registro_base = tipo_registro()
    campos = sample(lista_campos, randint(15, len(lista_campos)))
    for tipo_comprimento, nome, campo, valor in campos:
        # print(tipo_comprimento, nome, campo, valor)
        if tipo_comprimento == "fix":
            registro.adicione_campos((nome, campo(20, valor = valor)))
            registro_base.adicione_campos((nome, campo(20)))
        else:
            registro.adicione_campos((nome, campo(valor = valor)))
            registro_base.adicione_campos((nome, campo()))
        # print("ok")

    registro.adicione_campos(("rrn", CampoIntBinario(valor = 0)))
    registro_base.adicione_campos(("rrn", CampoIntBinario(valor = -1)))
    return registro, registro_base


# def mainx():
#     from os import system
#     arquivo = open("/tmp/dados", "wb")
#     registro = RegistroTerminador(
#         ("campo", CampoCadeiaTerminador())
#     )
#     registro.campo.valor = "abacate \x00 berinjela, ébano"
#     registro.escreva(arquivo)
#     arquivo.close()
#     system("hd /tmp/dados")
#     arquivo = open("/tmp/dados", "rb")
#     registro.leia(arquivo)
#     print("***\n", registro)
#     arquivo.close()


def main():
    numero_registros = 10000

    print("Criando /tmp/dados com", numero_registros, "registros")
    arquivo = open("/tmp/dados", "wb")
    dados = []
    for i in range(numero_registros):
        if i % 5 == 0:
            print(f"\r{100 * i / numero_registros:.1f}%", end = "",
                  flush = True)
            stdout.flush()

        reg, reg_base = crie_registro()
        dados.append(reg_base.copia())  # salva estrutura de cada registro

        reg.rrn.valor = i
        # print("**************\n", reg)
        reg.escreva(arquivo)
        # print(type(reg), reg.comprimento(), reg.tem_comprimento_fixo())
    print("\r100%      ")
    arquivo.close()

    print("Copiando dados para novo arquivo /tmp/dados_ref")
    arquivo = open("/tmp/dados", "rb")
    arquivo_ref = open("/tmp/dados_ref", "wb")
    for i, dado in enumerate(dados):
        if i % 5 == 0:
            print(f"\r{100 * i / numero_registros:.1f}%", end = "",
                  flush = True)
            stdout.flush()

        dado.leia(arquivo)
        if dado.rrn.valor != i:
            print(f"\nErro na numeração: {dado.rrn.valor} != {i}.")
            print(dado)
            print(type(dado.rrn.valor))
            exit()
        dado.escreva(arquivo_ref)
    print("\r100%     ")
    arquivo.close()
    arquivo_ref.close()

    diff = "diff /tmp/dados /tmp/dados_ref && echo Iguais || echo Diferentes"
    print(diff)
    system(diff)
    print()
    # system("hd /tmp/dados | less")

    remove("/tmp/dados")
    remove("/tmp/dados_ref")


if __name__ == "__main__":
    main()
