"""
Estruturação de dados para armazenamento interno, gravação e leitura, usando
representações diversas:

    * Em representação bruta
    * Com terminador
    * Prefixada pelo comprimento
    * Em formato binário
    * De comprimento fixo predefinido

Licença: GNU GENERAL PUBLIC LICENSE V.3, 2007

Jander Moreira, 2022
"""

from re import sub as regex_sub
from abc import ABCMeta, abstractmethod
from typing import BinaryIO


class DadoBasico(metaclass = ABCMeta):
    """
    Classe básica para armazenamento e manipulação de dados.

    Implementa as operações básicas e define os métodos abstratos.
    """

    byte_enchimento: bytes = b"\x1b"  # ESC
    """
    Contém o byte de escape usado para enchimento (`byte stuffing`). Valor
    padrão: ``ESC`` (hexadecimal ``0x1B``).
    """

    def __init__(self):
        self._comprimento_fixo = False

    # code::start basico_enchimento_bytes
    def enchimento_de_bytes(self, sequencia: bytes,
                            lista_bytes: list[bytes]) -> bytes:
        """
        Operação de enchimento de bytes (`byte stuffing`). Antes de cada item
        de ``lista_bytes`` é acrescentado o byte ``byte_enchimento``.

        :param bytes sequencia: a sequência de bytes a ser "enchida"
        :param list[bytes] lista_bytes: os bytes especiais que serão "escapados"
        :return: a sequência original enchida
        :rtype: bytes
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
        Operação de esvaziamento de bytes (`byte un-stuffing`). Todos os
        enchimentos feitos com ``byte_enchimento`` são removidos.

        :param bytes sequencia: a sequência de bytes a ser "esvaziada"
        :return: a sequência sem os enchimentos
        :rtype: bytes
        """
        padrao = self.byte_enchimento + rb"(.)"
        sequencia_esvaziada = regex_sub(padrao, rb"\1", sequencia)
        return sequencia_esvaziada

    # code::end

    def varredura_com_enchimento(self, sequencia: bytes,
                                 referencia: bytes) -> tuple[bytes, bytes]:
        """
        Recuperação de um dado individual de uma sequência de bytes,
        retornando o dado até um byte de referência (não "enchido") e o
        restante da sequência depois desse byte.

        :param bytes sequencia: uma sequência de bytes
        :param bytes referencia: byte simples usado como sentinela (terminador)
        :return: uma tupla contendo a sequência de bytes até ``referencia``
            e o restante da sequência depois de ``referencia``
        :rtype: tuple[bytes, bytes]
        :raise ValueError: se o byte de referência não estiver presente na
            sequência de bytes
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
        Recuperação de um dado lido de um arquivo, observando a representação
        do dado e a forma de organização. A forma de organização usada é
        removida.

        :param BinaryIO arquivo: arquivo binário aberto com permissão de leitura
        :return: a sequência de bytes lida
        :rtype: bytes
        """
        pass

    @abstractmethod
    def leia_de_bytes(self, sequencia: bytes) -> tuple[bytes, bytes]:
        """
        Recuperação de um dado a partir de uma sequência de bytes, retornando
        os bytes do dado em si e o restante da sequência depois da extração
        do dado, observando a representação do dado e a forma de organização.
        O dado é retornado sem a organização.

        :param bytes sequencia: sequência de bytes
        :return: tupla com os bytes do dado, removidos os bytes de organização
            de dados, e a sequência de bytes restante
        :rtype: tuple[bytes, bytes]
        """
        pass

    @abstractmethod
    def adicione_formatacao(self, dado: bytes) -> bytes:
        """
        Acréscimo da organização de dados em uso aos bytes do dado.

        :param bytes dado: bytes do dado
        :return: bytes do dado acrescido da forma de organização
        :rtype: bytes
        """
        pass

    @abstractmethod
    def remova_formatacao(self, sequencia: bytes) -> bytes:
        """
        Remoção dos bytes correspondentes à forma de organização da sequência
        de bytes.

        :param bytes sequencia: uma sequência de bytes
        :return: a sequência após extraídos os bytes de organização
        :rtype: bytes
        """
        pass


