"""
Campos para armazenamento de valores temporais, provendo
classes para uso de campos cujo conteúdo representa uma data, uma hora ou
ambos. Internamente, o valor temporal é armazenado em um valor :class:`int`
que contém o número de segundos desde 1/1/1970, 0h00min00s, momento conhecido
como *época* Unix.

Uma classe básica :class:`~.estrutarq.campo.campo_comum.CampoTempoBasico`
define uma classe abstrata (ABC) com as propriedades e métodos gerais e
aplicáveis tanto a datas, horários ou ambos.

Para o armazenamento são considerados os formatos binário (usando o número de
segundos) ou textual. Para textos são usadas bytes com caracteres de
comprimento fixo, como ``1500-04-22`` para datas, ``08:22:31`` para horários
ou ``1500-04-22 08:22:31`` para um momento genérico no tempo.

..
    Licença: GNU GENERAL PUBLIC LICENSE V.3, 2007
    Jander Moreira, 2021, 2022
"""

from abc import ABCMeta
from time import gmtime, localtime, mktime, strftime, strptime

from estrutarq.dado import DadoBinario, DadoFixo
from .campo_comum import CampoBasico


class CampoTempoBasico(CampoBasico, metaclass=ABCMeta):
    """
    Classe básica para campo de tempo (data + horário, somente data e
    somente horário), armazenado internamente como o número de segundos
    desde 1/1/1970, 0h00min00s.

    Quando apenas a data é armazenada, o horário é ajustado para
    12h00min00s, para tentar evitar incompatibilidade do horário interno
    frente ao fuso horário.

    :param str tipo: o tipo do campo (passado por subclasses)
    :param str formato: O formato de interpretação e geração textual
        (são esperados, ``formato_tempo``, ``formato_data`` ou ``formato_hora``)
    :param bool apenas_data: se `True`, o tempo é tratado apenas como
        data; se `False` a parte do horário é também considerada
    :param str, opcional valor: o valor textual da data ou horário, de acordo
        com o ``formato`` especificado
    """

    formato_tempo = "%Y-%m-%d %H:%M:%S"
    """
    Formato de tempo genérico em modo textual (exemplo:
    ``1500-04-22 00:00:00``).
    """

    formato_data = "%Y-%m-%d"
    """
    Formato de data em modo textual (exemplo: ``1500-04-22``).
    """

    formato_hora = "%H:%M:%S"
    """
    Formato de horário em modo textual (exemplo: ``00:00:00``).
    """

    __valor = None

    def __init__(self, tipo: str, formato: str, apenas_data: bool,
                 valor: str = ""):
        CampoBasico.__init__(self, tipo)
        self.__formato_tempo = formato
        self.__apenas_data = apenas_data
        self.valor = valor

    @property
    def valor(self) -> str:
        """
        Interface no modo textual, usando o formato do tempo especificado,
        para :attr:`~.estrutarq.campo.campo_tempo.CampoTempoBasico.segundos`.

        :Recebe: Recebe o tempo em uma cadeia formatada
        :return: Retorna o tempo em uma cadeia formatada
        """
        return strftime(self.__formato_tempo, localtime(self.segundos))

    @valor.setter
    def valor(self, valor: str):
        if not isinstance(valor, str):
            raise TypeError("O tempo deve ser uma cadeia de caracteres no" +
                            f" formato {self.__formato_tempo}.")
        elif valor == "":
            self.segundos = 0
        elif self.__apenas_data:
            self.segundos = int(mktime(strptime(valor + " 12:00:00",
                                                self.formato_tempo)))
        else:
            self.segundos = int(mktime(strptime(valor, self.__formato_tempo)))

    @property
    def segundos(self) -> int:
        """
        O valor em segundos desde a época.

        :Recebe: Recebe o tempo em segundos
        :return: Retorna o tempo em segundos
        """
        return self.__valor

    @segundos.setter
    def segundos(self, valor: int):
        if not isinstance(valor, int):
            raise TypeError("O tempo deve ser um valor inteiro de segundos.")
        self.__valor = valor

    def __str__(self) -> str:
        tempo_utc = strftime(self.formato_tempo,
                             gmtime(self.segundos)) + " (UTC)"
        tempo_local = strftime(self.formato_tempo,
                               localtime(self.segundos)) + " (local)"
        tempo_segundos = f"{self.segundos} segundo(s) desde a era"
        texto = f"{tempo_utc}\n{tempo_local}\n{tempo_segundos}"
        return type(self).__name__ + "\n" + texto


class CampoTempoBasicoBinario(CampoTempoBasico, metaclass=ABCMeta):
    """
    Classe extensão de :class:`~estrutarq.campo.campo_tempo.CampoTempoBasico`
    para incluir as rotinas de conversão de
    :attr:`~estrutarq.campo.campo_tempo.CampoTempoBasico.segundos`
    para binário e vice-versa.

    A representação é feita em um valor binário inteiro de 8 bytes,
    ordenação *big-endian* e com bit de sinal.

    :param list* args: lista de parâmetros posicionais para serem passados para
        :class:`~estrutarq.campo.campo_tempo.CampoTempoBasico`
    :param dict, opcional kwargs: lista de parâmetros opcionais passados para
        :class:`~.estrutarq.campo.campo_tempo.CampoTempoBasico`
    """

    _comprimento = 8  # 8 bytes

    def __init__(self, *args, **kwargs):
        CampoTempoBasico.__init__(self, *args, **kwargs)

    def bytes_para_valor(self, dado: bytes):
        """
        Conversão da representação binária para valor interno do campo
        de segundos.

        :param bytes dado: bytes da representação do tempo em binário
        """
        self.segundos = int.from_bytes(dado, "big", signed=True)

    def valor_para_bytes(self) -> bytes:
        """
        Conversão do valor do tempo interno em segundos para representação em
        inteiro binário.

        :return: a sequência de bytes do tempo em binário
        :rtype: bytes
        """
        return self.segundos.to_bytes(self._comprimento, "big", signed=True)


