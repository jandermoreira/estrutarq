from abc import ABCMeta, abstractmethod
from typing import BinaryIO

class DadoBasico(metaclass = ABCMeta):
    """
    Classe básica para dados
    """

    @abstractmethod
    def leia_de_arquivo(self, arquivo: BinaryIO) -> bytes:
        """
        Recuperação de um dado lido de um arquivo, observando a
        representação do dado e a forma de organização
        :param arquivo: arquivo binário aberto com permissão de leitura
        """
        pass

    @abstractmethod
    def leia_de_bytes(self, sequencia: bytes) -> (bytes, bytes):
        """
        Recuperação de um dado extraído de uma sequencia de bytes,
        retornando os bytes do dado em si e o restante da sequência
        depois da extração do dado, observando a representação do dado
        e a forma de organização
        :param sequencia: sequência de bytes
        :return: tupla com os bytes do dado, removido os bytes de organização
            de dados, a sequência de bytes restante
        """
        pass

    @abstractmethod
    def adicione_formatacao(self, dado: bytes) -> bytes:
        """
        Acrescenta aos bytes do dado a organização de dados em uso
        :param dado: bytes do dado
        :return: bytes do dado acrescida da forma de organização
        """
        pass

    @abstractmethod
    def remova_formatacao(self, sequencia: bytes) -> bytes:
        """
        Remove da sequência de bytes aqueles correspondentes à forma de
        organização
        :param sequencia: uma sequência de bytes
        :return: a sequência depois de extraídos os bytes de organização
        """
        pass

class DadoBruto(DadoBasico):
    """
    Classe para dado bruto
    """
    def leia_de_arquivo(self, arquivo: BinaryIO) -> bytes:
        """
        Recuperação de um dado lido de um arquivo, que é inviável para
        dado bruto
        :param arquivo: arquivo binário aberto com permissão de leitura
        """
        raise NotImplemented("A leitura de dado bruto é inviável.")

    def leia_de_bytes(self, sequencia: bytes):
        """
        Recuperação de um dado extraído de uma sequencia de bytes,
        que é inviável para dado bruto
        :param sequencia: sequência de bytes
        """
        raise NotImplemented("A leitura de dado bruto é inviável.")

    def adicione_formatacao(self, dado: bytes) -> bytes:
        """
        Acrescenta aos bytes do dado a organização de dados em uso.
        Para dado bruto, apenas repassa o dado sem modificação.
        :param dado: bytes do dado
        :return: bytes do dado inalterados
        """
        return dado

    def remova_formatacao(self, sequencia: bytes) -> bytes:
        """
        Remove da sequência de bytes de organização. Para dado bruto,
        apenas repassa a sequência sem modificação.
        :param sequencia: uma sequência de bytes
        :return: a sequência inalterada
        """
        return sequencia


class DadoBinario(DadoBasico):
    """
    Classe para dados binários com um determinado comprimento em bytes
    """

    __comprimento = None

    def __init__(self, comprimento: int):
        self.comprimento = comprimento

    @property
    def comprimento(self) -> int:
        return self.__comprimento

    @comprimento.setter
    def comprimento(self, valor: int):
        if not isinstance(valor, int):
            raise AttributeError("O comprimento do campo deve ser inteiro")
        if valor <= 0:
            raise AttributeError("O comprimento deve ser maior ou igual a um")
        self.__comprimento = valor

    # code::start binario_leitura_de_arquivo
    def leia_de_arquivo(self, arquivo: BinaryIO) -> bytes:
        """
        Recuperação dos bytes do valor binário a partir de um arquivo
        :param arquivo: arquivo binário aberto com permissão de leitura
        :return: a sequência de bytes lidos
        """
        dado = arquivo.read(self.comprimento)
        if len(dado) < self.comprimento:
            raise EOFError
        else:
            return dado

    # code::end

    def leia_de_bytes(self, sequencia: bytes) -> (bytes, bytes):
        """
        Recuperação de um dado binário de comprimento definido a partir de
        uma sequencia de bytes
        :param sequencia: sequência de bytes
        :return: tupla com os bytes do dado, removidos os bytes de organização
            de dados, e a sequência de bytes restante
        """
        if len(sequencia) < self.comprimento:
            raise TypeError("A sequência não possui bytes suficientes")
        dado = sequencia[:self.comprimento]
        sequencia_restante = sequencia[self.comprimento:]
        return dado, sequencia_restante

    # code::start binario_formatacoes
    def adicione_formatacao(self, dado: bytes) -> bytes:
        """
        Formatação do dado: apenas repassa o dado binário
        :param dado: valor binário
        :return: o dado formatado
        """
        if len(dado) != self.comprimento:
            raise TypeError("O dado não possui o comprimento correto")
        return dado

    def remova_formatacao(self, sequencia: bytes) -> bytes:
        """
        Desformatação do dado: apenas repassa o dado binário
        :param sequencia: bytes de dados
        :return: o dado sem a formatação
        """
        if len(sequencia) != self.comprimento:
            raise TypeError("A sequência de dados não possui o "
                            "comprimento correto")
        return sequencia
    # code::end


