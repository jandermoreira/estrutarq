################################################################################
################################################################################
# Campos reais

from .campo_basico import CampoBasico, CampoTerminador, CampoPrefixado, CampoFixo, \
    CampoBinario
from struct import pack, unpack

################################################################################
################################################################################
# real básico
class CampoRealBasico(CampoBasico):
    """
    Classe básica para campo real
    """

    def __init__(self, tipo: str, valor: int = 0, **kwargs):
        super().__init__(tipo, **kwargs)
        self.valor = valor

    @property
    def valor(self) -> float:
        return self.__valor

    @valor.setter
    def valor(self, valor: (float, int)):
        if not isinstance(valor, (float, int)):
            raise TypeError("O valor deve ser real ou inteiro")
        self.__valor = valor

    def leia(self, arquivo):
        """
        Conversão dos dados lidos para valor inteiro
        :param arquivo: arquivo binário aberto com permissão de leitura
        """
        dado = self.leia_dado_de_arquivo(arquivo)
        self.valor = float(dado)


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
#     # code::start terminador_para_bytes
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
# class CampoIntPrefixado(CampoIntBasico):
#     """Classe para inteiro textual com prefixo de comprimento"""
#
#     def __init__(self):
#         """Construtor"""
#         super().__init__("int prefixado")
#
#     # code::start prefixado_para_bytes
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
#     # code::end
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

#     # code::start fixo_para_bytes
#     def para_bytes(self):
#         # todo
#         """Representação do valor em uma sequência de dígitos que formam
#         o valor numérico, terminando como "terminador"
#         """
#         numero_bytes = bytes(
#             f"{self.valor:{self.__comprimento}d}",
#             encoding = "utf-8")
#         return numero_bytes
#     # code::end
#
# inteiro binário

class CampoRealBinario(CampoBinario, CampoRealBasico):
    """
    Classe para real em formato binário usando IEEE 754 de precisão dupla
    """

    def __init__(self, nome: str, **kwargs):
        CampoRealBasico.__init__(self, nome, "real binário", **kwargs)
        CampoBinario.__init__(self, len(pack("d", 0)))

    # code::start binario_para_bytes
    def para_bytes(self):
        """
        Conversão do valor real para representação floating point de
        precisão dupla
        :return: o valor real no padrão IEEE 754 de precisão dupla
        """
        return pack("d", self.valor)
    # code::end

    # code::start binario_leia
    def leia(self, arquivo):
        """
        Conversão dos dados lidos de bytes para IEEE 754 de precisão dupla
        :param arquivo: arquivo binário aberto com permissão de leitura
        """
        dado = self.leia_dado_de_arquivo(arquivo)
        self.valor = unpack("d", dado)[0]
    # code::end
