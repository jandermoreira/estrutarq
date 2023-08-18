"""
Testes das rotinas de conversão
"""

from random import randint
from estrutarq.utilitarios.conversor import *

def verifique(condicao):
    if condicao:
        return "Ok"
    else:
        print("Erro")
        exit(1)

def cadeias_de_caracteres():
    """Testes de cadeias"""
    cadeias = [
        "simples",
        "longa com alguns caracteres",
        "com acentuação",
        "キャラクター",
        "персонажи",
    ]
    for cadeia in cadeias:
        em_bytes = cadeia_para_bytes(cadeia)
        em_str = bytes_para_cadeia(em_bytes)
        print(f"** '{cadeia}':")
        print(f"   {len(cadeia)} caracteres para {len(em_bytes)} bytes")
        print("   Conversão inversa:", verifique(em_str == cadeia))


def inteiros():
    """Testes de inteiros"""
    for valor in ([-10, 10, 255, 160000] +
                  [randint(-20000000, 220000000) for i in range(5)]):
        em_bytes = inteiro_para_bytes(valor)
        em_int = bytes_para_inteiro(em_bytes)
        print(f"** inteiro: {valor} --> {hexa(em_bytes)}")
        print(f"   Conversão para {len(em_bytes)} bytes")
        print("   Conversão inversa:", verifique(em_int == valor))

def reais():
    """Testes de reais"""
    for valor in [randint(-20000000, 220000000)/10000 for i in range(5)]:
        em_bytes = real_para_bytes(valor)
        em_real = bytes_para_real(em_bytes)
        print(f"** real: {valor} --> {hexa(em_bytes)}")
        print(f"   Conversão para {len(em_bytes)} bytes")
        print("   Conversão inversa:", verifique(em_real== valor))

def main():
    """Principal"""
    # cadeias_de_caracteres()
    # inteiros()
    reais()

if __name__ == "__main__":
    main()
