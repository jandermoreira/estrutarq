################################################################################
################################################################################
# Campos inteiros
from abc import ABCMeta

from estrutarq.dado import DadoBinario, DadoTerminador, DadoPrefixado, DadoFixo
from .campo_comum import CampoBasico, terminador_de_campo


################################################################################
################################################################################
class CampoIntBasico(CampoBasico, metaclass = ABCMeta):
    """
    Classe básica para campo inteiro
    """

    def __init__(self, tipo: str, valor: int = 0):
        super().__init__(tipo)
        self.valor = valor

    @property
    def valor(self) -> int:
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
        
    def comprimento_fixo(self):
        """
        Obtém o comprimento do campo, se ele for fixo
        :return: o comprimento do campo se for fixo ou None se for variável 
        """
        return None



class CampoIntPrefixado(DadoPrefixado, CampoIntBasico):
    """Classe para inteiro textual com prefixo de comprimento"""

    def __init__(self, **kwargs):
        super().__init__("int prefixado", **kwargs)

    def comprimento_fixo(self):
        """
        Obtém o comprimento do campo, se ele for fixo
        :return: o comprimento do campo se for fixo ou None se for variável 
        """
        return None


class CampoIntFixo(DadoFixo, CampoIntBasico):
    """Classe para inteiro textual com tamanho fixo"""

    def __init__(self, comprimento: int, **kwargs):
        """Construtor"""
        CampoIntBasico.__init__(self, "int fixo", **kwargs)
        DadoFixo.__init__(self, comprimento)

    def comprimento_fixo(self):
        """
        Obtém o comprimento do campo, se ele for fixo
        :return: o comprimento do campo se for fixo ou None se for variável 
        """
        return self.comprimento

class CampoIntBinario(DadoBinario, CampoIntBasico):
    """
    Classe para inteiro em formato binário (big endian) com 8 bytes
    e complemento para 2 para valores negativos
    """

    numero_bytes = 8  # 8 bytes

    def __init__(self, **kwargs):
        CampoIntBasico.__init__(self, "inteiro binário", **kwargs)
        DadoBinario.__init__(self, self.numero_bytes)

    # code::start binario_conversoes
    def bytes_para_valor(self, dado: bytes):
        """
        Conversão de uma sequência de bytes (binária big-endian com sinal)
        para inteiro
        :param dado: sequência de bytes
        """
        if len(dado) != self.numero_bytes:
            raise TypeError("Sequência de bytes com comprimento inesperado.")
        self.valor = int.from_bytes(dado, "big", signed = True)

    def valor_para_bytes(self) -> bytes:
        """
        Conversão do valor inteiro para sequência de bytes usando
        representação binária big-endian com sinal
        :return: sequência de bytes
        """
        return self.valor.to_bytes(self.numero_bytes, "big", signed = True)
    # code::end

    def comprimento_fixo(self):
        """
        Obtém o comprimento do campo, se ele for fixo
        :return: o comprimento do campo se for fixo ou None se for variável 
        """
        return DadoBinario.comprimento
