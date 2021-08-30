################################################################################
################################################################################
#  Implementação de campos


################################################################################
################################################################################
# Campo básico

class CampoBasico:
    """
    Estruturação básica do campo como menor unidade de informação
    Implementa as funções de um campo bruto, ou seja, sem organização
    de campo. O valor é sempre armazenado como cadeia de caracteres.
    """

    # Atributos
    @property
    def tipo(self):
        return self.__tipo

    def _obtenha_valor(self):
        return self.__valor

    def _atribua_valor(self, valor):
        self.__valor = str(valor)

    valor = property(_obtenha_valor, _atribua_valor)

    def __init__(self, tipo = "bruto"):
        if tipo not in relacao_tipo_campos.keys():
            raise TypeError(f"Tipo de campo desconhecido ({tipo})")
        self.__tipo = tipo

    # code::start bruto
    def para_bytes(self):
        """
        Conversão para bytes feita para o conteúdo bruto com conjunto de
        caracteres UTF-8
        :return: os bytes do valor textual armazenado
        """
        return bytes(self.valor, "utf-8")

    def escreva(self, arquivo):
        """
        Gravação do conteúdo do campo em um arquivo
        :param arquivo: arquivo binário aberto com permissão de escrita
        """
        arquivo.write(self.para_bytes())
    # code::end


class CampoTerminador:
    """
    Classe para implementação de campos com terminador
    """

    def _obtenha_terminador(self):
        return self.__terminador

    def _atribua_terminador(self, terminador: str):
        """
        Determina o caractere que será usado como terminador de
        campo
        :param terminador: um caractere que será traduzido para
        o terminador com um único byte

        A conversão é feita usando o conjunto de caracteres Latin, que
        mapeia qualquer caractere para um único byte. Havendo mais que
        um caractere cadeia de entrada, somente o primeiro será considerado.
        """
        if not isinstance(terminador, str):
            raise AttributeError("O terminador deve ser str"
                                 f" (não '{type(terminador).__name__}')")
        terminador_bytes = bytes(terminador[0], 'latin')
        if len(terminador_bytes) != 1:
            raise AttributeError("O terminador deve ser um único byte")
        self.__terminador = terminador[0]

    terminador = property(_obtenha_terminador, _atribua_terminador)

    # code::start leitura_terminador
    def leia_dado_de_arquivo(self, arquivo):
        """
        Leitura de um único campo com terminador
        :param arquivo: arquivo binário aberto com permissão de leitura
        :return: os bytes do campo sem o terminador

        Em caso de falha na leitura é lançada a exceção EOFError
        """
        achou_terminador = False
        dado = b""
        while not achou_terminador:
            byte_lido = arquivo.read(1)  # byte a byte
            if len(byte_lido) == 0:
                raise EOFError
            if byte_lido == bytes(f"{self.terminador}", "latin"):
                achou_terminador = True
            else:
                dado += byte_lido

        return dado
    # code::end


class CampoPrefixado:
    # code::start leitura_prefixado
    @staticmethod
    def leia_dado_de_arquivo(arquivo):
        """
        Leitura de um único campo prefixado pelo comprimento.
        :param arquivo: arquivo binário aberto com permissão de leitura
        :return: os bytes do campo

        O comprimento é armazenado como um inteiro de 2 bytes, big-endian.
        Em caso de falha na leitura é lançada a exceção EOFError
        """
        bytes_comprimento = arquivo.read(2)
        comprimento = int.from_bytes(bytes_comprimento, "big", signed = False)
        if len(bytes_comprimento) == 0:
            raise EOFError
        else:
            dado = arquivo.read(comprimento)
            if len(dado) == comprimento:
                raise EOFError
            else:
                return dado
    # code::end


################################################################################
################################################################################
# Campos inteiros

# inteiro básico
class CampoIntBasico(CampoBasico):
    """
    Classe básica para campo inteiro
    """

    def _obtenha_valor(self):
        return self.__valor

    def _atribua_valor(self, valor: int):
        if not isinstance(valor, int):
            raise TypeError("O valor deve ser inteiro")
        self.__valor = valor

    valor = property(_obtenha_valor, _atribua_valor)


# inteiro textual com terminador
class CampoIntTerminador(CampoIntBasico, CampoTerminador):
    """
    Classe para inteiro textual com terminador
    """

    def __init__(self, terminador: str = "\x00", valor: int = 0):
        super().__init__("int terminador")
        self.terminador = terminador
        self.valor = valor

    # code::start inteiro_textual_terminador
    def para_bytes(self):
        """
        Representação do valor em uma sequência de dígitos que formam
        o valor numérico finalizado com o terminador
        """
        dado = bytes(f"{self.valor}", encoding = "utf-8")
        byte_terminador = bytes(f"{self.terminador}", "latin")
        return dado + byte_terminador

    def leia_de_arquivo(self, arquivo):
        """
        Conversão dos dados lidos para valor inteiro
        :param arquivo: arquivo binário aberto com permissão de leitura
        """
        dado = self.leia_dado_de_arquivo(arquivo)
        self.valor = int(dado)
    # code::end


