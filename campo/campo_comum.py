################################################################################
################################################################################
#  Implementação de campos

################################################################################
################################################################################

from abc import ABCMeta, abstractmethod
from copy import copy
from typing import BinaryIO

from estrutarq.dado import DadoBasico, DadoBruto

terminador_de_campo = b"\x00"


class CampoBasico(DadoBasico, metaclass = ABCMeta):
    """
    Estruturação básica do campo como menor unidade de informação.
    """

    def __init__(self, tipo: str):
        self.__tipo = tipo
        self._comprimento_fixo = False

    @property
    def tipo(self):
        return self.__tipo

    @property
    @abstractmethod
    def valor(self):
        """
        Recuperação, com as devidas conversões, do atributo __valor
        :return: o valor de __valor
        """
        pass

    @valor.setter
    @abstractmethod
    def valor(self, valor):
        """
        Atribuição, com as devidas conversões, para o atributo __valor
        """
        pass

    @abstractmethod
    def bytes_para_valor(self, dado: bytes):
        """
        Conversão de uma sequência de bytes para armazenamento no valor
        do campo, de acordo com a representação de dados
        :param dado: sequência de bytes
        :return: o valor do campo de acordo com seu tipo
        """
        pass

    @abstractmethod
    def valor_para_bytes(self) -> bytes:
        """
        Conversão do valor do campo para sequência de bytes de acordo
        com a representação de dados
        :return:
        """
        pass

    def comprimento_fixo(self):
        """
        Obtém o comprimento_bloco do campo, se ele for fixo
        :return: o comprimento_bloco do campo se for fixo ou None se
            for variável
        """
        return self._comprimento_fixo

    # code::start leitura_escrita
    def leia(self, arquivo: BinaryIO):
        """
        Conversão dos dado lidos para o valor do campo, obedecendo à
        organização e formato de representação
        :param arquivo: arquivo binário aberto com permissão de leitura
        """
        dado = self.leia_de_arquivo(arquivo)
        self.bytes_para_valor(dado)

    def escreva(self, arquivo: BinaryIO):
        """
        Conversão do valor para sequência de bytes e armazenamento no
        arquivo
        :param arquivo: arquivo binário aberto com permissão de escrita
        """
        dado = self.valor_para_bytes()
        arquivo.write(self.adicione_formatacao(dado))

    # code::end

    def __str__(self):
        """
        Valor padrão do campo para um 'print'
        :return: o valor do campo
        """
        return str(self.valor)

    def copy(self):
        """
        Cópia "rasa" deste campo
        :return: outra instância com os mesmos valores
        """
        return copy(self)


class CampoBruto(DadoBruto, CampoBasico):
    """
    Implementação das funções de um campo bruto, ou seja, sem organização
    de campo. O valor é sempre armazenado como cadeia de caracteres.
    """

    def __init__(self, valor = ""):
        super().__init__("bruto")
        self.valor = valor

    @property
    def valor(self):
        return self.__valor

    @valor.setter
    def valor(self, valor):
        """
        O valor armazenado para o campo básico (i.e., bruto) é sempre uma
        cadeia de caracteres
        :param valor: um valor qualquer
        """
        self.__valor = str(valor)

    # code::start bruto_conversoes
    def bytes_para_valor(self, dado: bytes):
        """
        Conversão de sequência de bytes para valor o campo, considerando
        uma cadeia de caracteres simples
        :param dado: a sequência de bytes
        """
        self.valor = dado.decode("utf-8")

    def valor_para_bytes(self) -> bytes:
        """
        Conversão do valor do campo (cadeia de caracteres) para uma
        sequência de bytes, usando codificação UTF-8
        :return: a sequência de bytes
        """
        return bytes(self.valor, "utf-8")

    # code::end
