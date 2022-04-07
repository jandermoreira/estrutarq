"""
Campos para armazenamento de valores inteiros, provendo classes para
uso de campos cujo conteúdo é um valor inteiro com sinal. Internamente,
o tipo :class:`int` é usado para armazenamento e a transformação para
sequência de bytes podem ser textuais ou binária.

Uma classe básica :class:`~.estrutarq.campo.campo_inteiro.CampoIntBasico`
define uma classe abstrata (ABC) com as propriedades e métodos gerais.
Dela são derivados campos:

* Com terminador
* Prefixado pelo comprimento
* Binário
* De comprimento fixo predefinido

..
    Licença: GNU GENERAL PUBLIC LICENSE V.3, 2007
    Jander Moreira, 2021, 2022
"""

from abc import ABCMeta

from estrutarq.dado import DadoBinario, DadoFixo, DadoPrefixado, DadoTerminador
from .campo_comum import CampoBasico, terminador_de_campo


class CampoIntBasico(CampoBasico, metaclass = ABCMeta):
    """
    Classe básica para campo inteiro. O armazenamento interno usa o tipo
    :class:`int`. A conversão para sequência de bytes assume, por padrão,
    a representação textual do valor inteiro (i.e., conversão para
    sequência de dígitos); outras representações devem sobrescrever os
    métodos de conversão
    :meth:`~.estrutarq.campo.campo_inteiro.CampoIntBasico.bytes_para_valor` e
    :meth:`~.estrutarq.campo.campo_inteiro.CampoIntBasico.valor_para_bytes`.

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

        :rtype: int
        """
        return self.__valor

    @valor.setter
    def valor(self, valor: int):
        """
        Armazenamento de valor inteiro no campo.

        :param int valor: valor inteiro a ser armazenado
        """
        if not isinstance(valor, int):
            raise TypeError("O valor deve ser inteiro")
        self.__valor = valor

    # code::start textual_conversoes
    def bytes_para_valor(self, dado: bytes):
        """
        Conversão de uma sequência de bytes (representação textual) para
        inteiro. O atributo :attr:`~.estrutarq.campo.CampoInteiro.valor` é
        atualizado.

        :param bytes dado: sequência de bytes
        """
        self.valor = int(dado)

    def valor_para_bytes(self) -> bytes:
        """
        Conversão do valor inteiro para sequência de bytes usando
        representação textual e codificação UTF-8.

        :return: sequência de bytes
        :rtype: bytes
        """
        return bytes(f"{self.valor}", "utf-8")
    # code::end


class CampoIntTerminador(DadoTerminador, CampoIntBasico):
    """
    Classe para campo inteiro textual com terminador.

    :param bytes, opcional terminador: um byte único com o valor do terminador
        (padrão :attr:`estrutarq.campo.campo_comum.terminador_de_campo`)
    :param dict, opcional kwargs: lista de parâmetros opcionais passados para
        :attr:`~.estrutarq.campo.campo_cadeia.CampoIntBasico`
    """

    def __init__(self, terminador: bytes = terminador_de_campo, **kwargs):
        CampoIntBasico.__init__(self, "int terminador", **kwargs)
        DadoTerminador.__init__(self, terminador)


class CampoIntPrefixado(DadoPrefixado, CampoIntBasico):
    """Classe para inteiro textual com prefixo de comprimento_bloco"""

    def __init__(self, **kwargs):
        CampoIntBasico.__init__(self, "int prefixado", **kwargs)


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


class CampoIntFixo(DadoFixo, CampoIntBasico):
    """Classe para inteiro textual com tamanho fixo"""

    def __init__(self, comprimento: int, **kwargs):
        """Construtor"""
        CampoIntBasico.__init__(self, "int fixo", **kwargs)
        DadoFixo.__init__(self, comprimento)
        self._comprimento_fixo = True
