"""
Rotinas gerais de conversão de dados

..
    Licença: GNU GENERAL PUBLIC LICENSE V.3, 2007
    Jander Moreira, 2021, 2022
"""

import struct


# code::start cadeias_de_caracteres :: Conversão de cadeias de caracteres para bytes e vice-versa.
def cadeia_para_bytes(cadeia: str, conjunto: str = "utf8") -> bytes:
    """
    Conversão de cadeia de caracteres para sequência de bytes.

    :param cadeia: uma cadeia de caracteres
    :param conjunto: conjunto de caracteres usado na conversão (padrão: "utf8")
    :return: a sequência de bytes convertida
    """
    return bytes(cadeia, conjunto)


def bytes_para_cadeia(sequencia: bytes, conjunto: str = "utf8") -> str:
    """
    Conversão de sequência de bytes para cadeia de caracteres.

    :param sequencia: sequência de bytes
    :param conjunto: conjunto de caracteres usado na conversão (padrão: "uft8")
    :return: a cadeia de caracteres armazenada
    """
    return str(sequencia, conjunto)
    # code::end


# code::start inteiros :: Conversão de inteiros para bytes e vice-versa.
def inteiro_para_bytes(valor: int) -> bytes:
    """
    Conversão de inteiro para bytes, usando comprimento padrão de 4 bytes,
    ordenação *big endian* e complemento para 2 para valores negativos.

    :param valor: valor a ser convertido
    :return: a sequência de bytes
    """
    return struct.pack(">i", valor)


def bytes_para_inteiro(sequencia: bytes) -> int:
    """
    Conversão de sequência de 4 bytes com bit de sinal (complemento para 2) e
    com ordenação *big endian* para o valor inteiro correspondente.

    :param sequencia: sequência de 4 bytes
    :return: o valor inteiro armazenado
    """
    return struct.unpack(">i", sequencia)[0]
    # code::end


# code::start reais :: Conversão de reais para bytes e vice-versa.
def real_para_bytes(valor: int) -> bytes:
    """
    Conversão de real para bytes, usando padrão IEEE 754 de precisão dupla.

    :param valor: valor a ser convertido
    :return: a sequência de bytes
    """
    return struct.pack("d", valor)


def bytes_para_real(sequencia: bytes) -> int:
    """
    Conversão de bytes para real, usando padrão IEEE 754 de precisão dupla.

    :param sequencia: sequência de bytes
    :return: o valor real armazenado
    """
    return struct.unpack("d", sequencia)[0]
    # code::end


# code::start hexa :: Função de conversão de uma sequência de bytes para valores em hexadecimal.
def hexa(sequencia: bytes, separador: str = ":") -> str:
    """
    Converte uma sequência de bytes para uma cadeia de caracteres os bytes
    em hexadecimal.

    :param sequencia: valores dos bytes
    :param separador: texto que separa cada byte (padrão: ":")
    :return: cadeia em hexadecimal
    """
    return separador.join(f"{byte:02X}" for byte in sequencia)
# code::end
