################################################################################
################################################################################
#  Implementação de campos

################################################################################
################################################################################
# Campo básico

class CampoBasico:
    """
    Estruturação básica do campo como menor unidade de informação
    Implementa as funções de um campo bruto, ou seja, sem organização
    de campo. O valor é sempre armazenado como cadeia de caracteres.
    """

    def __init__(self, tipo: str = "bruto"):
        # if tipo not in relacao_tipo_campos.keys():
        #     raise TypeError(f"Tipo de campo desconhecido ({tipo})")
        self.__tipo = tipo
        self.__valor = None

    @property
    def tipo(self):
        return self.__tipo

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

    @staticmethod
    def leia_dado_de_arquivo(arquivo) -> bytes:
        """
        Método para leitura de dados do arquivo a ser sobrescrito por
        outras classes. Não há suporte para leitura do tipo bruto.
        :return: os bytes lidos para o campo
        """
        pass

    # code::start escreva
    def escreva(self, arquivo):
        """
        Gravação do conteúdo do campo em um arquivo
        :param arquivo: arquivo binário aberto com permissão de escrita
        """
        arquivo.write(self.para_bytes())
    # code::end


class CampoTerminador:
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


class CampoPrefixado:
    """
    Classe para implementação de campos prefixados pelo seu comprimento
    """

    # code::start leitura_prefixado
    @staticmethod
    def leia_dado_de_arquivo(arquivo) -> bytes:
        """
        Leitura de um único campo prefixado pelo comprimento.
        :param arquivo: arquivo binário aberto com permissão de leitura
        :return: os bytes do campo

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


class CampoFixo:
    """
    Classe para implementação de campos de comprimento fixo
    """

    def __init__(self, comprimento: int, preenchimento = '\xFF'):
        print(f"comprimento '{comprimento}'")
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
        Leitura de um único campo de comprimento fixo
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


class CampoBinario:
    """
    Classe para campos binários: escrita e leitura de bytes
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



################################################################################
################################################################################
# Interface

# relacao_tipo_campos = [
#     "bruto": CampoBasico,
#     "cadeia terminador",
#     "cadeia prefixado",
#     "cadeia fixo",
#     "inteiro binário",
#     "real binário",
#     "data binário": campo_tempo.CampoDataBinario,
# ]

#
# def crie_campo(tipo: str, *args, **kwargs):
#     import estrutarq.campo_inteiro as campo_inteiro
#     import estrutarq.campo_cadeia as campo_cadeia
#     import estrutarq.campo_real as campo_real
#     import estrutarq.campo_tempo as campo_tempo
#     global relacao_tipo_campos
#     relacao_tipo_campos = {
#         "bruto": CampoBasico,
#         "cadeia terminador": campo_cadeia.CampoCadeiaTerminador,
#         "cadeia prefixado": campo_cadeia.CampoCadeiaPrefixado,
#         "cadeia fixo": campo_cadeia.CampoCadeiaFixo,
#         "inteiro binário": campo_inteiro.CampoIntBinario,
#         "real binário": campo_real.CampoRealBinario,
#         "data binário": campo_tempo.CampoDataBinario,
#     }
#
#     if tipo not in relacao_tipo_campos.keys():
#         raise TypeError(f"Tipo de campo desconhecido ({tipo})")
#     else:
#         return relacao_tipo_campos[tipo](*args, **kwargs)
