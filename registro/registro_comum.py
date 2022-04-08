"""
Registros como coleção de campos.

Uma classe básica :class:`~.estrutarq.registro_teste.registro_comum.RegistroBasico`
define uma classe abstrata (ABC) com as propriedades e métodos gerais. Dela
são derivados registros:

* Brutos (i.e., sem organização para o registro_teste)
* Com terminador
* Prefixado pelo comprimento
* De comprimento fixo predefinido

..
    Licença: GNU GENERAL PUBLIC LICENSE V.3, 2007
    Jander Moreira, 2021, 2022
"""

from abc import ABCMeta
from copy import deepcopy
from re import compile
from typing import BinaryIO

from estrutarq.campo import CampoBasico
from estrutarq.dado import DadoBasico, DadoBruto, DadoFixo, DadoPrefixado, \
    DadoTerminador
from utilitarios.geral import verifique_versao

# Verificação de versão necessária para uso de registros
verifique_versao()

terminador_de_registro = b"\x01"
"""
Byte terminador de registro_teste. Deve diferir do terminador de campo.
(valor padrão ``0x01``)
"""

preenchimento_de_registro = b"\xfe"
"""
Byte usado no preenchimento de registros de comprimento fixo. Deve diferir
do preenchimento de campo. (valor padrão ``0xFE``)
"""


class RegistroBasico(DadoBasico, metaclass = ABCMeta):
    """
    Classe básica para registros, o qual é estruturado pela adiçõo de campos.

    Os campos ficam acessíveis como atributos da classe e, assim, podem ser
    manipulados individualmente.

    :param str tipo: o nome do tipo do parâmetro (definido pelas subclasses)
    :param list[tuple[str, CampoBasico]], opcional lista_campos: sequência com
        tuplas ``("nome_campo", Campo())``.
    """

    def __init__(self, tipo: str, *lista_campos: tuple[str, CampoBasico]):
        DadoBasico.__init__(self)
        self.__tipo = tipo
        self.lista_campos = {}
        self.adicione_campos(*lista_campos)
        self._comprimento_fixo = False

    @property
    def tipo(self) -> str:
        """
        O nome do tipo do registro_teste, usado apenas para consulta. São exemplos
        ``registro_teste fixo`` e ``registro_teste terminador``.

        :return: o nome do tipo do registro_teste
        """
        return self.__tipo

    def __adicione_um_campo(self, campo: tuple[str, CampoBasico]):
        """
        Acréscimo de um campo a registro_teste, com criação de um atributo e
        inclusão na lista de campos.

        :param tuple[str, CampoBasico] campo: uma tupla (nome_arquivo, campo),
            com nome_arquivo (str) sendo o nome_arquivo do campo e campo
            sendo uma instância de um campo válido
        :raise AttributeError: se o nome do campo não for um identificador
            válido
        """
        nome_campo = campo[0]
        tipo_campo = campo[1]
        identificador = compile(r"^\w[_\w\d]+$")
        if not isinstance(nome_campo, str) or \
                not identificador.match(campo[0]):
            raise AttributeError("O nome_arquivo do campo deve ser " +
                                 f"um identificador válido ('{nome_campo}').")
        setattr(self, nome_campo, tipo_campo.copia())
        self.lista_campos[nome_campo] = getattr(self, nome_campo)

    def adicione_campos(self, *lista_campos: tuple[str, CampoBasico]):
        """
        Inclusão de uma sequência de campos ao registro_teste

        :param list[tuple[str, CampoBasico] lista_campos: uma sequência de um ou
            mais campos, cada um especificado pela tupla (nome_do_campo, campo),
            com nome_arquivo (str) sendo o nome_arquivo do campo e campo sendo
            uma instância de um campo válido
        """
        for campo in lista_campos:
            self.__adicione_um_campo(campo)

    def de_bytes(self, dados_registro: bytes):
        """
        Varredura da sequência de bytes que formam um registro_teste para a obtenção
        dos dados de cada campo individual, atualizando cada um deles.

        :param bytes dados_registro: sequência de bytes do registro_teste
        """
        dados_restantes = dados_registro
        for campo in self.lista_campos.values():
            dado_campo, dados_restantes = campo.leia_de_bytes(dados_restantes)
            campo.bytes_para_valor(dado_campo)

    def para_bytes(self) -> bytes:
        """
        Criação dos bytes do registro_teste pela concatenação dos bytes dos campos,
        sucessivamente.

        :return: sequência dos bytes do registro_teste
        :rtype: bytes
        """
        dado_do_registro = bytes()
        for campo in self.lista_campos.values():
            dado_do_registro += \
                campo.adicione_formatacao(campo.valor_para_bytes())
        return dado_do_registro

    def tem_comprimento_fixo(self) -> bool:
        """
        Verifica se o registro_teste tem comprimento fixo.

        O registro_teste é considerado de tamanho fixo se qualquer uma das
        propriedades foram verdadeiras:
        * o registro_teste tem é marcado com _comprimento_fixo == True
        * todos os campos tiverem comprimento fixo

        :return: `True` se o comprimento for fixo, `False` caso contrário
        :rtype: bool
        """
        return self._comprimento_fixo or all(
            campo.tem_comprimento_fixo() for campo
            in self.lista_campos.values())

    def comprimento(self) -> int:
        """
        Retorna o comprimento atual do registro_teste em bytes.

        :return: o comprimento do registro_teste em bytes
        :rtype: int
        """

        return sum(campo.comprimento() for campo in self.lista_campos.values())

    # code::start basico_leia

    def leia(self, arquivo: BinaryIO):
        """
        Obtenção de um registro_teste a partir do arquivo, considerando a organização
        de registro_teste em uso.

        :param BinaryIO arquivo: arquivo binário aberto com permissão de leitura
        """

        bytes_arquivo = self.leia_de_arquivo(arquivo)
        self.de_bytes(bytes_arquivo)

    # code::end

    def escreva(self, arquivo: BinaryIO):
        """
        Escrita dos bytes do registro_teste no arquivo, usando a organização
        definida.

        :param BinaryIO arquivo: arquivo binário aberto com permissão de escrita
        """
        bytes_dados = self.adicione_formatacao(self.para_bytes())
        arquivo.write(bytes_dados)

    def __str__(self):
        texto = f"Registro: {self.tipo}\n"
        for nome, campo in self.lista_campos.items():
            em_bytes = campo.adicione_formatacao(campo.valor_para_bytes())
            texto += f"{nome}: {type(campo).__name__} = {campo.valor} " + \
                     f"({em_bytes})\n"
        return texto[:-1]

    def copia(self):
        """
        Cópia "profunda" do registro_teste.

        :return: outra instância com os mesmos valores.
        """
        return deepcopy(self)


