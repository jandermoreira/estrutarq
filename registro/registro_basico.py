"""
Registros
"""

from estrutarq.campo.campo_basico import CampoBasico


class RegistroBasico:
    """
    Classe básica para registros

    Utiliza @DynamicAttrs
    """

    def __init__(self, tipo: str, *lista_campos):
        self.__tipo = tipo
        self.lista_campos = []
        self.adicione_campos(*lista_campos)

    @property
    def tipo(self):
        return self.__tipo

    def __adicione_um_campo(self, campo: CampoBasico):
        if not isinstance(campo, CampoBasico):
            raise TypeError("Esperado um campo para o registro")
        setattr(self, campo.nome, campo.copy())
        self.lista_campos.append(getattr(self, campo.nome))

    def adicione_campos(self, *lista_campos):
        for campo in lista_campos:
            self.__adicione_um_campo(campo)

    def escreva(self, arquivo):
        pass

    def leia(self, arquivo):
        pass


class RegistroBruto(RegistroBasico):
    """
    Classe básica para registro, com controle exclusivamente pelo número
    de campos

    Utiliza @DynamicAttrs
    """

    def __init__(self, *lista_campos):
        super().__init__("bruto", *lista_campos)

    # code::start bruto_escreva
    def escreva(self, arquivo):
        """
        Escrita do registro no arquivo pela escrita sucessiva dos campos
        :param arquivo: arquivo binário aberto com permissão de escrita
        """
        for i, campo in enumerate(self.lista_campos):
            campo.escreva(arquivo)

    # code::end

    # code::start bruto_leia
    def leia(self, arquivo):
        """
        Leitura do registro do arquivo pela recuperação sucessiva de cada
        campo
        :param arquivo: arquivo binário aberto com permissão de leitura
        """
        for campo in self.lista_campos:
            campo.leia(arquivo)
    # code::end
