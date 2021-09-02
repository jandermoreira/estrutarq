################################################################################
################################################################################
# Campos inteiros

import campo


################################################################################
################################################################################
# inteiro básico
class CampoIntBasico(campo.CampoBasico):
    """
    Classe básica para campo inteiro
    """

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


#
#
# # inteiro textual com terminador
# class CampoIntTerminador(CampoTerminador, CampoIntBasico):
#     """
#     Classe para inteiro textual com terminador
#     """
#
#     def __init__(self, terminador: str = "\x00", valor: int = 0):
#         super().__init__("int terminador")
#         self.terminador = terminador
#         self.valor = valor
#
#     # code::start inteiro_textual_terminador
#     def para_bytes(self) -> bytes:
#         """
#         Representação do valor em uma sequência de dígitos que formam
#         o valor numérico finalizado com o terminador
#         """
#         dado = bytes(f"{self.valor}", encoding = "utf-8")
#         byte_terminador = bytes(f"{self.terminador}", "latin")
#         return dado + byte_terminador
#     # code::end
#

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
# inteiro binário
class CampoIntBinario(CampoIntBasico):
    """Classe para inteiro em formato binário (little endian) com 8 bytes
    e complemento para 2 para valores negativos; transbordo resulta em -1
    """

    def __init__(self):
        """Construtor"""
        super().__init__("int binário")

    def para_bytes(self):
        """Representação do valor em binário (little endian) de 8 bytes"""
        return self.valor.to_bytes(8, "little", signed = True)