class CampoTempoBasicoFixo(CampoTempoBasico, metaclass=ABCMeta):
    """
    Classe extensão de :class:`~estrutarq.campo.campo_tempo.CampoTempoBasico`
    para suporte às conversões de representação interna para valor textual e
    vice-versa.

    :param list* args: lista de parâmetros posicionais para serem passados para
        :class:`~estrutarq.campo.campo_tempo.CampoTempoBasico`
    :param dict, opcional kwargs: lista de parâmetros opcionais passados para
        :class:`~.estrutarq.campo.campo_tempo.CampoTempoBasico`
    """

    def __init__(self, *args, **kwargs):
        CampoTempoBasico.__init__(self, *args, **kwargs)

    def bytes_para_valor(self, dado: bytes):
        """
        Conversão da sequência de bytes com a representação textual para o valor
        interno de segundos.

        :param bytes dado: bytes da representação do tempo em cadeia formatada
        """
        self.valor = dado.decode("utf-8")

    def valor_para_bytes(self) -> bytes:
        """
        Conversão do valor do tempo interno de segundos para representação em
        sequência de bytes com caracteres no formato especificado.

        :return: a sequência de bytes do tempo formatado
        :rtype: bytes
        """
        return bytes(self.valor, "utf-8")


########################################

class CampoDataBinario(DadoBinario, CampoTempoBasicoBinario):
    """
    Classe para armazenamento de data (dia, mês e ano) em formato binário.

    :param dict, opcional kwargs: lista de parâmetros opcionais passados para
        :class:`~.estrutarq.campo.campo_tempo.CampoTempoBasicoBinario`
    """

    def __init__(self, **kwargs):
        CampoTempoBasicoBinario.__init__(self, "data binário",
                                         self.formato_data,
                                         apenas_data=True,
                                         **kwargs)
        DadoBinario.__init__(self, CampoTempoBasicoBinario._comprimento)


class CampoDataFixo(DadoFixo, CampoTempoBasicoFixo):
    """
    Classe para data com armazenamento em cadeia de caracteres no formato
    :attr:`~.estrutarq.campo.campo_tempo.CampoTempoBasico.formato_data`.

    :param dict, opcional kwargs: lista de parâmetros opcionais passados para
        :class:`~.estrutarq.campo.campo_tempo.CampoTempoBasicoFixo`
    """

    def __init__(self, **kwargs):
        CampoTempoBasicoFixo.__init__(self, "data fixo", self.formato_data,
                                      apenas_data=True, **kwargs)
        DadoFixo.__init__(self, len(self.valor))


class CampoHoraBinario(DadoBinario, CampoTempoBasicoBinario):
    """
    Classe para horário usando armazenamento em formato binário.

    :param dict, opcional kwargs: lista de parâmetros opcionais passados para
        :class:`~.estrutarq.campo.campo_tempo.CampoTempoBasicoBinario`
    """

    def __init__(self, **kwargs):
        CampoTempoBasicoBinario.__init__(self, "hora binário",
                                         self.formato_hora, apenas_data=False,
                                         **kwargs)
        DadoBinario.__init__(self, CampoTempoBasicoBinario._comprimento)


class CampoHoraFixo(DadoFixo, CampoTempoBasicoFixo):
    """
    Classe para horário com armazenamento em cadeia de caracteres no formato
    :attr:`~.estrutarq.campo.campo_tempo.CampoTempoBasico.formato_hora`.

    :param dict, opcional kwargs: lista de parâmetros opcionais passados para
        :class:`~.estrutarq.campo.campo_tempo.CampoTempoBasicoFixo`
    """

    def __init__(self, **kwargs):
        CampoTempoBasicoFixo.__init__(self, "hora fixo", self.formato_hora,
                                      apenas_data=False, **kwargs)
        DadoFixo.__init__(self, len(self.valor))


class CampoTempoBinario(DadoBinario, CampoTempoBasicoBinario):
    """
    Classe para tempo (data + horário) em binário.

    :param dict, opcional kwargs: lista de parâmetros opcionais passados para
        :class:`~.estrutarq.campo.campo_tempo.CampoTempoBasicoBinario`
    """

    def __init__(self, **kwargs):
        CampoTempoBasicoBinario.__init__(self, "tempo binário",
                                         self.formato_tempo,
                                         apenas_data=False, **kwargs)
        DadoBinario.__init__(self, CampoTempoBasicoBinario._comprimento)


class CampoTempoFixo(DadoFixo, CampoTempoBasicoFixo):
    """
    Classe para horário com armazenamento em cadeia de caracteres no formato
    :attr:`~.estrutarq.campo.campo_tempo.CampoTempoBasico.formato_tempo`.

    :param dict, opcional kwargs: lista de parâmetros opcionais passados para
        :class:`~.estrutarq.campo.campo_tempo.CampoTempoBasicoFixo`
    """

    def __init__(self, **kwargs):
        CampoTempoBasicoFixo.__init__(self, "tempo fixo", self.formato_tempo,
                                      apenas_data=False, **kwargs)
        DadoFixo.__init__(self, len(self.valor))
