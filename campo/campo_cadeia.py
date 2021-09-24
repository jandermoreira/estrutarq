################################################################################
################################################################################
# Campos de cadeias de caracteres

from estrutarq.dado import DadoFixo, DadoPrefixado, \
    DadoTerminador
from .campo_comum import CampoBasico, terminador_de_campo


# cadeia de caracteres básica
class CampoCadeiaBasico(CampoBasico):
    """
    Classe básica para cadeias de caracteres
    """

    def __init__(self, nome: str, tipo: str, valor: str = ""):
        CampoBasico.__init__(self, nome, tipo)
        self.valor = valor

    @property
    def valor(self):
        return self.__valor

    @valor.setter
    def valor(self, valor: str):
        if not isinstance(valor, str):
            raise TypeError("O valor deve ser uma cadeia de caracteres")
        self.__valor = valor

    def dado_de_bytes(self, dado: bytes):
        """
        Atribuição de valor a partir da representação de dados
        :param dado: sequência de bytes
        """
        self.valor = dado.decode("utf-8")

    def dado_para_bytes(self) -> bytes:
        """
        Conversão da cadeia de caracteres para sequência de bytes com
        codificação UTF-8
        :return: sequência de bytes
        """
        return bytes(self.valor, "utf-8")


class CampoCadeiaBruto(CampoCadeiaBasico):
    """
    Classe para cadeia de caracteres em formato bruto, ou seja, sem
    organização de campo
    """

    def __init__(self, nome: str, **kwargs):
        super().__init__(nome, "cadeia bruto", **kwargs)


# cadeia de caracteres com terminador
class CampoCadeiaTerminador(DadoTerminador, CampoCadeiaBasico):
    """
    Classe para inteiro textual com terminador
    """

    def __init__(self, nome: str, **kwargs):
        CampoCadeiaBasico.__init__(self, nome, "cadeia terminador", **kwargs)
        DadoTerminador.__init__(self, terminador_de_campo)



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
        dado = bytes(self.valor, encoding = "utf-8")
        return self.formate_dado(dado)
    # code::end
