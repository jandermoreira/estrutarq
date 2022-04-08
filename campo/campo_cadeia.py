"""
Campos para armazenamento de cadeias de caracteres, provendo classes
para uso de campos cujo conteúdo é uma cadeia de caracteres.
Internamente, o tipo :class:`str` é usado para armazenamento e a
transformação para sequência de bytes usa a codificação UTF-8.

Uma classe básica :class:`~.estrutarq.campo.campo_cadeia.CampoCadeiaBasico`
define uma classe abstrata (ABC) com as propriedades e métodos gerais. Dela
são derivados campos:

* Com terminador
* Prefixado pelo comprimento
* De comprimento fixo predefinido

..
    Licença: GNU GENERAL PUBLIC LICENSE V.3, 2007
    Jander Moreira, 2021, 2022
"""

from abc import ABCMeta

from estrutarq.dado import DadoFixo, DadoPrefixado, DadoTerminador
from .campo_comum import CampoBasico, terminador_de_campo


class CampoCadeiaBasico(CampoBasico, metaclass = ABCMeta):
    """
    Classe básica para cadeias de caracteres.

    :param str tipo: nome do tipo (definido nas subclasses)
    :param str, opcional valor: o valor a ser armazenado no campo
        (padrão: ``""``)
    """

    def __init__(self, tipo: str, valor: str = ""):
        CampoBasico.__init__(self, tipo)
        self.valor = valor

    @property
    def valor(self) -> str:
        """
        O valor do campo. Recebe e retorna uma cadeia de caracteres.

        :Recebe: Recebe um valor para ser armazenado
        :return: Retorna o valor atual do campo
        :tipo: str
        """
        return self.__valor

    @valor.setter
    def valor(self, valor: str):
        if not isinstance(valor, str):
            raise TypeError("O valor deve ser uma cadeia de caracteres")
        self.__valor = valor

    # code::start conversoes
    def bytes_para_valor(self, dado: bytes):
        """Armazenamento da sequência de bytes de ``dado`` como valor
        do campo.
        
        :param bytes dado: sequência de bytes com codificação UTF-8
        """
        self.valor = dado.decode("utf-8")

    def valor_para_bytes(self) -> bytes:
        """Retorno do valor do campo convertido para sequência
        de bytes usando codificação UTF-8.
        
        :return: sequência de bytes
        :rtype: bytes
        """
        return bytes(self.valor, "utf-8")
    # code::end


class CampoCadeiaTerminador(DadoTerminador, CampoCadeiaBasico):
    """
    Classe para cadeia de caracteres com terminador. O terminador de campo é
    definido por :attr:`estrutarq.campo.terminador_de_campo`.

    :param dict, opcional kwargs: lista de parâmetros opcionais passados para
        :attr:`~.estrutarq.campo.campo_cadeia.CampoCadeiaBasico`
    """

    def __init__(self, **kwargs):
        CampoCadeiaBasico.__init__(self, "cadeia terminador", **kwargs)
        DadoTerminador.__init__(self, terminador_de_campo)


class CampoCadeiaPrefixado(DadoPrefixado, CampoCadeiaBasico):
    """
    Classe para cadeia de caracteres prefixada pelo comprimento. O prefixo é
    o adotado em
    :class:`~.estrutarq.dado.DadoPrefixado`.


    :param dict, opcional kwargs: lista de parâmetros opcionais passados para
        :class:`~.estrutarq.campo.campo_cadeia.CampoCadeiaBasico`
    """

    def __init__(self, **kwargs):
        CampoCadeiaBasico.__init__(self, "cadeia prefixado", **kwargs)
        DadoPrefixado.__init__(self)


class CampoCadeiaFixo(DadoFixo, CampoCadeiaBasico):
    """
    Classe para cadeia de caracteres com comprimento fixo, com enchimento de
    bytes e preenchimento de bytes inválidos. O byte de prenchimento é o
    padrão de :class:`~.estrutarq.dado.DadoFixo`.

    :param int comprimento: o comprimento do campo em bytes
    :param dict, opcional kwargs: lista de parâmetros opcionais passados para
        :class:`~.estrutarq.campo.campo_cadeia.CampoCadeiaBasico`
    """

    def __init__(self, comprimento: int, **kwargs):
        CampoCadeiaBasico.__init__(self, "cadeia fixo", **kwargs)
        DadoFixo.__init__(self, comprimento)
