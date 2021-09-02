################################################################################
################################################################################
# Campos reais
import campo


class CampoRealBasico(campo.CampoBasico):
    def atribua(self, valor):
        if type(valor).__name__ != "float":
            raise TypeError("Esperado um valor real (float)")
        else:
            self.__valor = valor


class CampoRealPrefixo(CampoRealBasico):
    def __init__(self):
        super().__init__("real prefixo")
