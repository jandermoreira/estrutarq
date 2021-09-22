"""
Registros
"""

from estrutarq.campo import CampoBasico


class RegistroBruto:
    """
    Classe básica para registro, com controle exclusivamente pelo número
    de campos
    """

    def __init__(self):
        self.__tipo = "bruto"
        self.__lista_campos = []

    @property
    def tipo(self):
        return self.__tipo

    def adicione_campo(self, campo: CampoBasico):
        if not isinstance(campo, CampoBasico):
            raise TypeError("Esperado um campo para o registro")
        self.__lista_campos.append(campo)

    # code::start bruto_escreva
    def escreva(self, arquivo):
        """
        Escrita do registro no arquivo pela escrita sucessiva dos campos
        :param arquivo: arquivo binário aberto com permissão de escrita
        """
        for campo in self.__lista_campos:
            campo.escreva(arquivo)

    # code::end

    # code::start bruto_leia
    def leia(self, arquivo):
        """
        Leitura do registro do arquivo pela recuperação sucessiva de cada
        campo
        :param arquivo: arquivo binário aberto com permissão de leitura
        """
        for campo in self.__lista_campos:
            campo.leia(arquivo)
    # code::end
