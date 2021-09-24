"""
Registros
"""

from estrutarq.campo.campo_comum import CampoBasico
from estrutarq.dado import DadoPrefixado, DadoTerminador

terminador_de_registro = "\x01"


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

    def de_bytes(self, dados_registro: bytes):
        """
        Obtenção dos bytes de cada campo a partir dos bytes do registro inteiro
        :param dados_registro: sequência de bytes do registro
        """
        dados_restantes = dados_registro
        for campo in self.lista_campos:
            dado_campo, dados_restantes = campo.leia_dados_de_buffer(
                dados_restantes)
            campo.de_bytes(dado_campo)

    # code::start para_bytes
    def para_bytes(self) -> bytes:
        """
        Criação do registro pela concatenação dos bytes dos campos,
        sucessivamente
        :return: sequência dos bytes dos campos
        """
        dado_campos = bytes()
        for campo in self.lista_campos:
            dado_campos += campo.para_bytes()
        return dado_campos

    # code::end

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
        Escrita do registro no arquivo após a concatenação dos bytes de
        cada campo
        :param arquivo: arquivo binário aberto com permissão de escrita
        """
        arquivo.write(self.para_bytes())

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


class RegistroPrefixado(DadoPrefixado, RegistroBasico):
    """
    Classe para registros prefixados pelo comprimento
    """

    def __init__(self, *lista_campos):
        RegistroBasico.__init__(self, "prefixado", *lista_campos)
        DadoPrefixado.__init__(self)

    def escreva(self, arquivo):
        """
        Escrita de registro, que é montado integralmente, seguido da
        escrita do comprimento total e escrita dos bytes do registro em si
        :param arquivo: arquivo binário aberto com permissão para escrita

        O prefixo é um inteiro binário sem sinal de 2 bytes, big-endian
        """
        dado_campos = self.para_bytes()
        comprimento_campos = len(dado_campos)
        bytes_prefixo = comprimento_campos.to_bytes(2, "big", signed = False)
        arquivo.write(bytes_prefixo + dado_campos)

    def leia(self, arquivo):
        """
        Leitura de um registro do arquivo, com posterior separação dos campos
        :param arquivo: arquivo binário aberto com permissão para leitura
        """
        dado_campos = self.leia_dado_de_arquivo(arquivo)
        for campo in self.lista_campos:
            bytes_campo, dado_campos = campo.leia_dado_de_buffer(dado_campos)
            campo.de_bytes(bytes_campo)


class RegistroTerminador(DadoTerminador, RegistroBasico):
    """
    Classe para registros com terminador
    """

    def __init__(self, *lista_campos):
        RegistroBasico.__init__(self, "terminador", *lista_campos)
        DadoTerminador.__init__(self, terminador_de_registro)