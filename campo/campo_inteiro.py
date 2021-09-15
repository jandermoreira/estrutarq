################################################################################
################################################################################
# Campos inteiros

from .campo_basico import CampoBasico, CampoTerminador, CampoPrefixado, CampoFixo, \
    CampoBinario


################################################################################
################################################################################
# inteiro básico
class CampoIntBasico(CampoBasico):
    """
    Classe básica para campo inteiro
    """

    def __init__(self, tipo: str, valor: int = 0, **kwargs):
        super().__init__(tipo, **kwargs)
        self.valor = valor

    @property
    def valor(self) -> int:
        return self.__valor

    @valor.setter
    def valor(self, valor: int):
        if not isinstance(valor, int):
            raise TypeError("O valor deve ser inteiro")
        self.__valor = valor

    def leia(self, arquivo):
        """
        Conversão dos dados lidos para valor inteiro
        :param arquivo: arquivo binário aberto com permissão de leitura
        """
        dado = self.leia_dado_de_arquivo(arquivo)
        self.valor = int(dado)




# inteiro textual com terminador
class CampoIntTerminador(CampoTerminador, CampoIntBasico):
    """
    Classe para inteiro textual com terminador
    """

    def __init__(self, terminador: str = "\x00", valor: int = 0):
        super().__init__("int terminador")
        self.terminador = terminador
        self.valor = valor

    # code::start terminador_para_bytes
    def para_bytes(self) -> bytes:
        """
        Representação do valor em uma sequência de dígitos que formam
        o valor numérico finalizado com o terminador
        """
        dado = bytes(f"{self.valor}", encoding = "utf-8")
        byte_terminador = bytes(f"{self.terminador}", "latin")
        return dado + byte_terminador
    # code::end


# inteiro com prefixo de comprimento
class CampoIntPrefixado(CampoIntBasico):
    """Classe para inteiro textual com prefixo de comprimento"""

    def __init__(self):
        """Construtor"""
        super().__init__("int prefixado")

    # code::start prefixado_para_bytes
    def para_bytes(self):
        """
        Representação do valor em uma sequência de bytes
        2 bytes de prefixo em binário com o número de dígitos (little endian)
        sequência de dígitos que formam o valor numérico, com "-" se negativo
        :return: sequência de bytes com o prefixo binário e os bytes do campo
        """
        numero_bytes = bytes(f"{self._CampoBasico__valor}", encoding = "utf-8")
        prefixo_binario = len(numero_bytes).to_bytes(2, "big")
        return prefixo_binario + numero_bytes
    # code::end

    def leia(self, arquivo):
        """
        Recuperação do conteúdo do campo de um arquivo
        :param arquivo:
        :return:
        """
        arquivo.read(2)


# inteiro de comprimento fixo
class CampoIntFixo(CampoIntBasico):
    """Classe para inteiro textual com tamanho fixo"""

    def __init__(self, comprimento):
        """Construtor"""
        super().__init__("int fixo")
        self.__comprimento = comprimento

    # code::start fixo_para_bytes
    def para_bytes(self):
        # todo
        """Representação do valor em uma sequência de dígitos que formam
        o valor numérico, terminando como "terminador"
        """
        numero_bytes = bytes(
            f"{self.valor:{self.__comprimento}d}",
            encoding = "utf-8")
        return numero_bytes
    # code::end

class CampoIntBinario(CampoBinario, CampoIntBasico):
    """
    Classe para inteiro em formato binário (big endian) com 8 bytes
    e complemento para 2 para valores negativos
    """

    numero_bytes = 8  # 8 bytes

    def __init__(self, **kwargs):
        CampoIntBasico.__init__(self, "inteiro binário", **kwargs)
        CampoBinario.__init__(self, self.numero_bytes)

    # code::start binario_para_bytes
    def para_bytes(self):
        """
        Conversão do inteiro para representação do valor em binário
        (big endian) de 8 bytes com sinal
        :return: o valor inteiro em 8 bytes
        """
        return self.valor.to_bytes(self.numero_bytes, "big", signed = True)

    # code::end

    # code::start binario_leia
    def leia(self, arquivo):
        """
        Conversão dos dados lidos de bytes para inteiro
        :param arquivo: arquivo binário aberto com permissão de leitura
        """
        dado = self.leia_dado_de_arquivo(arquivo)
        self.valor = int.from_bytes(dado, "big", signed = True)
    # code::end