################################################################################
################################################################################
# Campos de cadeias de caracteres

import campo

# cadeia de caracteres básica
class CampoCadeiaBasico(campo.CampoBasico):
    """
    Classe básica para cadeias de caracteres
    """

    def __init__(self, tipo: str, valor: str = ""):
        super().__init__(tipo)
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
        Conversão dos dados lidos para valor inteiro
        :param arquivo: arquivo binário aberto com permissão de leitura
        """
        dado = self.leia_dado_de_arquivo(arquivo)
        self.valor = dado.decode("utf-8")


# cadeia de caracteres com terminador
class CampoCadeiaTerminador(campo.CampoTerminador, CampoCadeiaBasico):
    """
    Classe para inteiro textual com terminador
    """

    # code::start para_bytes_cadeia_terminador
    def para_bytes(self) -> bytes:
        """
        Representação da cadeia de caracteres em uma sequência de
        bytes finalizada com terminador
        :return a sequência de bytes seguida pelo byte do terminador
        """
        dado = bytes(f"{self.valor}", encoding = "utf-8")
        byte_terminador = bytes(f"{self.terminador}", "latin")
        assert byte_terminador not in dado
        return dado + byte_terminador
    # code::end


# cadeia de caracteres com prefixo de comprimento
class CampoCadeiaPrefixado(CampoPrefixado, CampoCadeiaBasico):
    """
    Classe para inteiro textual com terminador
    """

    def __init__(self, *args, **kwargs):
        super().__init__("cadeia prefixo", *args, **kwargs)

    # code::start para_bytes_prefixo
    def para_bytes(self) -> bytes:
        """
        Representação da cadeia de caracteres em uma sequência de
        bytes prefixada pelo comprimento (em binário, 2 bytes, big-endian)
        :return: os bytes do comprimento seguidos pela sequência de bytes
        do dado
        """
        dado = bytes(f"{self.valor}", encoding = "utf-8")
        bytes_comprimento = len(dado).to_bytes(2, "big", signed = False)
        return bytes_comprimento + dado
    # code::end


# cadeia de caracteres com prefixo de comprimento
class CampoCadeiaFixo(campo.CampoFixo, CampoCadeiaBasico):
    """
    Classe para inteiro textual com terminador
    """

    def __init__(self, *args, **kwargs):
        CampoCadeiaBasico.__init__(self, "cadeia fixo", **kwargs)
        campo.CampoFixo.__init__(self, *args, **kwargs)

    # code::start para_bytes_fixo
    def para_bytes(self) -> bytes:
        """
        Representação da cadeia de caracteres em uma sequência de
        bytes de comprimento fixo
        :return os bytes da sequência de bytes do dado

        Valores com comprimento maior que o do campo são truncados, enquanto
        os com comprimento menor têm as posições inválidas preenchidas com um
        byte de preenchimento.
        """
        dado = bytes(f"{self.valor}", encoding = "utf-8")[:self.comprimento]
        byte_preenchimento = bytes(self.preenchimento, "latin")
        dado = dado + byte_preenchimento * (self.comprimento - len(dado))
        return dado
    # code::end

