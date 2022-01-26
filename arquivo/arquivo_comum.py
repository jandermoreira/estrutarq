#############################
# Implementação de arquivos
#############################

from os.path import exists
from time import localtime, mktime

# from registro import RegistroBasico
from bloco import Bloco
from campo import *
from registro import RegistroFixo
from utilitarios.dispositivo import comprimento_de_bloco
from os.path import dirname


class Arquivo:
    lista_campos_cabecalho = [
        ("comprimento_do_bloco", CampoIntFixo(8)),
        ("criacao", CampoTempoFixo())
    ]

    def __init__(self, nome: str, novo: bool = False):
        self.nome_arquivo = nome
        if not exists(self.nome_arquivo) or novo:
            self._crie_arquivo_novo()
        else:
            self._abra_arquivo_existente()

    def _crie_arquivo_novo(self):
        """
            Criação de um arquivo novo, com seu cabeçalho
        """
        try:
            self._arquivo = open(self.nome_arquivo, "wb")
        except IOError:
            raise IOError(f"Erro de criação do arquivo {self.nome_arquivo}.")
        else:
            comprimento_do_bloco = comprimento_de_bloco(
                dirname(self.nome_arquivo))
            cabecalho = RegistroFixo(comprimento_do_bloco)
            cabecalho.adicione_campos(*self.lista_campos_cabecalho)
            cabecalho.comprimento_do_bloco.valor = comprimento_do_bloco
            cabecalho.criacao.segundos = int(mktime(localtime()))
            print(cabecalho)
            cabecalho.escreva(self._arquivo)

    def _abra_arquivo_existente(self):
        """

        """
        # try:
        #     self._arquivo = open(self.nome_arquivo, modo)
        # except IOError:
        #     raise IOError(f"Erro de abertura do arquivo {self.nome_arquivo}.")
        # else:
        #     self.bloco = Bloco(self._arquivo)

    # def registro(self, formato):
    #     if isinstance(formato, str):
    #         # cria arquivo a partir de especificação textual
    #         ""
    #     elif isinstance(RegistroBasico):
    #         # cria arquivo a partir de um registro pré-existente
    #         ""
    #     else:
    #         raise TypeError("Esperado um registro ou uma especificação.")

    def feche(self):
        """
        Fecha o arquivo
        """
        self._arquivo.close()
