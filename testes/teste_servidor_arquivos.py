"""
Teste do servidor de arquivos
"""

from servidor_de_arquivos import *

servidor = ServidorDeArquivos("localhost", 10027)
servidor.inicie()