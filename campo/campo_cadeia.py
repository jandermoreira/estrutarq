################################################################################
################################################################################
# Campos de cadeias de caracteres

from estrutarq.dado import DadoFixo, DadoPrefixado, \
    DadoTerminador
from .campo_basico import CampoBasico


# cadeia de caracteres básica
class CampoCadeiaBasico(CampoBasico):
    """
    Classe básica para cadeias de caracteres
    """

    def __init__(self, nome: str, tipo: str, valor: str = ""):
        super().__init__(nome, tipo)
        self.valor = valor

    @property
    def valor(self):
        return self.__valor

    @valor.setter
    def valor(self, valor: str):
        if not isinstance(valor, str):
            raise TypeError("O valor deve ser uma cadeia de caracteres")
        self.__valor = valor

    def leia(self, arquivo):
        """
        Conversão dos dado lidos para valor inteiro
        :param arquivo: arquivo binário aberto com permissão de leitura
        """
        dado = self.leia_dado_de_arquivo(arquivo)
        self.valor = dado.decode("utf-8")


# cadeia de caracteres com terminador
class CampoCadeiaTerminador(DadoTerminador, CampoCadeiaBasico):
    """
    Classe para inteiro textual com terminador
    """

    def __init__(self, nome: str, **kwargs):
        CampoCadeiaBasico.__init__(self, nome, "cadeia terminador", **kwargs)
        DadoTerminador.__init__(self, **kwargs)

    # code::start terminador_para_bytes
    def para_bytes(self) -> bytes:
        """
        Representação da cadeia de caracteres em uma sequência de
        bytes finalizada com terminador
        :return a sequência de bytes seguida pelo byte do terminador
        """
        dado = bytes(f"{self.valor}", encoding = "utf-8")
        byte_terminador = bytes(f"{self.terminador}", "latin")
        if byte_terminador in dado:
            raise ValueError(
                "Byte terminador não pode estar presente nos dado")
        return dado + byte_terminador
    # code::end


# cadeia de caracteres com prefixo de comprimento
class CampoCadeiaPrefixado(DadoPrefixado, CampoCadeiaBasico):
    """
    Classe para inteiro textual com terminador
    """

    def __init__(self, nome: str, *args, **kwargs):
        super().__init__(nome, "cadeia prefixado", *args, **kwargs)

    # code::start prefixado_para_bytes
    def para_bytes(self) -> bytes:
        """
        Representação da cadeia de caracteres em uma sequência de
        bytes prefixada pelo comprimento (em binário, 2 bytes, big-endian)
        :return: os bytes do comprimento seguidos pela sequência de bytes
        do dado
        """
        dado = bytes(f"{self.valor}", encoding = "utf-8")
        bytes_comprimento = len(dado).to_bytes(2, "big")
        return bytes_comprimento + dado
    # code::end


# cadeia de caracteres com prefixo de comprimento
class CampoCadeiaFixo(DadoFixo, CampoCadeiaBasico):
    """
    Classe para inteiro textual com terminador
    """

    def __init__(self, nome: str, *args, **kwargs):
        CampoCadeiaBasico.__init__(self, nome, "cadeia fixo", **kwargs)
        DadoFixo.__init__(self, *args, **kwargs)

    # code::start fixo_para_bytes
    def para_bytes(self) -> bytes:
        """
        Representação da cadeia de caracteres em uma sequência de
        bytes de comprimento fixo
        :return os bytes da sequência de bytes do dado

        Valores com comprimento maior que o do campo são truncados, enquanto
        os com comprimento menor têm as posições inválidas preenchidas com um
        byte de preenchimento.
        """
        dado = bytes(self.valor, encoding = "utf-8")[:self.comprimento]
        byte_preenchimento = bytes(self.preenchimento, "latin")
        dado = dado + byte_preenchimento * (self.comprimento - len(dado))
        return dado
    # code::end