class DadoBruto(DadoBasico):
    """
    Classe para dado em forma bruta, ou seja, sem acréscimo de qualquer forma
    de organização de dados.

    Campos brutos não possuem aplicação prática e são usados apenas para fins
    didáticos.
    """

    def __init__(self):
        DadoBasico.__init__(self)

    def leia_de_arquivo(self, arquivo: BinaryIO):
        """
        Recuperação de um dado lido de um arquivo (inviável para
        dado bruto).

        :param BinaryIO arquivo: arquivo binário aberto com permissão de leitura
        :raise NotImplemented: se o método for acidentalmente chamado
        """
        raise NotImplemented("A leitura de dado bruto é inviável.")

    def leia_de_bytes(self, sequencia: bytes):
        """
        Recuperação de um dado extraído de uma sequência de bytes (inviável
        para dado bruto).

        :param bytes sequencia: sequência de bytes
        :raise NotImplemented: se o método for acidentalmente chamado
        """
        raise NotImplemented("A leitura de dado bruto é inviável.")

    def adicione_formatacao(self, dado: bytes) -> bytes:
        """
        Para dado bruto não há acréscimo de bytes de organização de dados e
        o dado é repassado sem modificação.

        :param bytes dado: bytes do dado
        :return: bytes do dado inalterados
        :rtype: bytes
        """
        return dado

    def remova_formatacao(self, sequencia: bytes) -> bytes:
        """
        Para o dado bruto não há bytes de organização a sequência de bytes é
        repassada sem modificação.

        :param bytes sequencia: uma sequência de bytes
        :return: a sequência inalterada
        :rtype: bytes
        """
        return sequencia


class DadoTerminador(DadoBasico):
    """
    Classe para implementação de dados com terminador. O dado é tratado como
    uma sequência de bytes à qual um byte predefinido
    (:attr:`~.estrutarq.dado.DadoTerminador.terminador`) é
    acrescentado ao final para demarcar o fim dos dados. A existência do
    valor do byte terminador na sequência de dados é tratada com a técnica
    de enchimento de bytes (implementada em
    :class:`~.estrutarq.dado.DadoBasico`).

    :param bytes terminador: um byte a ser usado como terminador
    """

    def __init__(self, terminador: bytes):
        DadoBasico.__init__(self)
        self.terminador = terminador

    @property
    def terminador(self) -> bytes:
        """
        Byte simples usado como terminador.
        """
        return self.__terminador

    @terminador.setter
    def terminador(self, terminador: bytes):
        """
        Determina o byte que será usado como terminador.

        :param terminador: o byte terminador
        """
        if not isinstance(terminador, bytes) \
                or len(terminador) != 1:
            raise AttributeError("O terminador deve ser um único byte")
        self.__terminador = terminador

    # code::start terminador_leitura_de_arquivo
    def leia_de_arquivo(self, arquivo: BinaryIO) -> bytes:
        """
        Leitura de um único dado com terminador. A leitura é feita byte a
        byte até que o byte terminador seja encontrado. Bytes terminadores
        enchidos são restaurados, mas não determinam o fim da busca. O
        enchimento de bytes é removido.

        :param arquivo: arquivo binário aberto com permissão de leitura
        :return: a sequência de bytes do dado sem o terminador
        :raise EOFError: se o fim do arquivo for atingido antes de o byte
            terminador ser encontrado
        """
        achou_terminador = False
        achou_enchimento = False
        dado = b""
        while not achou_terminador:
            byte_lido = arquivo.read(1)  # byte a byte
            if len(byte_lido) == 0:
                raise EOFError("Byte terminador não encontrado no arquivo")
            if byte_lido == self.terminador and not achou_enchimento:
                achou_terminador = True
            achou_enchimento = (byte_lido == self.byte_enchimento
                                and not achou_enchimento)
            dado += byte_lido
        dado_limpo = self.remova_formatacao(dado)
        return dado_limpo

    # code::end

    def leia_de_bytes(self, sequencia: bytes) -> tuple[bytes, bytes]:
        """
        Recuperação de um dado individual de uma sequência de bytes,
        retornando o dado até o terminador e o restante da sequência depois
        do terminador.

        :param bytes sequencia: uma sequência de bytes
        :return: uma tupla contendo os bytes dos dados e a sequência de bytes
            restante, excluindo-se de ambas o terminador
        :rtype: tuple[bytes, bytes]
        """
        bytes_dados, sequencia_restante = \
            self.varredura_com_enchimento(sequencia, self.terminador)
        return self.remova_formatacao(bytes_dados), sequencia_restante

    # code::start terminador_formatacoes
    def adicione_formatacao(self, dado: bytes) -> bytes:
        """
        Formatação do dado: uso de 'byte stuffing' para permitir o byte
        terminador como dado e acréscimo do byte terminador.

        :param bytes dado: sequência de bytes do dado
        :return: a sequência de dados enchida e com o acréscimo do terminador
            ao final
        :rtype: bytes
        """
        dado_enchido = self.enchimento_de_bytes(dado, [self.terminador])
        return dado_enchido + self.terminador

    def remova_formatacao(self, sequencia: bytes) -> bytes:
        """
        Desformatação do dado: remoção dos bytes de enchimento e também do
        byte terminador.

        :param sequencia: sequência de bytes de dados
        :return: sequência de bytes de dados, esvaziada e sem terminador
        :rtype: bytes
        :raise TypeError: se o terminador não estiver presente na sequência
            esvaziada
        """
        sequencia = self.esvaziamento_de_bytes(sequencia)
        if bytes([sequencia[-1]]) != self.terminador:
            raise TypeError("A sequência de bytes não possui o terminador")
        return sequencia[:-1]
    # code::end


