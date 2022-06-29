#!/usr/bin/python3
"""
Teste da compressão LZW
"""

from sys import argv

from estrutarq.compressao import LZW

if len(argv) > 1:
    arquivo = argv[1]
else:
    arquivo = "gone_with_the_wind.txt"

compressor = LZW()

# Compressão
with open(arquivo, "rb") as f:
    texto_original = f.read()
compressor.processe_de_bytes(texto_original)

# Descompressão
texto_recuperado = compressor.recupere_de_lista()

print(texto_original == texto_recuperado)

# with open("/tmp/saida", "wb") as f:
#     f.write(texto_recuperado)
# 
# 
# system(f"diff {arquivo} /tmp/saida && echo Ok")
