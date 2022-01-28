#
# Teste com registros
#

from os import system
from random import randint, sample

from estrutarq.campo import *
from estrutarq.registro import *

lista_campos = [
    ("fix", "nome", CampoCadeiaFixo, "Jander"),
    ("var", "sobrenome", CampoCadeiaPrefixado, "Moreira"),
    ("var", "apelido", CampoCadeiaTerminador, "olieli"),
    ("var", "data1", CampoDataBinario, "1967-01-24"),
    ("xxx", "data2", CampoDataFixo, "1967-01-20"),
    ("var", "hora1", CampoHoraBinario, "00:12:13"),
    ("xxx", "hora2", CampoHoraFixo, "11:12:13"),
    ("var", "int1", CampoIntBinario, 1238),
    ("fix", "int2", CampoIntFixo, 1236),
    ("var", "int3", CampoIntPrefixado, 1230),
    ("var", "int4", CampoIntTerminador, 1231),
    ("var", "real1", CampoRealBinario, 123.2),
    ("fix", "real2", CampoRealFixo, 123.3),
    ("var", "real3", CampoRealPrefixado, 123.5),
    ("var", "real4", CampoRealTerminador, 123.6),
    ("var", "tempo1", CampoTempoBinario, "2000-01-24 11:12:13"),
    ("xxx", "tempo2", CampoTempoFixo, "1900-01-24 11:12:13"),
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
        registro = tipo_registro(300, ("rrn", CampoIntBinario(valor = 0)))
        registro_base = tipo_registro(300, ("rrn", CampoIntBinario(valor = -1)))
    else:
        registro = tipo_registro(("rrn", CampoIntBinario(valor = 0)))
        registro_base = tipo_registro(("rrn", CampoIntBinario(valor = -1)))
    campos = sample(lista_campos, randint(15, len(lista_campos)))
    for tipo_comprimento, nome, campo, valor in campos:
        if tipo_comprimento == "fix":
            registro.adicione_campos((nome, campo(20, valor = valor)))
            registro_base.adicione_campos((nome, campo(20)))
        else:
            registro.adicione_campos((nome, campo(valor = valor)))
            registro_base.adicione_campos((nome, campo()))
    return registro, registro_base


def main():
    numero_registros = 1000

    print("Criando /tmp/dados com", numero_registros, "registros")
    arquivo = open("/tmp/dados", "wb")
    dados = []
    for i in range(numero_registros):
        reg, reg_base = crie_registro()
        dados.append(reg_base.copy())  # salva estrutura de cada registro

        reg.rnn.valor = i
        reg.escreva(arquivo)
    arquivo.close()

    arquivo = open("/tmp/dados", "rb")
    arquivo_ref = open("/tmp/dados_ref", "wb")
    for dado in enumerate(dados):
        dado.leia(arquivo)
        dado.escreva(arquivo_ref)
    arquivo.close()
    arquivo_ref.close()

    diff = "diff /tmp/dados /tmp/dados_ref && echo Iguais || echo Diferentes"
    print(diff)
    system(diff)

    # for dado, dado_base in dados:
    #     print("********************************************")
    #     print(dado)
    #     print("--------------------------------------------")
    #     print(dado_base)
    #     print("********************************************")
    #     print()
    #     # input("ENTER... ")


if __name__ == "__main__":
    main()
