################################################################################
################################################################################
#  Implementação de campos

################################################################################
################################################################################

from copy import copy


class CampoBasico:
    """
    Estruturação básica do campo como menor unidade de informação.
    """

    valor = ""

    def __init__(self, nome: str, tipo: str):
        self.nome = nome
        self.__tipo = tipo

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, valor):
        if not isinstance(valor, str):
            raise TypeError("Nome do campo deve ser uma cadeia de caracteres.")
        self.__nome = valor

    @property
    def tipo(self):
        return self.__tipo

    def para_bytes(self) -> bytes:
        pass

    @staticmethod
    def leia_dado_de_arquivo(arquivo) -> bytes:
        pass

    def escreva(self, arquivo):
        pass

    def __str__(self):
        """
        Valor padrão do campo para um 'print'
        :return: o valor do campo
        """
        return str(self.valor)

    def copy(self):
        """
        Cópia "rasa" deste campo
        :return: outra instância com os mesmos valores
        """
        return copy(self)


class CampoBruto(CampoBasico):
    """
    Implementação das funções de um campo bruto, ou seja, sem organização
    de campo. O valor é sempre armazenado como cadeia de caracteres.
    """

    def __init__(self, nome: str, valor = ""):
        super().__init__(nome, "bruto")
        self.valor = valor

    @property
    def valor(self):
        return self.__valor

    @valor.setter
    def valor(self, valor):
        """
        O valor armazenado para o campo básico (i.e., bruto) é sempre uma
        cadeia de caracteres
        :param valor: um valor qualquer
        """
        self.__valor = str(valor)

    # code::start bruto_para_bytes
    def para_bytes(self) -> bytes:
        """
        Conversão para bytes feita para o conteúdo bruto com conjunto de
        caracteres UTF-8
        :return: os bytes do valor textual armazenado
        """
        return bytes(self.valor, "utf-8")

    # code::end

    # code::start escreva
    def escreva(self, arquivo):
        """
        Gravação do conteúdo do campo em um arquivo
        :param arquivo: arquivo binário aberto com permissão de escrita
        """
        arquivo.write(self.para_bytes())
    # code::end