class DadoPrefixado(DadoBasico):
    """
    Classe para a implementação de dado prefixado pelo seu comprimento.
    O prefixo é um valor inteiro binário de 2 bytes, sem sinal e com
    ordenação de bytes `big-endian`.
    """

    def __init__(self):
        DadoBasico.__init__(self)

    # code::start prefixado_leitura_de_arquivo
    def leia_de_arquivo(self, arquivo: BinaryIO) -> bytes:
        """
        Leitura de um único dado prefixado pelo comprimento a partir de um
        arquivo binário aberto. Os bytes de comprimento são removidos.

        :param BinaryIO arquivo: arquivo binário aberto com permissão de leitura
        :return: sequência com os bytes do dado, sem o prefixo
        :rtype: bytes
        :raise EOFError: se houver tentativa de leitura além do fim do arquivo
        """
        bytes_comprimento = arquivo.read(2)
        if len(bytes_comprimento) == 0:
            raise EOFError("Fim do arquivo encontrado ao ler comprimento.")
        else:
            comprimento = int.from_bytes(bytes_comprimento, "big",
                                         signed = False)
            dado = arquivo.read(comprimento)
            if len(dado) != comprimento:
                raise EOFError("Fim do arquivo encontrado ao ler dado" +
                               f" prefixado. {len(dado) - comprimento}" +
                               " bytes faltantes.")
            else:
                return dado

    # code::end

    def leia_de_bytes(self, sequencia: bytes) -> tuple[bytes, bytes]:
        """
        Recuperação de um dado individual de uma sequência de bytes,
        retornando o dado sem o prefixo e o restante da sequência.

        :param bytes sequencia: uma sequência de bytes
        :return: uma tupla com a sequência de bytes de dados sem o prefixo e
            o restante da sequência de entrada
        :rtype: tuple[bytes, bytes]
        :raise TypeError: se a sequência contiver menos bytes que o necessário
        """
        if len(sequencia) >= 2:
            comprimento = int.from_bytes(sequencia[:2], "big", signed = False)
        else:
            raise TypeError("A sequência de bytes não contém bytes suficientes")
        dado = sequencia[2:comprimento + 2]
        sequencia_restante = sequencia[comprimento + 2:]
        if len(dado) != comprimento:
            raise TypeError("A sequência de bytes não contém bytes suficientes")
        return dado, sequencia_restante

    # code::start prefixado_formatacoes
    def adicione_formatacao(self, dado: bytes) -> bytes:
        """
        Formatação do dado: acréscimo do prefixo binário com comprimento
        (2 bytes, `big-endian`, sem sinal).

        :param bytes dado: sequência de bytes do dado
        :return: a sequência de bytes prefixada por dois bytes com o
            comprimento
        :rtype: bytes
        """
        bytes_comprimento = len(dado).to_bytes(2, "big", signed = False)
        return bytes_comprimento + dado

    def remova_formatacao(self, sequencia: bytes) -> bytes:
        """
        Desformatação do dado: remoção dos dois bytes do comprimento.

        :param bytes sequencia: bytes de dados
        :return: dado efetivo, sem o prefixo de comprimento
        :rtype: bytes
        :raise TypeError: se a sequência de bytes passada contém quantidade de
            bytes diferente do comprimento especificado
        """
        dado, sequencia_restante = self.leia_de_bytes(sequencia)
        if len(sequencia_restante) != 0:
            raise TypeError("O comprimento da sequência de bytes de dados" +
                            " não contém é o tamanho especificado.")
        return dado
    # code::end


