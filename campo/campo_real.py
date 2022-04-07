"""
Campos para armazenamento de valores reais, provendo classes para
uso de campos cujo conteúdo é um valor em ponto flutuante. Internamente,
o tipo :class:`float` é usado para armazenamento e a transformação para
sequência de bytes podem ser textuais ou binária.

Uma classe básica :class:`~.estrutarq.campo.campo_real.CampoRealBasico`
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
from struct import pack, unpack

from typing import Union

from estrutarq.dado import DadoBinario, DadoFixo, DadoPrefixado, DadoTerminador
from .campo_comum import CampoBasico, terminador_de_campo


class CampoRealBasico(CampoBasico, metaclass = ABCMeta):
    """
    Classe básica para campo com valor real. O armazenamento interno usa
    o tipo :class:`float`. A conversão para sequência de bytes assume, por
    padrão, a representação textual do valor real (i.e., conversão para
    sequência de dígitos); outras representações devem sobrescrever os
    métodos de conversão
    :meth:`~.estrutarq.campo.campo_real.CampoRealBasico.bytes_para_valor` e
    :meth:`~.estrutarq.campo.campo_real.CampoRealBasico.valor_para_bytes`.

    :param str tipo: o nome do tipo (definido em subclasses)
    :param float, opcional valor: o valor a ser armazenado no campo
        (padrão: 0.0)
    """

    def __init__(self, tipo: str, valor: float = 0.0):
        super().__init__(tipo)
        self.valor = valor

    @property
    def valor(self) -> float:
        """
        Valor numérico real armazenado no campo.

        :Recebe: Recebe um valor para ser armazenado
        :return: Retorna o valor atual do campo
        :type: float
        """
        return self.__valor

    @valor.setter
    def valor(self, valor: Union[float, int]):
        """
        Atribuição de valor ao campo.
        
        :param float, int valor: valor a ser armazenado no campo
        """
        if not isinstance(valor, (float, int)):
            raise TypeError("O valor deve ser real ou inteiro")
        self.__valor = float(valor)

    # code::start conversoes
    def bytes_para_valor(self, dado: bytes):
        """
        Conversão de sequência de bytes com valor textual (dígitos, sinal e
        ponto decimal) para valor real. O valor convertido é armazenado como
        valor interno do campo.
        
        :param bytes dado: sequência de bytes com o valor textual do real 
        """
        self.valor = float(dado)

    def valor_para_bytes(self) -> bytes:
        """
        Conversão do valor interno do campo para sequência de bytes usando
        representação textual. O formato textual é o padrão da linguagem
        Python.
        
        :return: a sequência de bytes que forma o valor real
        """
        return bytes(f"{self.valor}", "utf-8")
    # code::end


class CampoRealTerminador(DadoTerminador, CampoRealBasico):
    """
    Classe para campo real com representação textual com um byte terminador
    que indica o fim da sequência.

    :param bytes, opcional terminador: um byte único com o valor do terminador
        (valor padrão :attr:`estrutarq.campo.campo_comum.terminador_de_campo`)
    :param dict, opcional kwargs: lista de parâmetros opcionais passados para
        :class:`~.estrutarq.campo.campo_real.CampoRealBasico`
    """

    def __init__(self, terminador: bytes = terminador_de_campo,
                 **kwargs):
        CampoRealBasico.__init__(self, "real fixo", **kwargs)
        DadoTerminador.__init__(self, terminador)


class CampoRealPrefixado(DadoPrefixado, CampoRealBasico):
    """
    Classe para campo real com representação textual com prefixo de comprimento,
    conforme definido em :class:`estrutarq.dado.DadoPrefixado`.

    :param dict, opcional kwargs: lista de parâmetros opcionais passados para
        :class:`~.estrutarq.campo.campo_real.CampoRealBasico`
    """

    def __init__(self, **kwargs):
        CampoRealBasico.__init__(self, "real prefixado", **kwargs)


class CampoRealBinario(DadoBinario, CampoRealBasico):
    """
    Classe para real em formato binário. A conversão para sequência de bytes
    é feita segundo padrão IEEE 754 de precisão dupla.

    :param dict, opcional kwargs: lista de parâmetros opcionais passados para
        :class:`~.estrutarq.campo.campo_real.CampoRealBasico`
    """

    def __init__(self, **kwargs):
        CampoRealBasico.__init__(self, "real binário", **kwargs)
        DadoBinario.__init__(self, len(pack("d", 0)))

    # code::start binario_conversoes
    def bytes_para_valor(self, dado: bytes):
        """
        Conversão de sequência de bytes com representação IEEE 754 de
        precisão dupla para real, com armazenamento do valor convertido como
        valor do campo.

        :param bytes dado: sequência de 8 bytes com o valor real em binário
        """
        self.valor = unpack("d", dado)[0]

    def valor_para_bytes(self) -> bytes:
        """
        Conversão do valor do campo para sequência de bytes no padrão
        IEEE 754 de precisão dupla.

        :return: a sequência de bytes no padrão especificado
        :rtype: bytes
        """
        return pack("d", self.valor)
    # code::end


class CampoRealFixo(DadoFixo, CampoRealBasico):
    """
    Classe para campo real com representação textual com comprimento fixo
    predefinido. Os bytes que não correspondem aos dados são preenchidos
    conforme definido em :class:`~.estrutarq.dado.DadoFixo`.

    :param int comprimento: comprimento em bytes fixado para o campo.
    :param dict, opcional kwargs: lista de parâmetros opcionais passados para
        :class:`~.estrutarq.campo.campo_real.CampoRealBasico`
    """

    def __init__(self, comprimento: int, **kwargs):
        CampoRealBasico.__init__(self, "real fixo", **kwargs)
        DadoFixo.__init__(self, comprimento)