# # inteiro com prefixo de comprimento
# class CampoIntPrefixo(CampoIntBasico):
#     """Classe para inteiro textual com prefixo de comprimento"""
#
#     def __init__(self):
#         """Construtor"""
#         super().__init__("int prefixo")
#
#     def para_bytes(self):
#         """
#         Representação do valor em uma sequência de bytes
#         2 bytes de prefixo em binário com o número de dígitos (little endian)
#         sequência de dígitos que formam o valor numérico, com "-" se negativo
#         :return: sequência de bytes com o prefixo binário e os bytes do campo
#         """
#         numero_bytes = bytes(f"{self._CampoBasico__valor}", encoding = "utf-8")
#         prefixo_binario = len(numero_bytes).to_bytes(2, "big")
#         return prefixo_binario + numero_bytes
#
#     def leia(self, arquivo):
#         """
#         Recuperação do conteúdo do campo de um arquivo
#         :param arquivo:
#         :return:
#         """
#         arquivo.read(2)
#
#
# # inteiro de comprimento fixo
# class CampoIntFixo(CampoIntBasico):
#     """Classe para inteiro textual com tamanho fixo"""
#
#     def __init__(self, comprimento):
#         """Construtor"""
#         super().__init__("int fixo")
#         self.__comprimento = comprimento
#
#     def para_bytes(self):
#         # todo
#         """Representação do valor em uma sequência de dígitos que formam
#         o valor numérico, terminando como "terminador"
#         """
#         numero_bytes = bytes(
#             f"{self.valor:{self.__comprimento}d}",
#             encoding = "utf-8")
#         return numero_bytes
#
#
# # inteiro binário
# class CampoIntBinario(CampoIntBasico):
#     """Classe para inteiro em formato binário (little endian) com 8 bytes
#     e complemento para 2 para valores negativos; transbordo resulta em -1
#     """
#
#     def __init__(self):
#         """Construtor"""
#         super().__init__("int binário")
#
#     def para_bytes(self):
#         """Representação do valor em binário (little endian) de 8 bytes"""
#         return self._CampoBasico__valor.to_bytes(8, "little", signed = True)
#
#
# ################################################################################
# ################################################################################
# # Campos reais
#
# class CampoRealBasico(CampoBasico):
#     def atribua(self, valor):
#         if type(valor).__name__ != "float":
#             raise TypeError("Esperado um valor real (float)")
#         else:
#             self._CampoBasico__valor = valor
#
#
# class CampoRealPrefixo(CampoRealBasico):
#     def __init__(self):
#         super().__init__("real prefixo")


################################################################################
################################################################################
# Campos de cadeias de caracteres

# cadeia de caracteres básica
class CampoCadeiaBasico(CampoBasico):
    """
    Classe básica para cadeias de caracteres
    """

    def _obtenha_valor(self):
        return self.__valor

    def _atribua_valor(self, valor: int):
        if not isinstance(valor, str):
            raise TypeError("O valor deve ser uma cadeia de caracteres")
        self.__valor = valor

    valor = property(_obtenha_valor, _atribua_valor)


# cadeia de caracteres com terminador
class CampoCadeiaTerminador(CampoCadeiaBasico, CampoTerminador):
    """
    Classe para inteiro textual com terminador
    """

    def __init__(self, terminador: str = "\x00", valor: int = 0):
        super().__init__("cadeia terminador")
        self.terminador = terminador
        self.valor = valor

    # code::start inteiro_textual_terminador
    def para_bytes(self):
        """
        Representação da cadeia de caracteres em uma sequência de
        bytes finalizada com terminador
        :return '
        """
        dado = bytes(f"{self.valor}", encoding = "utf-8")
        byte_terminador = bytes(f"{self.terminador}", "latin")

        # Eliminação do byte terminador do conjunto de dados
        if byte_terminador != b'_':
            byte_substituicao = b'_'
        else:
            byte_substituicao = b'*'
        dado = dado.replace(byte_terminador, byte_substituicao)

        return dado + byte_terminador

    def leia_de_arquivo(self, arquivo):
        """
        Conversão dos dados lidos para valor inteiro
        :param arquivo: arquivo binário aberto com permissão de leitura
        """
        dado = self.leia_dado_de_arquivo(arquivo)
        self.valor = int(dado)
    # code::end


################################################################################
################################################################################
# Interface

relacao_tipo_campos = {
    "bruto": CampoBasico,
    "int terminador": CampoIntTerminador,
    # "int prefixo": CampoIntPrefixo,
    # "int binário": CampoIntBinario,
    # "int fixo": CampoIntFixo,
    # "real prefixo": CampoRealPrefixo,
}


def crie_campo(tipo, *args, **kwargs):
    if tipo not in relacao_tipo_campos.keys():
        raise TypeError(f"Tipo de campo desconhecido ({tipo})")
    else:
        return relacao_tipo_campos[tipo](*args, **kwargs)
