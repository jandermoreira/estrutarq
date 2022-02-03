#############################
# Implementação de arquivos
#############################

from os.path import dirname, exists
from time import localtime, mktime

from campo import *
from registro import RegistroFixo
from utilitarios.dispositivo import comprimento_de_bloco


class Arquivo:
    lista_campos_cabecalho = [
        ("comprimento_do_bloco", CampoIntFixo(8)),
        ("criacao", CampoTempoFixo()),
        ("quantidade_de_esquemas", CampoIntFixo(2)),
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
            # Dois bytes para o comprimento do bloco
            comprimento_do_bloco = comprimento_de_bloco(
                dirname(self.nome_arquivo))
            comprimento_em_bytes = comprimento_do_bloco.to_bytes(
                2, "big", signed = False)
            self._arquivo.write(comprimento_em_bytes)

            # Restante do cabeçalho
            self.cabecalho = RegistroFixo(comprimento_do_bloco - 2,
                                          *self.lista_campos_cabecalho)
            self.cabecalho.comprimento_do_bloco.valor = comprimento_do_bloco
            self.cabecalho.criacao.segundos = int(mktime(localtime()))
            self.cabecalho.escreva(self._arquivo)

    def _abra_arquivo_existente(self):
        """

        """
        try:
            self._arquivo = open(self.nome_arquivo, "rb")
        except IOError:
            raise IOError(f"Erro de abertura do arquivo {self.nome_arquivo}.")
        else:
            # Obtenção do cabeçalho
            comprimento_do_bloco = int.from_bytes(
                self._arquivo.read(2), "big", signed = False)
            self.cabecalho = RegistroFixo(comprimento_do_bloco - 2,
                                          *self.lista_campos_cabecalho)
            self.cabecalho.leia(self._arquivo)
            print(self.cabecalho)

    def registro(self, formato):
        """

        :param formato:
        :return:
        """

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
        Fechamento do arquivo associado
        """
        self._arquivo.close()

    def __str__(self):
        """
        Descrição textual do arquivo
        """
        descricao = \
            f"Nome do arquivo: {self.nome_arquivo}\n" + \
            f"Data de criação: {self.cabecalho.criacao.valor}\n" + \
            "Comprimento do bloco na criação: " + \
            f"{self.cabecalho.comprimento_do_bloco} bytes\n"
        return descricao