class RegistroBruto(DadoBruto, RegistroBasico):
    """
    Classe para registros brutos, ou seja, sem organização de dados adiconal e
    com controle exclusivamente pelo número de campos definido.

    :param list[tuple[str, CampoBasico]], opcional lista_campos: sequência com
        tuplas ``("nome_campo", Campo())``.
    """

    def __init__(self, *lista_campos: tuple[str, CampoBasico]):
        RegistroBasico.__init__(self, "bruto", *lista_campos)
        DadoBruto.__init__(self)

    # code::start bruto_leia_registro
    def leia(self, arquivo):
        """
        Leitura de registro_teste bruto, feita campo a campo.

        :param BinaryIO arquivo: arquivo binário aberto com permissão de leitura
        """

        for campo in self.lista_campos.values():
            campo.leia(arquivo)
    # code::end


class RegistroTerminador(DadoTerminador, RegistroBasico):
    """
    Classe para registros com terminador

    :param list[tuple[str, CampoBasico]], opcional lista_campos: sequência com
        tuplas ``("nome_campo", Campo())``.
    """

    def __init__(self, *lista_campos):
        RegistroBasico.__init__(self, "terminador", *lista_campos)
        DadoTerminador.__init__(self, terminador_de_registro)


class RegistroPrefixado(DadoPrefixado, RegistroBasico):
    """
    Classe para registros prefixados pelo comprimento, usando a estruturação de
    :class:`~.estrutarq.dado.dado_comum.DadoPrefixado`.

    :param list[tuple[str, CampoBasico]], opcional lista_campos: sequência com
        tuplas ``("nome_campo", Campo())``.
    """

    def __init__(self, *lista_campos):
        RegistroBasico.__init__(self, "prefixado", *lista_campos)
        DadoPrefixado.__init__(self)


class RegistroFixo(DadoFixo, RegistroBasico):
    """
    Classe para registros com comprimento fixo.

    :param int comprimento: o comprimento prefixado para o campo em bytes
    :param list[tuple[str, CampoBasico]], opcional lista_campos: sequência com
        tuplas ``("nome_campo", Campo())``.
    """

    def __init__(self, comprimento: int, *lista_campos):
        RegistroBasico.__init__(self, "fixo", *lista_campos)
        DadoFixo.__init__(self, comprimento,
                          preenchimento = preenchimento_de_registro)
        self._comprimento_fixo = True
        self._comprimento_registro = comprimento

    def comprimento(self) -> int:
        """
        Retorna o comprimento do registro_teste em bytes.

        :return: o comprimento do registro_teste em bytes
        :rtype: int
        """
        return self._comprimento_registro