class DadoFixo(DadoBasico):
    """
    Classe dado de comprimento fixo
    """

    def __init__(self, comprimento: int, preenchimento = b'\xFF'):
        self.comprimento = comprimento
        self.preenchimento = preenchimento

    @property
    def comprimento(self):
        return self.__comprimento

    @comprimento.setter
    def comprimento(self, comprimento: int):
        if not isinstance(comprimento, int):
            raise AttributeError("O comprimento deve ser inteiro")
        if comprimento <= 0:
            raise AttributeError("O comprimento mínimo para é um byte")
        self.__comprimento = comprimento

    @property
    def preenchimento(self) -> bytes:
        return self.__preenchimento

    @preenchimento.setter
    def preenchimento(self, preenchimento: bytes):
        """
        Determina o byte que será usado como preenchimento de
        campo
        :param preenchimento: um byte para preenchimento
        """
        if not isinstance(preenchimento, bytes) \
                or len(preenchimento) != 1:
            raise AttributeError("O byte de preenchimento deve ter um byte")
        self.__preenchimento = preenchimento

    # code::start fixo_leitura_de_arquivo
    def leia_de_arquivo(self, arquivo: BinaryIO) -> bytes:
        """
        Leitura de um único dado de comprimento fixo a partir do arquivo
        :param arquivo: arquivo binário aberto com permissão de leitura
        :return: os bytes do campo

        Os bytes de preenchimento que existirem são removidos.
        """
        dado = arquivo.read(self.comprimento)
        if len(dado) != self.comprimento:
            raise EOFError
        else:
            return self.remova_formatacao(dado)

    # code::end

    def leia_de_bytes(self, sequencia: bytes) -> (bytes, bytes):
        """
        Recuperação de um dado individual de um sequencia de bytes,
        retornando o dado sem os bytes de preenchimento e o restante da
        sequencia
        :param sequencia: uma sequência de bytes
        :return: tupla com os bytes do dado, removidos os bytes de organização
            de dados, e a sequência de bytes restante
        """
        dado = sequencia[:self.comprimento].replace(self.preenchimento, b"")
        sequencia_restante = sequencia[self.comprimento:]
        return dado, sequencia_restante

    # code::start fixo_formatacoes
    def adicione_formatacao(self, dado: bytes) -> bytes:
        """
        Formatação do dado: ajusta o dado para o comprimento definido,
        truncando ou adicionando o byte de preenchimento
        :param dado: valor do dado
        :return: o dado formatado no comprimento especificado
        """
        if dado.find(self.preenchimento) != -1:
            raise TypeError("O byte de preenchimento está presente no dado.")
        dado = dado[:self.comprimento]
        dado = dado + self.preenchimento * (self.comprimento - len(dado))
        return dado

    def remova_formatacao(self, sequencia: bytes) -> bytes:
        """
        Desformatação do dado: remoção de caracteres de preenchimento
        :param sequencia: bytes de dados
        :return: dado efetivo, sem preenchimento
        """
        if len(sequencia) != self.comprimento:
            raise TypeError("A sequência de dados tem comprimento incorreto.")
        return sequencia.replace(self.preenchimento, b"")
    # code::end


