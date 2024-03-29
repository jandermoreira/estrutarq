"""
Implementação de campos, provendo a classe básica para definição de campos.

Uma classe básica :class:`~.estrutarq.campo.campo_comum.CampoBasico`
define uma classe abstrata (ABC) com as propriedades e métodos gerais.
Dela são derivados os demais campos.
A classe :class:`~.estrutarq.campo.campo_comum.CampoBruto`, também
disponibilizada, define um campo sem organização que utiliza
:class:`str` (UTF-8) como valor.

..
    Licença: GNU GENERAL PUBLIC LICENSE V.3, 2007
    Jander Moreira, 2021, 2022
"""

from abc import ABCMeta, abstractmethod
from copy import copy
from typing import BinaryIO

from estrutarq.dado import DadoBasico, DadoBruto

terminador_de_campo: bytes = b"\x00"
"""
O terminador de campo é um byte único usado como delimitador para o
fim do campo. O valor padrão é ``0x00``.
"""


class CampoBasico(DadoBasico, metaclass=ABCMeta):
    """
    Classe básica para campo, a menor unidade de informação.

    :param str tipo: cadeia de caracteres com o nome do tipo; possíveis valores
        são, por exemplo, ``"cadeia fixo"``, ``"real terminador"`` ou
        ``"int prefixado"``
    """

    def __init__(self, tipo: str):
        DadoBasico.__init__(self)
        self.__tipo = tipo
        self._comprimento_fixo = False

    @property
    def tipo(self):
        """
        Nome do tipo do campo. É um valor puramente ornamental (i.e., não
        é usado internamente com nenhum fim) e pode ser consultado externamente.

        :return: Retorna o tipo do campo
        """
        return self.__tipo

    @property
    @abstractmethod
    def valor(self):
        """
        Valor do campo, usando sua representação interna. Recebe e retorna o
        valor armazenado.
        """
        pass

    @valor.setter
    @abstractmethod
    def valor(self, valor):
        """
        Atribuição do valor ao campo.
        """
        pass

    @abstractmethod
    def bytes_para_valor(self, dado: bytes):
        """
        Conversão de uma sequência de bytes para armazenamento para valor
        do campo, de acordo com a representação de dados.
        O :attr:`~.estrutarq.campo.CampoBasico.valor` é atualizado.

        :param bytes dado: sequência de bytes
        """
        pass

    @abstractmethod
    def valor_para_bytes(self) -> bytes:
        """
        Conversão do valor do campo para sequência de bytes de acordo
        com a representação de dados.

        :return: sequência de bytes
        :rtype: bytes
        """
        pass

    def tem_comprimento_fixo(self) -> bool:
        """
        Retorna se o comprimento é ou não fixo.

        :return: `True` para comprimento fixo ou `False` para variável
        :rtype: bool
        """
        return self._comprimento_fixo

    def comprimento(self) -> int:
        """
        Obtém o comprimento atual do campo após convertido para sequência de
        bytes, o que inclui a organização do dado.

        :return: o comprimento do campo com a organização
        :rtype: int
        """
        return len(self.adicione_formatacao(self.valor_para_bytes()))

    # code::start leitura_escrita
    def leia(self, arquivo: BinaryIO):
        """
        Leitura da sequência de bytes que representa o campo e sua conversão
        para o valor do campo, obedecendo à organização e formato de
        representação.
        O :attr:`~.estrutarq.campo.CampoBasico.valor` é atualizado.

        :param BinaryIO arquivo: arquivo binário aberto com permissão de leitura
        """
        dado = self.leia_de_arquivo(arquivo)
        self.bytes_para_valor(dado)

    def escreva(self, arquivo: BinaryIO):
        """
        Conversão do valor do campo para sequência de bytes e armazenamento no
        arquivo, incluindo a organização de dados.

        :param BinaryIO arquivo: arquivo binário aberto com permissão de escrita
        """
        dado = self.valor_para_bytes()
        arquivo.write(self.adicione_formatacao(dado))

    # code::end

    @property
    def dado_formatado(self) -> bytes:
        """

        :return: sequência de bytes com a formatação da organização do dado
        """
        return self.adicione_formatacao(self.valor_para_bytes())

    def __str__(self) -> str:
        """
        Retorno do valor textual do campo.

        :return: o valor do campo
        :rtype: str
        """
        return str(self.valor)

    def copia(self):
        """
        Retorna uma cópia "rasa" do objeto.

        :return: uma instância copiada de ``self``
        """
        return copy(self)


class CampoBruto(DadoBruto, CampoBasico):
    """
    Implementação das funções de um campo bruto, ou seja, sem organização
    de campo. O valor é sempre armazenado como cadeia de caracteres com
    codificação de caracteres UTF-8.

    :param str, opcional valor: valor do campo
    """

    def __init__(self, valor=""):
        CampoBasico.__init__(self, "bruto")
        DadoBruto.__init__(self)
        self.valor = valor

    @property
    def valor(self) -> str:
        """
        O valor armazenado no campo. Recebe e retorna uma cadeia de caracteres.

        :Recebe: Recebe uma cadeia de caracteres
        :return: Retorna o valor armazenado no campo
        """
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
        Atualização do valor do campo a partir de uma sequência de bytes
        com codificação UTF-8.

        :param bytes dado: a sequência de bytes
        """
        self.valor = dado.decode("utf-8")

    def valor_para_bytes(self) -> bytes:
        """
        Retorno do valor do campo (cadeia de caracteres) convertido para uma
        sequência de bytes, usando codificação UTF-8.

        :return: a sequência de bytes
        :rtype: bytes
        """
        return bytes(self.valor, "utf-8")

    # code::end
