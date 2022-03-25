import re
from abc import ABCMeta, abstractmethod
from typing import BinaryIO


class DadoBasico(metaclass = ABCMeta):
    """
    Classe básica para dados
    """

    byte_enchimento = b"\x1b"  # ESC

    def __init__(self):
        self._comprimento_fixo = False

    # code::start basico_enchimento_bytes
    def enchimento_de_bytes(self, sequencia: bytes, lista_bytes) -> bytes:
        """
        Operação de enchimento de bytes (byte stuffing)
        :param sequencia: a sequência de bytes a ser "enchida"
        :param lista_bytes: os bytes especiais que serão "escapados"
        :return: a sequência original enchida
        """
        lista_bytes.append(self.byte_enchimento)
        sequencia_enchida = b''
        for single_byte in [bytes([b]) for b in sequencia]:
            if single_byte in lista_bytes:
                sequencia_enchida += self.byte_enchimento + single_byte
            else:
                sequencia_enchida += single_byte
        return sequencia_enchida

    def esvaziamento_de_bytes(self, sequencia: bytes) -> bytes:
        """
        Operação de esvaziamento de bytes (byte un-stuffing)
        :param sequencia: a sequência de bytes a ser "esvaziada"
        :return: a sequência sem o enchimento
        """
        padrao = self.byte_enchimento + rb"(.)"
        sequencia_esvaziada = re.sub(padrao, rb"\1", sequencia)
        return sequencia_esvaziada

    # code::end

    def varredura_com_enchimento(self, sequencia: bytes,
                                 referencia: bytes) -> (bytes, bytes):
        """
        Recuperação de um dado individual de uma sequência de bytes,
        retornando o dado até um byte de referência (não "enchido") e o
        restante da sequência depois desse byte
        :param sequencia: uma sequência de bytes
        :param referencia: byte simples usado como sentinela (terminador)
        :return: o restante da sequência
        """
        achou_referencia = False
        achou_enchimento = False
        dado = b""
        posicao = 0
        while not achou_referencia and posicao < len(sequencia):
            byte_atual = bytes([sequencia[posicao]])
            if byte_atual == referencia and not achou_enchimento:
                achou_referencia = True
            achou_enchimento = (byte_atual == self.byte_enchimento
                                and not achou_enchimento)
            dado += byte_atual
            posicao += 1
        if bytes([dado[-1]]) != referencia:
            raise ValueError("Byte de referência não encontrado na sequência.")
        sequencia_restante = sequencia[posicao:]
        return dado, sequencia_restante

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
        Recuperação de um dado extraído de uma sequência de bytes,
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
        :return: a sequência após extraídos os bytes de organização
        """
        pass


class DadoBruto(DadoBasico):
    """
    Classe para dado bruto
    """

    def __init__(self):
        DadoBasico.__init__(self)

    def leia_de_arquivo(self, arquivo: BinaryIO) -> bytes:
        """
        Recuperação de um dado lido de um arquivo (inviável para
        dado bruto)
        :param arquivo: arquivo binário aberto com permissão de leitura
        """
        raise NotImplemented("A leitura de dado bruto é inviável.")

    def leia_de_bytes(self, sequencia: bytes):
        """
        Recuperação de um dado extraído de uma sequência de bytes
        (inviável para dado bruto)
        :param sequencia: sequência de bytes
        """
        raise NotImplemented("A leitura de dado bruto é inviável.")

    def adicione_formatacao(self, dado: bytes) -> bytes:
        """
        Acrescenta aos bytes do dado a organização de dados em uso.
        Para dado bruto, apenas repassa o dado sem modificação
        :param dado: bytes do dado
        :return: bytes do dado inalterados
        """
        return dado

    def remova_formatacao(self, sequencia: bytes) -> bytes:
        """
        Remove da sequência de bytes de organização. Para dado bruto,
        apenas repassa a sequência sem modificação
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
        DadoBasico.__init__(self)
        self._comprimento = comprimento
        self._comprimento_fixo = True

    @property
    def _comprimento(self) -> int:
        return self.__comprimento

    @_comprimento.setter
    def _comprimento(self, valor: int):
        if not isinstance(valor, int):
            raise AttributeError(
                "O comprimento do campo deve ser inteiro")
        if valor <= 0:
            raise AttributeError(
                "O comprimento deve ser maior ou igual a um")
        self.__comprimento = valor

    # code::start binario_leitura_de_arquivo
    def leia_de_arquivo(self, arquivo: BinaryIO) -> bytes:
        """
        Recuperação dos bytes do valor binário a partir de um arquivo
        :param arquivo: arquivo binário aberto com permissão de leitura
        :return: a sequência de bytes lidos
        """
        dado = arquivo.read(self._comprimento)
        if len(dado) < self._comprimento:
            raise EOFError
        else:
            return dado

    # code::end

    def leia_de_bytes(self, sequencia: bytes) -> (bytes, bytes):
        """
        Recuperação de um dado binário de comprimento definido a partir de
        uma sequência de bytes
        :param sequencia: sequência de bytes
        :return: tupla com os bytes do dado, removidos os bytes de organização
            de dados, e a sequência de bytes restante
        """
        if len(sequencia) < self._comprimento:
            raise TypeError("A sequência não possui bytes suficientes")
        dado = sequencia[:self._comprimento]
        sequencia_restante = sequencia[self._comprimento:]
        return dado, sequencia_restante

    # code::start binario_formatacoes
    def adicione_formatacao(self, dado: bytes) -> bytes:
        """
        Formatação do dado: apenas repassa o dado binário
        :param dado: valor binário
        :return: o dado formatado
        """
        if len(dado) != self._comprimento:
            raise TypeError("O dado não possui o comprimento correto")
        return dado

    def remova_formatacao(self, sequencia: bytes) -> bytes:
        """
        Desformatação do dado: apenas repassa o dado binário
        :param sequencia: bytes de dados
        :return: o dado sem a formatação
        """
        if len(sequencia) != self._comprimento:
            raise TypeError("A sequência de dados não possui o "
                            "comprimento correto")
        return sequencia
    # code::end


