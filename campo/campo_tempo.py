################################################################################
################################################################################
# Campos tempo

from .campo_basico import CampoBasico, CampoTerminador, CampoPrefixado, CampoFixo, \
    CampoBinario
from time import mktime, gmtime, strptime, strftime, localtime
from struct import pack, unpack


################################################################################
################################################################################
# real básico
class CampoTempoBasico(CampoBasico):
    """
    Classe básica para campo de tempo (data + horário), armazenado
    como o número de segundos desde 1/1/1970, 0h00min00s.
    """

    formato_hora = "%H:%M:%S"
    formato_data = "%Y-%m-%d"
    formato_tempo = "%Y-%m-%d %H:%M:%S"

    def __init__(self, tipo: str, valor: int = 0):
        super().__init__(tipo)
        self.atribua_tempo(valor)

    # todo: __str__ é sáida obseleta (pode ser removida)
    def __str__(self) -> str:
        tempo_utc = strftime(self.formato_tempo,
                             gmtime(self.obtenha_tempo())) + " (UTC)"
        tempo_local = strftime(self.formato_tempo,
                               localtime(self.obtenha_tempo())) + " (local)"
        tempo_segundos = f"{self.valor} segundo(s) desde a era"
        texto = f"{tempo_utc}\n{tempo_local}\n{tempo_segundos}"
        return type(self).__name__ + "\n" + texto

    def atribua_tempo(self, valor: int):
        if not isinstance(valor, (int, float)):
            raise AttributeError(
                "O tempo deve ser um valor numérico (segundos)")
        self.__valor = int(valor)

    def obtenha_tempo(self) -> int:
        return self.__valor

    @property
    def valor(self) -> int:
        return self.obtenha_tempo()

    @valor.setter
    def valor(self, valor):
        self.atribua_tempo(valor)

    @property
    def tempo(self):
        return strftime(self.formato_tempo, localtime(self.obtenha_tempo()))

    @tempo.setter
    def tempo(self, valor):
        self.atribua_tempo(int(mktime(strptime(valor, self.formato_tempo))))

    @property
    def data(self) -> str:
        return strftime(self.formato_data, localtime(self.obtenha_tempo()))

    @data.setter
    def data(self, valor):
        tempo = strptime(valor + " " + self.hora, self.formato_tempo)
        self.atribua_tempo(int(mktime(tempo)))

    @property
    def hora(self) -> str:
        return strftime(self.formato_hora, localtime(self.obtenha_tempo()))

    @hora.setter
    def hora(self, valor):
        tempo = strptime(self.data + " " + valor, self.formato_tempo)
        self.atribua_tempo(int(mktime(tempo)))

    @staticmethod
    def _correcao_fuso():
        """
        Diferença do fuso horário em relação ao horário local e UTC
        :return: a diferença de horário em segundos
        """
        return -int(mktime(gmtime(0)))

    def leia(self, arquivo):
        """
        Conversão dos dados lidos para valor inteiro
        :param arquivo: arquivo binário aberto com permissão de leitura
        """
        pass


class CampoTempoBinario(CampoBinario, CampoTempoBasico):
    """
    Classe para armazenamento de tempo em formato binário (8 bytes,
    big endian, com sinal)
    """

    numero_bytes = 8

    def __init__(self, tipo: str = "tempo binário",
                 valor: str = "1970-01-01 00:00:00"):
        CampoTempoBasico.__init__(self, tipo)
        CampoBinario.__init__(self, self.numero_bytes)
        self.tempo = valor

    @property
    def valor(self) -> str:
        return self.tempo

    @valor.setter
    def valor(self, valor: str):
        if not isinstance(valor, str):
            raise AttributeError("O tempo deve ser no formato "
                                 f"'{self.formato_tempo}'")
        self.tempo = valor

    # code::start data_binario_para_bytes
    def para_bytes(self) -> bytes:
        """
        Conversão da representação interna (número inteiro de segundos)
        para inteiro binário com sinal, big-endian, com comprimento
        'numero_bytes'
        :return: a sequência de bytes representando o valor inteiro
        """
        tempo = self.obtenha_tempo()
        return tempo.to_bytes(self.numero_bytes, "big", signed = True)
        # code::end

    def leia(self, arquivo):
        dado = self.leia_dado_de_arquivo(arquivo)
        self.atribua_tempo(int.from_bytes(dado, "big", signed = True))


class CampoDataBinario(CampoTempoBinario):
    """
    Classe para data em armazenamento binário: número de segundos desde
    1/1/1970 0h0min0s, armazenado em valor inteiro com sinal
    Interface somente para Data
    """

    numero_bytes = 8

    def __init__(self, valor: str = "1970-01-01"):
        CampoTempoBasico.__init__(self, tipo = "data binário")
        CampoBinario.__init__(self, self.numero_bytes)
        self.data = valor
        self.hora = "00:00:00"  # hora local

    @property
    def valor(self) -> str:
        return self.data

    @valor.setter
    def valor(self, valor: str):
        if not isinstance(valor, str):
            raise AttributeError("A data deve ser no formato "
                                 f"'{self.formato_data}'")
        self.data = valor


class CampoHoraBinario(CampoTempoBinario):
    """
    Classe para data em armazenamento binário: número de segundos desde
    1/1/1970 0h0min0s, armazenado em valor inteiro com sinal
    Interface somente para Data
    """

    numero_bytes = 8

    def __init__(self, valor: str = "00:00:00"):
        CampoTempoBinario.__init__(self, tipo = "hora binário")
        CampoBinario.__init__(self, self.numero_bytes)
        self.data = "1970-01-01"  # data padrão
        self.hora = valor

    @property
    def valor(self) -> str:
        return self.hora

    @valor.setter
    def valor(self, valor: str):
        if not isinstance(valor, str):
            raise AttributeError("A data hora ser no formato "
                                 f"'{self.formato_hora}'")
        self.data = valor

#
# class CampoHoraBasico(CampoTempoBasico):
#
#     # code::start data_binario_para_bytes
#     def para_bytes(self):
#         """
#         Conversão da data para sequência de bytes (inteiro com sinal de
#         comprimento 'numero_bytes')
#         :return: o valor real no padrão IEEE 754 de precisão dupla
#         """
#         segundos = mktime(self.valor)
#         dado = pack("d", segundos)
#         return dado
#
#     # code::end
#
#     def leia(self, arquivo):
#         """
#         Conversão dos dados lidos de bytes para IEEE 754 de precisão dupla
#         :param arquivo: arquivo binário aberto com permissão de leitura
#         """
#         dado = self.leia_dado_de_arquivo(arquivo)
#         self.valor = unpack("d", dado)[0]