class DadoBinario(DadoBasico):
    """
    Classe para a implementação de dado como sequência de bytes (i.e., formato
    binário) com um determinado comprimento fixo em bytes.

    :param int comprimento: comprimento em bytes do valor a ser armazenado
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
        Recuperação dos bytes do valor binário a partir de um arquivo dada a
        quantidade de bytes esperada.

        :param BinaryIO arquivo: arquivo binário aberto com permissão de leitura
        :return: a sequência de bytes lidos
        :rtype: bytes
        :raise EOFError: se o arquivo contiver menos bytes que a quantidade
            esperada
        """
        dado = arquivo.read(self._comprimento)
        if len(dado) < self._comprimento:
            raise EOFError("Quantidade de bytes inferior à esperada" +
                           " para o dado")
        else:
            return dado

    # code::end

    def leia_de_bytes(self, sequencia: bytes) -> tuple[bytes, bytes]:
        """
        Recuperação de um dado binário de comprimento definido a partir de
        uma sequência de bytes.

        :param bytes sequencia: sequência de bytes
        :return: tupla com os bytes do dado no comprimento esperado e a
            sequência de bytes restante
        :rtype: tuple[bytes, bytes]
        :raise TypeError: se a sequência contiver menos bytes que o esperado
        """
        if len(sequencia) < self._comprimento:
            raise TypeError("A sequência não possui bytes suficientes")
        dado = sequencia[:self._comprimento]
        sequencia_restante = sequencia[self._comprimento:]
        return dado, sequencia_restante

    # code::start binario_formatacoes
    def adicione_formatacao(self, dado: bytes) -> bytes:
        """
        Formatação do dado: apenas repassa o dado binário.

        :param bytes dado: valor binário
        :return: o dado sem modificação
        :rtype: bytes
        :raise TypeError: se o comprimento do dado diferir do esperado
        """
        if len(dado) != self._comprimento:
            raise TypeError("O dado não possui o comprimento correto")
        return dado

    def remova_formatacao(self, sequencia: bytes) -> bytes:
        """
        Desformatação do dado: apenas repassa o dado binário.

        :param bytes sequencia: sequência de bytes do valor binário
        :return: a sequência sem modificação
        :rtype: bytes
        :raise TypeError: se o comprimento do dado diferir do esperado
        """
        if len(sequencia) != self._comprimento:
            raise TypeError("A sequência de dados não possui o "
                            "comprimento correto")
        return sequencia
    # code::end


