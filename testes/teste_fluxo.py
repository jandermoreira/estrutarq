"""
Teste do fluxo de bytes
"""

from random import randint

from bitarray import bitarray

from utilitarios.fluxo import Fluxo


def apresente_bytes(sequencia: bytes):
    """
    Torna os bytes "bonitos"
    :param sequencia: os bytes
    """
    return ":".join([f"{v:02X}" for v in sequencia])


def main():
    fluxo = Fluxo()

    # TESTE
    print("Teste: inserção bit a bit")
    bits_teste = bitarray(20)
    for bit in bits_teste.tolist():
        fluxo.adicione_bits(bitarray(str(bit)))
    print(bits_teste)

    bits_recuperados = bitarray()
    while len(fluxo) > 0:
        bits_recuperados += fluxo.obtenha_bits(1)
    print(bits_recuperados)

    if bits_recuperados == bits_teste:
        print("Ok")
    else:
        print("Erro")

    # TESTE
    print("Teste: inserção de sequências de comprimentos diferentes")
    fluxo.limpe()
    bits_teste = bitarray()
    for n in range(10):
        bits = bitarray(randint(1, 5))
        fluxo.adicione_bits(bits)
        bits_teste += bits
    print(bits_teste)

    bits_recuperados = bitarray()
    while len(fluxo) > 0:
        bits_recuperados += fluxo.obtenha_bits(randint(0, 4))
    print(bits_recuperados)

    if bits_recuperados == bits_teste:
        print("Ok")
    else:
        print("Erro")

    # TESTE
    print("Teste: remoção de bytes")
    fluxo.limpe()
    bits_teste = bitarray(60)
    fluxo.adicione_bits(bits_teste)
    print(bits_teste, fluxo)
    fluxo_teste = str(fluxo)[1:-2]

    fim = False
    bytes_recuperados = b""
    while not fim:
        byte = fluxo.obtenha_bytes(randint(1, 4))
        print(apresente_bytes(byte), fluxo)
        fim = len(byte) == 0
        bytes_recuperados += byte

    if fluxo_teste == apresente_bytes(bytes_recuperados) + str(fluxo)[1:-2]:
        print("Ok")
    else:
        print("Erro")


if __name__ == '__main__':
    main()
