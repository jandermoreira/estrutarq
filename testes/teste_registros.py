#
# Teste com registros
#

from random import randint, sample

from estrutarq.campo import *
from estrutarq.registro import *

lista_campos = [
    (CadeiaFixo, "Jander"),
    (CadeiaPrefixado, "Moreira"),
    (CadeiaTerminador, "olieli"),
    (CampoDataBinario, "1967-01-24"),
    (CampoDataFixo, "1967-01-24"),
    (CampoHoraBinario, "11:12:13"),
    (CampoHoraFixo, "11:12:13"),
    (CampoIntBinario, 123),
    (CampoIntFixo, 123),
    (CampoIntPrefixado, 123),
    (CampoIntTerminador, 123),
    (CampoRealBinario, 123.3),
    (CampoRealFixo, 123.3),
    (CampoRealPrefixado, 123.3),
    (CampoRealTerminador, 123.3),
    (CampoTempoBinario, "1967-01-24 11:12:13"),
    (CampoTempoFixo, "1967-01-24 11:12:13"),
]

def main():
    arquivo = open("/tmp/dados", "rb")

    registros = RegistroFixo(300)
    campos = sample(lista_campos, randint(4, 8))
    print(campos)




if __name__ == "__main__":
    main()