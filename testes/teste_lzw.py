#!/usr/bin/python3
"""
Teste da compressão LZW
"""

from sys import argv
from os import system

from estrutarq.compressao import LZWcompressor, LZWdescompressor

if len(argv) > 1:
    arquivo = argv[1]
else:
    arquivo = "gone_with_the_wind.txt"

with open(arquivo, "rb") as f:
    dados = f.read(1393)
comprimento_original = 8 * len(dados)

print(f"Comprimindo {comprimento_original} bits...", end = "")
compressor = LZWcompressor()
compressor.processe_de_bytes(dados)
compressor.feche()
comprimento_comprimido = len(compressor.fluxo)
print(" Terminado")

# Descompressão
print(f"Descomprimindo {comprimento_comprimido} bits...", end = "",
      flush = True)
descompressor = LZWdescompressor()
texto_recuperado = descompressor.recupere_de_fluxo(compressor.fluxo)
print(" Terminado")

print("\nDeu certo?", "sim" if dados == texto_recuperado else "não")
print(f"Original:   {comprimento_original:10d} bits")
print(f"Comprimido: {comprimento_comprimido:10d} bits")
taxa_compressao = (comprimento_original - comprimento_comprimido) / \
                  comprimento_original * 100
print(f"Taxa de compressão: {taxa_compressao:.3f}%")

with open("/tmp/saida", "wb") as f:
    f.write(texto_recuperado)
system(f"diff {arquivo} /tmp/saida > /dev/null && echo Ok")
