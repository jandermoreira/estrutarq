"""
Teste do fluxo de bytes
"""

from random import randint

from bitarray import bitarray

from utilitarios.fluxo import Fluxo


def main():
    fluxo = Fluxo()
    print(0, fluxo)

    for n in range(20):
        fluxo.adicione_bits(bitarray(str(randint(0, 0))))
        print(n + 1, fluxo, len(fluxo))

    for n in range(20):
        bit = fluxo.obtenha_bits(1)
        print(bit, fluxo)

if __name__ == '__main__':
    main()
