"""
Campos para armazenamento de valores inteiros.

Este arquivo provê classes para uso de campos cujo conteúdo é
um valor inteiro com sinal. Internamente, o tipo :class:`int` é usado
para armazenamento e a transformação para sequência de bytes podem ser
textuais ou binária.

Uma classe básica :class:`~.estrutarq.campo.campo_inteiro.CampoIntBasico`
define uma classe abstrata (ABC) com as propriedades e métodos gerais.
Dela são derivados campos:

* Com terminador
* Prefixado pelo comprimento
* Binário
* De comprimento fixo predefinido

..
    Licença: GNU GENERAL PUBLIC LICENSE V.3, 2007
    Jander Moreira, 2021-2022
"""

from abc import ABCMeta

from estrutarq.dado import DadoBinario, DadoFixo, DadoPrefixado, DadoTerminador
from .campo_comum import CampoBasico, terminador_de_campo


################################################################################
################################################################################
class CampoIntBasico(CampoBasico, metaclass = ABCMeta):
    """
    Classe básica para campo inteiro.

    :param str tipo: o nome do tipo (definido em subclasses)
    :param int, opcional valor: o valor a ser armazenado no campo
        (padrão: 0)
    """

    def __init__(self, tipo: str, valor: int = 0):
        CampoBasico.__init__(self, tipo)
        self.valor = valor

    @property
    def valor(self) -> int:
        """
        Valor inteiro armazenado no campo.
        """
        return self.__valor

    @valor.setter
    def valor(self, valor: int):
        if not isinstance(valor, int):
            raise TypeError("O valor deve ser inteiro")
        self.__valor = valor

    # code::start textual_conversoes
    def bytes_para_valor(self, dado: bytes):
        """
        Conversão de uma sequência de bytes (representação textual)
        para inteiro
        :param dado: sequência de bytes
        """
        self.valor = int(dado)

    def valor_para_bytes(self) -> bytes:
        """
        Conversão do valor inteiro para sequência de bytes usando
        representação textual e codificação UTF-8
        :return: sequência de bytes
        """
        return bytes(f"{self.valor}", "utf-8")
    # code::end


class CampoIntTerminador(DadoTerminador, CampoIntBasico):
    """
    Classe para inteiro textual com terminador
    """

    def __init__(self, terminador: bytes = terminador_de_campo, **kwargs):
        CampoIntBasico.__init__(self, "int terminador", **kwargs)
        DadoTerminador.__init__(self, terminador)

    # def comprimento_fixo(self):
    #     """
    #     Obtém o comprimento_bloco do campo, se ele for fixo
    #     :return: o comprimento_bloco do campo se for fixo ou None se for variável
    #     """
    #     return None


class CampoIntPrefixado(DadoPrefixado, CampoIntBasico):
    """Classe para inteiro textual com prefixo de comprimento_bloco"""

    def __init__(self, **kwargs):
        CampoIntBasico.__init__(self, "int prefixado", **kwargs)

    # def comprimento_fixo(self):
    #     """
    #     Obtém o comprimento_bloco do campo, se ele for fixo
    #     :return: o comprimento_bloco do campo se for fixo ou None se for variável
    #     """
    #     return None


class CampoIntBinario(DadoBinario, CampoIntBasico):
    """
    Classe para inteiro em formato binário (big endian) com 8 bytes
    e complemento para 2 para valores negativos
    """

    numero_bytes = 8  # 8 bytes

    def __init__(self, **kwargs):
        CampoIntBasico.__init__(self, "inteiro binário", **kwargs)
        DadoBinario.__init__(self, self.numero_bytes)
        self._comprimento_fixo = True

    # code::start binario_conversoes
    def bytes_para_valor(self, dado: bytes):
        """
        Conversão de uma sequência de bytes (binária big-endian com sinal)
        para inteiro
        :param dado: sequência de bytes
        """
        if len(dado) != self.numero_bytes:
            raise TypeError(
                "Sequência de bytes com comprimento_bloco inesperado.")
        self.valor = int.from_bytes(dado, "big", signed = True)

    def valor_para_bytes(self) -> bytes:
        """
        Conversão do valor inteiro para sequência de bytes usando
        representação binária big-endian com sinal
        :return: sequência de bytes
        """
        return self.valor.to_bytes(self.numero_bytes, "big", signed = True)

    # code::end

    # def comprimento_fixo(self):
    #     """
    #     Obtém o comprimento_bloco do campo, se ele for fixo
    #     :return: o comprimento_bloco do campo se for fixo ou None se for variável
    #     """
    #     return self.comprimento


class CampoIntFixo(DadoFixo, CampoIntBasico):
    """Classe para inteiro textual com tamanho fixo"""

    def __init__(self, comprimento: int, **kwargs):
        """Construtor"""
        CampoIntBasico.__init__(self, "int fixo", **kwargs)
        DadoFixo.__init__(self, comprimento)
        self._comprimento_fixo = True

    # def comprimento_fixo(self):
    #     """
    #     Obtém o comprimento_bloco do campo, se ele for fixo
    #     :return: o comprimento_bloco do campo se for fixo ou None se for variável
    #     """
    #     return self.comprimento