class DadoFixo(DadoBasico):
    """
    Classe dado de comprimento fixo
    """

    def __init__(self, comprimento: int, preenchimento = b'\xFF'):
        DadoBasico.__init__(self)
        self._comprimento = comprimento
        self.preenchimento = preenchimento
        self._comprimento_fixo = True

    @property
    def _comprimento(self):
        return self.__comprimento

    @_comprimento.setter
    def _comprimento(self, comprimento: int):
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
        dado = arquivo.read(self._comprimento)
        if len(dado) != self._comprimento:
            raise EOFError
        else:
            return self.remova_formatacao(dado)

    # code::end

    def leia_de_bytes(self, sequencia: bytes) -> (bytes, bytes):
        """
        Recuperação de um dado individual de uma sequência de bytes,
        retornando o dado sem os bytes de preenchimento e o restante da
        sequência
        :param sequencia: uma sequência de bytes
        :return: tupla com os bytes do dado, removidos os bytes de organização
            de dados, e a sequência de bytes restante
        """
        sequencia_restante = sequencia[self._comprimento:]
        sequencia = sequencia[:self._comprimento] + self.preenchimento
        dado_limpo = self.varredura_com_enchimento(sequencia,
                                                   self.preenchimento)[0][:-1]
        return self.esvaziamento_de_bytes(dado_limpo), sequencia_restante

    # code::start fixo_formatacoes
    def adicione_formatacao(self, dado: bytes) -> bytes:
        """
        Formatação do dado: ajusta o dado para o comprimento definido,
        truncando ou adicionando o byte de preenchimento
        :param dado: valor do dado
        :return: o dado formatado no comprimento especificado
        """
        dado_enchimento = self.enchimento_de_bytes(dado, [self.preenchimento])
        dado_restrito = dado_enchimento[:self._comprimento]
        dado_efetivo = (dado_restrito + self.preenchimento *
                        (self._comprimento - len(dado_restrito)))
        dado_recuperado = self.remova_formatacao(dado_efetivo)
        if dado_recuperado != dado[:len(dado_recuperado)]:
            print(self)
            print(dado, 'dado')
            print(dado_enchimento, 'enchimento')
            print(dado_recuperado, 'recuperado')
            raise ValueError("Truncamento nos dados gerou corrupção.")
        return dado_efetivo

    def remova_formatacao(self, sequencia: bytes) -> bytes:
        """
        Desformatação do dado: remoção de caracteres de preenchimento
        :param sequencia: bytes de dados
        :return: dado efetivo, sem preenchimento
        """
        # if len(sequencia) != self.comprimento:
        #     raise TypeError(
        #     "A sequência de dados tem comprimento incorreto.")
        return self.leia_de_bytes(sequencia)[0]
        # code::end


class DadoPrefixado(DadoBasico):
    """
    Classe dado prefixados pelo seu comprimento
    """

    def __init__(self):
        DadoBasico.__init__(self)

    # code::start prefixado_leitura_de_arquivo
    def leia_de_arquivo(self, arquivo: BinaryIO) -> bytes:
        """
        Leitura de um único dado prefixado pelo comprimento
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
        DadoBasico.__init__(self)
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
        achou_enchimento = False
        dado = b""
        while not achou_terminador:
            byte_lido = arquivo.read(1)  # byte a byte
            if len(byte_lido) == 0:
                raise EOFError
            if byte_lido == self.terminador and not achou_enchimento:
                achou_terminador = True
            achou_enchimento = (byte_lido == self.byte_enchimento
                                and not achou_enchimento)
            dado += byte_lido
        dado_limpo = self.remova_formatacao(dado)
        return dado_limpo

    # code::end

    def leia_de_bytes(self, sequencia: bytes) -> (bytes, bytes):
        """
        Recuperação de um dado individual de uma sequência de bytes,
        retornando o dado até o terminador e o restante da sequência depois
        do terminador
        :param sequencia: uma sequência de bytes
        :return: o restante da sequência
        """
        bytes_dados, sequencia_restante = \
            self.varredura_com_enchimento(sequencia, self.terminador)
        return self.remova_formatacao(bytes_dados), sequencia_restante

    # code::start terminador_formatacoes
    def adicione_formatacao(self, dado: bytes) -> bytes:
        """
        Formatação do dado: acréscimo do byte terminador e uso de
        'byte stuffing' para incluir o terminador como dado
        :param dado: valor do dado
        :return: o dado formatado
        """
        dado_enchido = self.enchimento_de_bytes(dado, [self.terminador])
        return dado_enchido + self.terminador

    def remova_formatacao(self, sequencia: bytes) -> bytes:
        """
        Desformatação do dado: remoção de byte terminador
        :param sequencia: bytes de dados
        :return: dado efetivo, sem terminador
        """
        sequencia = self.esvaziamento_de_bytes(sequencia)
        if bytes([sequencia[-1]]) != self.terminador:
            raise TypeError("A sequência de bytes não possui o terminador")
        return sequencia[:-1]
    # code::end