class DadoFixo(DadoBasico):
    """
    Classe para a implementação de dado de comprimento fixo em representação
    textual (i.e., sequência de caracteres). Caso o comprimento do dado seja
    inferior ao comprimento estabelecido para o campo, é feito o preenchimento
    dos bytes restantes com o valor
    :attr:`~.estrutarq.dado.DadoFixo.preenchimento`. Caso o dado passado seja
    de comprimento superior ao definido, há o truncamento. Havendo a ocorrência
    do byte de preenchimento nos bytes de dados, é feito o enchimento de bytes.
    O preenchimento e o truncamento são feitos depois do enchimento.

    :param int comprimento: o comprimento em bytes fixado para o dado
    :param bytes, opcional preenchimento: um byte usado para preenchimento
        do espaço não usado para dado (valor padrão ``0xFF``)
    """

    def __init__(self, comprimento: int, preenchimento: bytes = b'\xff'):
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
            raise AttributeError("O comprimento mínimo para o dado é um byte")
        self.__comprimento = comprimento

    @property
    def preenchimento(self) -> bytes:
        """
        Um único byte usado para o preenchimento do espaço não usado dentro
        do comprimento final do campo. Valor padrão ``0xFF``.
        """
        return self.__preenchimento

    @preenchimento.setter
    def preenchimento(self, preenchimento: bytes):
        """
        Determina o byte que será usado como preenchimento de campo.

        :param bytes preenchimento: um byte para preenchimento
        """
        if not isinstance(preenchimento, bytes) \
                or len(preenchimento) != 1:
            raise AttributeError("O byte de preenchimento deve ter um byte")
        self.__preenchimento = preenchimento

    # code::start fixo_leitura_de_arquivo
    def leia_de_arquivo(self, arquivo: BinaryIO) -> bytes:
        """
        Leitura de um único dado de comprimento fixo a partir do arquivo, com
        remoção de bytes de enchimento e supressão do preenchimento.

        :param BinaryIO arquivo: arquivo binário aberto com permissão de leitura
        :return: os bytes do dado, removidos o enchimento e preenchimento
        :rtype: bytes
        :raise EOFError: se o arquivo não contiver a quantidade de bytes
            esperada definida pelo comprimento do dado
        """
        dado = arquivo.read(self._comprimento)
        if len(dado) != self._comprimento:
            raise EOFError("O comprimento da sequência de bytes de dados" +
                           " não contém é o tamanho especificado.")
        else:
            return self.remova_formatacao(dado)

    # code::end

    def leia_de_bytes(self, sequencia: bytes) -> typle[bytes, bytes]:
        """
        Recuperação de um dado individual de uma sequência de bytes,
        retornando o dado sem os bytes de preenchimento e o restante da
        sequência.

        :param sequencia: uma sequência de bytes
        :return: tupla com os bytes do dado, removidos os bytes de enchimento
            e preenchimento, e a sequência de bytes restante
        :rtype: typle[bytes, bytes]
        :raise TypeError: se o comprimento da sequência tem menos bytes
            que o definido para o comprimento do campo
        """
        if len(sequencia < self._comprimento):
            raise TypeError("A sequência de bytes contém menos bytes que" +
                            " o esperado.")
        else:
            sequencia_restante = sequencia[self._comprimento:]
            sequencia = sequencia[:self._comprimento] + self.preenchimento
            dado_limpo = self.varredura_com_enchimento(
                sequencia, self.preenchimento)[0][:-1]
            return self.esvaziamento_de_bytes(dado_limpo), sequencia_restante

    # code::start fixo_formatacoes
    def adicione_formatacao(self, dado: bytes) -> bytes:
        """
        Formatação do dado: ajusta o dado para o comprimento definido,
        truncando ou adicionando o byte de preenchimento.

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
        Desformatação do dado: remoção de caracteres de preenchimento.

        :param sequencia: bytes de dados
        :return: dado efetivo, sem preenchimento
        """
        # if len(sequencia) != self.comprimento:
        #     raise TypeError(
        #     "A sequência de dados tem comprimento incorreto.")
        return self.leia_de_bytes(sequencia)[0]
        # code::end