class DadoPrefixado(DadoBasico):
    """
    Classe dado prefixados pelo seu comprimento
    """

    # code::start prefixado_leitura_de_arquivo
    def leia_de_arquivo(self, arquivo: BinaryIO) -> bytes:
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

    def leia_de_bytes(self, sequencia: bytes) -> (bytes, bytes):
        """
        Recuperação de um dado individual de uma sequência de bytes,
        retornando o dado sem o prefixo e o restante da sequência
        :param sequencia: uma sequência de bytes
        :return: os bytes de dados e o restante da sequência
        """
        comprimento = int.from_bytes(sequencia[:2], "big", signed = False)
        dado = sequencia[2:comprimento + 2]
        sequencia_restante = sequencia[comprimento + 2:]
        if len(dado) != comprimento:
            raise TypeError("A sequência de bytes não contém bytes suficientes")
        return dado, sequencia_restante

    # code::start prefixado_formatacoes
    def adicione_formatacao(self, dado: bytes) -> bytes:
        """
        Formatação do dado: acréscimo do prefixo binário com comprimento
        (2 bytes, big-endian, sem sinal)
        :param dado: valor do dado
        :return: o dado formatado
        """
        bytes_comprimento = len(dado).to_bytes(2, "big", signed = False)
        return bytes_comprimento + dado

    def remova_formatacao(self, sequencia: bytes) -> bytes:
        """
        Desformatação do dado: remoção dos dois bytes do comprimento
        :param sequencia: bytes de dados
        :return: dado efetivo, sem o prefixo de comprimento
        """
        dado, sequencia_restante = self.leia_de_bytes(sequencia)
        if len(sequencia_restante) != 0:
            raise TypeError("O sequência é mais longa que o tamanho registrado")
        return dado
    # code::end


class DadoTerminador(DadoBasico):
    """
    Classe para implementação de campos com terminador
    """

    def __init__(self, terminador: bytes):
        self.terminador = terminador

    @property
    def terminador(self) -> bytes:
        return self.__terminador

    @terminador.setter
    def terminador(self, terminador: bytes):
        """
        Determina o byte que será usado como terminador
        :param terminador: o byte terminador
        """
        if not isinstance(terminador, bytes) \
                or len(terminador) != 1:
            raise AttributeError("O terminador deve ter um byte")
        self.__terminador = terminador

    # code::start terminador_leitura_de_arquivo
    def leia_de_arquivo(self, arquivo: BinaryIO) -> bytes:
        """
        Leitura de um único dado com terminador
        :param arquivo: arquivo binário aberto com permissão de leitura
        :return: os bytes do dado sem o terminador

        Em caso de falha na leitura é lançada a exceção EOFError
        """
        achou_terminador = False
        dado = b""
        while not achou_terminador:
            byte_lido = arquivo.read(1)  # byte a byte
            if len(byte_lido) == 0:
                raise EOFError
            elif byte_lido == self.terminador:
                achou_terminador = True
            else:
                dado += byte_lido
        return dado

    # code::end

    def leia_de_bytes(self, sequencia: bytes) -> (bytes, bytes):
        """
        Recuperação de um dado individual de um sequencia de bytes,
        retornando o dado até o terminador e o restante do sequencia depois
        do terminador
        :param sequencia: uma sequência de bytes
        :return: o restante do sequencia
        """
        posicao_terminador = sequencia.find(self.terminador)
        if posicao_terminador == -1:
            raise TypeError("Nenhum terminador presente na sequência de bytes")
        dado = sequencia[:posicao_terminador]
        sequencia_restante = sequencia[posicao_terminador + 1:]
        return dado, sequencia_restante

    # code::start terminador_formatacoes
    def adicione_formatacao(self, dado: bytes) -> bytes:
        """
        Formatação do dado: acréscimo do byte terminador
        :param dado: valor do dado
        :return: o dado formatado
        """
        if dado.find(self.terminador) != -1:
            raise TypeError("O byte terminador não pode estar contido no dado")
        return dado + self.terminador

    def remova_formatacao(self, sequencia: bytes) -> bytes:
        """
        Desformatação do dado: remoção de byte terminador
        :param sequencia: bytes de dados
        :return: dado efetivo, sem terminador
        """
        if sequencia.find(self.terminador) != len(sequencia) - 1:
            raise TypeError("A sequência de bytes não possui o terminador")
        return sequencia[:-1]
    # code::end
