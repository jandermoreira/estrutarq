class DadoBasico:
    """
    Classe básica para dados
    """

    def dado_de_bytes(self, dado: bytes) -> bytes:
        pass

    def dado_para_bytes(self) -> bytes:
        pass


class DadoBinario(DadoBasico):
    """
    Classe para dados binários com um determinado número de bytes
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

    def leia_dado_de_buffer(self, buffer: bytes) -> (bytes, bytes):
        """
        Recuperação de um dado individual de um buffer que será varrido,
        retornando o dado e o restante do buffer
        :param buffer: uma sequência de bytes
        :return: o restante do buffer
        """
        dado = buffer[:self.comprimento]
        buffer_restante = buffer[self.comprimento + 1:]
        return dado, buffer_restante

    @staticmethod
    def formate_dado(dado: bytes):
        """
        Formatação do dado: apenas repassa o dado binário
        :param dado: valor binário
        :return: o dado formatado
        """
        return dado

    @staticmethod
    def desformate_dado(dado):
        """
        Desformatação do dado: apenas repassa o dado binário
        :param dado: bytes de dados
        :return: dado binário
        """
        return dado


class DadoFixo(DadoBasico):
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

    def byte_preenchimento(self) -> bytes:
        """
        O caractere de preenchimento convertido para byte
        :return: o byte de preenchimento
        """
        return bytes(self.preenchimento, 'latin')

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

        self.__preenchimento = preenchimento[0]
        if len(self.byte_preenchimento()) != 1:
            raise AttributeError("O preenchimento deve ser um único byte")

    def leia_dado_de_buffer(self, buffer: bytes) -> (bytes, bytes):
        """
        Recuperação de um dado individual de um buffer que será varrido,
        retornando o dado sem os bytes de preenchimento e o restante do buffer
        :param buffer: uma sequência de bytes
        :return: o restante do buffer
        """
        dado = buffer[:self.comprimento].replace(self.byte_preenchimento(), b"")
        buffer_restante = buffer[self.comprimento + 1:]
        return dado, buffer_restante

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
            return dado.replace(self.byte_preenchimento(), b"")

    # code::end

    def formate_dado(self, dado: bytes):
        """
        Formatação do dado: ajusta o dado para o comprimento definido,
        truncando ou adicionando o byte de preenchimento
        :param dado: valor do dado
        :return: o dado formatado
        """
        dado = dado[: self.comprimento]
        dado = dado + byte_preenchimento() * (self.comprimento - len(dado))
        return dado

    def desformate_dado(self, dado):
        """
        Desformatação do dado: remoção de caracteres de preenchimento
        :param dado: bytes de dados
        :return: dado efetivo, sem preenchimento
        """
        return dado.replace(self.byte_preenchimento(), b"")


class DadoPrefixado(DadoBasico):
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

    @staticmethod
    def leia_dado_de_buffer(buffer: bytes) -> (bytes, bytes):
        """
        Recuperação de um dado individual de um buffer que será varrido,
        retornando o dado sem o prefixo e o restante do buffer
        :param buffer: uma sequência de bytes
        :return: o restante do buffer
        """
        comprimento = int.from_bytes(buffer[:1], "big", signed = False)
        dado = buffer[2:comprimento + 1]
        buffer_restante = buffer[comprimento + 4:]
        return dado, buffer_restante

    @staticmethod
    def formate_dado(dado: bytes):
        """
        Formatação do dado: acréscimo do prefixo binário com comprimento
        (2 bytes, big-endian, sem sinal)
        :param dado: valor do dado
        :return: o dado formatado
        """
        bytes_comprimento = len(dado).to_bytes(2, "big", signed = False)
        return bytes_comprimento + dado

    @staticmethod
    def desformate_dado(dado):
        """
        Desformatação do dado: remoção dos dois bytes do comprimento
        :param dado: bytes de dados
        :return: dado efetivo, sem o prefixo de comprimento
        """
        return dado[2:]


class DadoTerminador(DadoBasico):
    """
    Classe para implementação de campos com terminador
    """

    def __init__(self, terminador: str):
        self.terminador = terminador

    @property
    def terminador(self) -> str:
        return self.__terminador

    def byte_terminador(self):
        """
        Retorna o byte terminador gerado a partir do caractere terminador
        :return:
        """
        return bytes(self.terminador, 'latin')

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
        self.__terminador = terminador[0]
        if len(self.byte_terminador()) != 1:
            raise AttributeError("O terminador deve ser um único byte")

    # code::start leitura_terminador
    def leia_dado_de_arquivo(self, arquivo) -> bytes:
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
            elif byte_lido == self.byte_terminador():
                achou_terminador = True
            else:
                dado += byte_lido

        return dado

    # code::end

    def leia_dado_de_buffer(self, buffer: bytes) -> (bytes, bytes):
        """
        Recuperação de um dado individual de um buffer que será varrido,
        retornando o dado até o terminador e o restante do buffer depois
        do terminador
        :param buffer: uma sequência de bytes
        :return: o restante do buffer
        """
        posicao_terminador = buffer.find(self.byte_terminador())
        dado = buffer[:posicao_terminador]
        buffer_restante = buffer[posicao_terminador + 1:]
        return dado, buffer_restante

    def formate_dado(self, dado: bytes):
        """
        Formatação do dado: acréscimo do byte terminador
        :param dado: valor do dado
        :return: o dado formatado
        """
        return dado + self.byte_terminador()

    @staticmethod
    def desformate_dado(dado):
        """
        Desformatação do dado: remoção de byte terminador
        :param dado: bytes de dados
        :return: dado efetivo, sem terminador
        """
        return dado[:-1]
