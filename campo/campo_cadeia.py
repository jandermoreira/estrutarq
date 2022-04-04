"""
Campos para armazenamento de cadeias de caracteres.

Este arquivo provê classes para uso de campos cujo conteúdo é
uma cadeia de caracteres. Internamente, o tipo `str` é usado
para armazenamento e a transformação para sequência de bytes
usa a codificação UTF-8.

Uma classe básica :class:`CampoCadeiaBasico` define uma classe
abstrata (ABC) com as propriedades e métodos gerais. Dela são
derivadas campos:

    * Com terminadores
    * Prefixada pelo comprimento
    * De comprimento fixo predefinido

Licença: GNU GENERAL PUBLIC LICENSE V.3, 2007

Jander Moreira, 2021-2022
"""

from abc import ABCMeta
import typing

from estrutarq.dado import DadoFixo, DadoPrefixado, \
    DadoTerminador
from .campo_comum import CampoBasico, terminador_de_campo


# cadeia de caracteres básica
class CampoCadeiaBasico(CampoBasico, metaclass = ABCMeta):
    """
    Classe básica para cadeias de caracteres.

    :param tipo: nome do tipo (definido nas classes derivadas)
    :type tipo: str
    :param str, opcional valor: o valor a ser armazenado no campo
        (padrão: ``""``)
    """

    def __init__(self, tipo: str, valor: str = ""):
        CampoBasico.__init__(self, tipo)
        self.valor = valor

    @property
    def valor(self):
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
        
        :param dado: sequência de bytes com codificação UTF-8
        :type dado: bytes
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


# cadeia de caracteres com terminador
class CampoCadeiaTerminador(DadoTerminador, CampoCadeiaBasico):
    """
    Classe para cadeia de caracteres com terminador

    :param kwargs: parâmetros nomeados a serem repassados
    :type kwargs: :class:dict
    """

    def __init__(self, **kwargs):
        CampoCadeiaBasico.__init__(self, "cadeia terminador", **kwargs)
        DadoTerminador.__init__(self, terminador_de_campo)


# cadeia de caracteres com prefixo de comprimento
class CampoCadeiaPrefixado(DadoPrefixado, CampoCadeiaBasico):
    """
    Classe para cadeia de caracteres prefixada pelo comprimento_bloco
    """

    def __init__(self, *args, **kwargs):
        CampoCadeiaBasico.__init__(self, "cadeia prefixado", *args, **kwargs)
        DadoPrefixado.__init__(self)


class CampoCadeiaFixo(DadoFixo, CampoCadeiaBasico):
    """
    Classe para cadeia de caracteres com comprimento_bloco fixo e preenchimento
    de dados inválidos
    """

    def __init__(self, comprimento: int, **kwargs):
        CampoCadeiaBasico.__init__(self, "cadeia fixo", **kwargs)
        DadoFixo.__init__(self, comprimento)
