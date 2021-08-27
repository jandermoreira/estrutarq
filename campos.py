import estrutarq.erros


class CampoBasico:
    """
    Estruturação básica do campo como menor unidade de informação
    """

    def __init__(self, tipo):
        self.tipo = tipo
        self.valor = None

    def atribua(self, valor):
        """
        Atribuição do valor do campo
        :param valor: valor a ser guardado
        """
        self.valor = valor

    def escreva(self, arquivo):
        """
        Gravação do conteúdo do campo em um arquivo
        :param arquivo:
        :return:
        """
        arquivo.write(self.bytes())


class CampoIntBasico(CampoBasico):
    def atribua(self, valor):
        """
        Atribuição de um valor inteiro do campo. Caso o valor não seja
        do tipo int, uma exceção TipoInválido é disparada.
        :param valor: valor a ser guardado
        """
        if type(valor).__name__ != 'int':
            raise estrutarq.erros.TipoInvalido('Esperado um valor inteiro')
        else:
            self._CampoBasico__valor = valor


class CampoIntPrefixo(CampoIntBasico):
    """Classe para inteiro textual com prefixo de tamanho"""

    def __init__(self):
        """Construtor"""
        super().__init__('int prefixo')
        self.atribua(0)

    def bytes(self):
        """
        Representação do valor em uma sequência de bytes
        2 bytes de prefixo em binário com o número de dígitos (little endian)
        sequência de dígitos que formam o valor numérico, com '-' se negativo
        :return: sequência de bytes com o prefixo binário e os bytes do campo
        """
        numero_bytes = bytes(f'{self._CampoBasico__valor}', encoding = 'utf8')
        prefixo_binario = len(numero_bytes).to_bytes(2, 'little')
        return prefixo_binario + numero_bytes

    def leia(self, arquivo):
        """
        Recuperação do conteúdo do campo de um arquivo
        :param self:
        :param arquivo:
        :return:
        """
        arquivo.read(2)


class CampoIntBinario(CampoIntBasico):
    """Classe para inteiro em formato binário (little endian) com 8 bytes
    e complemento para 2 para valores negativos; transbordo resulta em -1
    """

    def __init__(self):
        """Construtor"""
        super().__init__('int binário')
        self.atribua(0)

    def bytes(self):
        """Representação do valor em binário (little endian) de 8 bytes"""
        return self._CampoBasico__valor.to_bytes(8, 'little', signed = True)


class CampoIntFixo(CampoIntBasico):
    """Classe para inteiro textual com tamanho fixo"""

    def __init__(self, comprimento):
        """Construtor"""
        super().__init__('int terminador')
        self.atribua(0)
        self.__comprimento = comprimento

    def bytes(self):
        """Representação do valor em uma sequência de dígitos que formam
        o valor numérico, terminando como 'terminador'
        """
        numero_bytes = bytes(
            f'{self._CampoBasico__valor:{self.__comprimento}d}',
            encoding = 'utf8')
        return numero_bytes


class CampoIntTerminador(CampoIntBasico):
    """Classe para inteiro textual com terminador"""

    def __init__(self, terminador = '!'):
        super().__init__('int terminador')
        self.__terminador = terminador
        self.atribua(0)

    def bytes(self):
        """Representação do valor em uma sequência de dígitos que formam
        o valor numérico, terminando como 'terminador'
        """
        numero_bytes = bytes(f'{self._CampoBasico__valor}{self.__terminador}',
                             encoding = 'utf8')
        return numero_bytes


class CampoRealBasico(CampoBasico):
    def atribua(self, valor):
        if type(valor).__name__ != 'float':
            raise estrutarq.erros.TipoInvalido('Esperado um valor real (float)')
        else:
            self._CampoBasico__valor = valor


class CampoRealPrefixo(CampoRealBasico):
    def __init__(self):
        super().__init__('real prefixo')


relacao_tipo_campos = {
    'int prefixo': CampoIntPrefixo,
    'int binário': CampoIntBinario,
    'int fixo': CampoIntFixo,
    'int terminador': CampoIntTerminador,
    'real prefixo': CampoRealPrefixo,
}


def campo(tipo, *args, **kwargs):
    if tipo not in relacao_tipo_campos.keys():
        raise estrutarq.erros.TipoDesconhecido(
            f'Tipo de campo desconhecido ({tipo})')
    else:
        return relacao_tipo_campos[tipo](*args, **kwargs)
