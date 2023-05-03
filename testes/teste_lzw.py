#!/usr/bin/python3
"""
Teste da compressão LZW
"""

from os import system
from sys import argv

from estrutarq.compressao import LZWcompressor, LZWdescompressor

if len(argv) > 1:
    arquivo = argv[1]
else:
    arquivo = "quincas_borba.txt"

with open(arquivo, "rb") as f:
    dados = f.read()
comprimento_original = 8 * len(dados)

print(f"Comprimindo {comprimento_original} bits...", end="")
compressor = LZWcompressor()
compressor.processe_de_bytes(dados)
compressor.feche()
comprimento_comprimido = len(compressor.fluxo)
print(" Terminado")

# Descompressão
print(f"Descomprimindo {comprimento_comprimido} bits...", end="",
      flush=True)
descompressor = LZWdescompressor()
texto_recuperado = descompressor.recupere_de_fluxo(compressor.fluxo)
print(" Terminado")

print("\nDeu certo?",
      "sim" if dados == texto_recuperado else "\033[38:5:9mnão\033[39m")
print(f"Original:   {comprimento_original:10d} bits")
print(f"Comprimido: {comprimento_comprimido:10d} bits")
taxa_compressao = (comprimento_original - comprimento_comprimido) / \
                  comprimento_original * 100
print(f"Taxa de compressão: {taxa_compressao:.3f}%")

with open("/tmp/saida", "wb") as f:
    f.write(texto_recuperado)
system(f"diff {arquivo} /tmp/saida > /dev/null && echo Ok")
