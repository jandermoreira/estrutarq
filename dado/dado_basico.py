class DadoBinario:
    """
    Classe para dado binários com um determinado número de bytes
    """

    def __init__(self, comprimento: int):
        self.comprimento = comprimento

    @property
    def comprimento(self):
        return self.__comprimento

    @comprimento.setter
    def comprimento(self, valor):
        if not isinstance(valor, int):
            raise AttributeError("O comprimento do campo deve ser inteiro")
        if valor <= 0:
            raise AttributeError("O comprimento deve ser maior ou igual a um")
        self.__comprimento = valor

    # code::start leitura_binario
    def leia_dado_de_arquivo(self, arquivo) -> bytes:
        """
        Recuperação dos bytes gravados no arquivo
        :param arquivo: arquivo binário aberto com permissão de leitura
        :return: a sequência de bytes lidos
        """
        dado = arquivo.read(self.comprimento)
        if len(dado) < self.comprimento:
            raise EOFError
        else:
            return dado
    # code::end


class DadoFixo:
    """
    Classe dado de comprimento fixo
    """

    def __init__(self, comprimento: int, preenchimento = '\xFF'):
        self.comprimento = comprimento
        self.preenchimento = preenchimento

    @property
    def comprimento(self):
        return self.__comprimento

    @comprimento.setter
    def comprimento(self, comprimento: int):
        if not isinstance(comprimento, int):
            raise AttributeError("O comprimento de campo deve ser inteiro")
        if comprimento <= 0:
            raise AttributeError("O comprimento mínimo para o campo é um byte")
        self.__comprimento = comprimento

    @property
    def preenchimento(self) -> str:
        return self.__preenchimento

    @preenchimento.setter
    def preenchimento(self, preenchimento: str):
        """
        Determina o caractere que será usado como preenchimento de
        campo
        :param preenchimento: um caractere que será traduzido para
        o preenchimento com um único byte

        A conversão é feita usando o conjunto de caracteres Latin, que
        mapeia qualquer caractere para um único byte. Havendo mais que
        um caractere cadeia de entrada, somente o primeiro será considerado.
        """
        if not isinstance(preenchimento, str):
            raise AttributeError("O preenchimento deve ser str"
                                 f" (não '{type(preenchimento).__name__}')")
        preenchimento_bytes = bytes(preenchimento[0], 'latin')
        if len(preenchimento_bytes) != 1:
            raise AttributeError("O preenchimento deve ser um único byte")
        self.__preenchimento = preenchimento[0]

    # code::start leitura_fixo
    def leia_dado_de_arquivo(self, arquivo) -> bytes:
        """
        Leitura de um único dado de comprimento fixo
        :param arquivo: arquivo binário aberto com permissão de leitura
        :return: os bytes do campo

        Os bytes de preenchimento que existirem são removidos.
        """
        dado = arquivo.read(self.comprimento)
        if len(dado) != self.comprimento:
            raise EOFError
        else:
            return dado.replace(bytes(self.preenchimento, "latin"), b"")
    # code::end


class DadoPrefixado:
    """
    Classe dado prefixados pelo seu comprimento
    """

    # code::start leitura_prefixado
    @staticmethod
    def leia_dado_de_arquivo(arquivo) -> bytes:
        """
        Leitura de um único dado prefixado pelo comprimento.
        :param arquivo: arquivo binário aberto com permissão de leitura
        :return: os bytes do dado

        O comprimento é armazenado como um inteiro de 2 bytes, big-endian.
        Em caso de falha na leitura é lançada a exceção EOFError
        """
        bytes_comprimento = arquivo.read(2)
        if len(bytes_comprimento) == 0:
            raise EOFError
        else:
            comprimento = int.from_bytes(bytes_comprimento, "big",
                                         signed = False)
            dado = arquivo.read(comprimento)
            if len(dado) != comprimento:
                raise EOFError
            else:
                return dado
    # code::end


class DadoTerminador:
    """
    Classe para implementação de campos com terminador
    """

    def __init__(self, terminador: str = "\x00"):
        self.terminador = terminador

    @property
    def terminador(self) -> str:
        return self.__terminador

    @terminador.setter
    def terminador(self, terminador: str):
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

    # code::start leitura_terminador
    def leia_dado_de_arquivo(self, arquivo) -> bytes:
        """
        Leitura de um único campo com terminador
        :param arquivo: arquivo binário aberto com permissão de leitura
        :return: os bytes do campo sem o terminador

        Em caso de falha na leitura é lançada a exceção EOFError
        """
        achou_terminador = False
        byte_terminador = bytes(f"{self.terminador}", "latin")
        dado = b""
        while not achou_terminador:
            byte_lido = arquivo.read(1)  # byte a byte
            if len(byte_lido) == 0:
                raise EOFError
            elif byte_lido == byte_terminador:
                achou_terminador = True
            else:
                dado += byte_lido

        return dado
    # code::end
