"""
Registros
"""

from abc import ABCMeta
from copy import deepcopy
from re import compile

from estrutarq.campo import CampoBasico
from estrutarq.dado import DadoBasico, DadoBruto, DadoFixo, DadoPrefixado, \
    DadoTerminador
from estrutarq.utilitarios.geral import verifique_versao

#######
verifique_versao()

terminador_de_registro = b"\x01"
preenchimento_de_registro = b"\xfe"


class RegistroBasico(DadoBasico, metaclass = ABCMeta):
    """
    Classe básica para registros

    Utiliza @DynamicAttrs
    """

    def __init__(self, tipo: str, *lista_campos):
        self.__tipo = tipo
        self.lista_campos = {}
        self.adicione_campos(*lista_campos)

    @property
    def tipo(self):
        return self.__tipo

    def __adicione_um_campo(self, campo: (str, CampoBasico)):
        """
        Acréscimo de um campo a registro, com criação de um atributo e
        inclusão na lista de campos
        :param campo: uma tupla (nome_arquivo, campo), com nome_arquivo (str)
            sendo o nome_arquivo do campo e campo sendo uma instância de um
            campo válido
        """
        nome_campo = campo[0]
        tipo_campo = campo[1]
        identificador = compile(r"^\w[_\w\d]+$")
        if not isinstance(nome_campo, str) or \
                not identificador.match(campo[0]):
            mensagem = "O nome_arquivo do campo deve ser " + \
                       f"um identificador válido ('{nome_campo}')."
            raise TypeError(mensagem)
        # if not isinstance(tipo_campo, str):
        #     print("************", type(tipo_campo))
        #     raise TypeError("Esperado um campo valido para o registro.")
        setattr(self, nome_campo, tipo_campo.copy())
        self.lista_campos[nome_campo] = getattr(self, nome_campo)

    def adicione_campos(self, *lista_campos):
        """
        Inclusão de uma sequência de campos ao registro
        :param lista_campos: uma sequência de um ou mais campos, cada um
            especificado pela tupla (nome_arquivo, campo), com
            nome_arquivo (str) sendo o nome_arquivo do campo e campo sendo
            uma instância de um campo válido
        """
        for campo in lista_campos:
            self.__adicione_um_campo(campo)

    def de_bytes(self, dados_registro: bytes):
        """
        Obtenção dos bytes de cada campo a partir dos bytes do registro inteiro
        :param dados_registro: sequência de bytes do registro
        """
        dados_restantes = dados_registro
        for campo in self.lista_campos.values():
            dado_campo, dados_restantes = campo.leia_de_bytes(dados_restantes)
            campo.bytes_para_valor(dado_campo)

    def para_bytes(self) -> bytes:
        """
        Criação dos bytes do registro pela concatenação dos bytes dos campos,
        sucessivamente
        :return: sequência dos bytes dos campos
        """
        dado_campos = bytes()
        for campo in self.lista_campos.values():
            dado_campos += campo.adicione_formatacao(campo.valor_para_bytes())
        return dado_campos

    def tem_comprimento_fixo(self):
        """
        Verifica se o registro tem comprimento_bloco fixo
        :return: True se o comprimento_bloco for fixo

        O registro é considerado de tamanho fixo se qualquer uma das
        propriedades foram verdadeiras:
            1) o registro tem o atributo 'comprimento_bloco'
            2) todos os campos tiverem comprimento_bloco fixo
        """
        registro_fixo = hasattr(self, "comprimento_bloco")
        campos_fixos = all(hasattr(campo, "comprimento_bloco") for campo in
                           self.lista_campos.values())
        return registro_fixo or campos_fixos

    def comprimento_fixo(self):
        """
        Retorna o comprimento_bloco do registro em bytes caso ele tenha comprimento_bloco
        total fixo
        :return: o comprimento_bloco do registro em bytes ou None se tiver
        comprimento_bloco variável
        """
        comprimentos = [campo.comprimento_fixo() for campo in
                        self.lista_campos.values()]
        if None not in comprimentos:
            return sum(comprimentos)
        else:
            return None

    def _leia_registro(self, arquivo):
        """
        Leitura genérica de um registro usando a forma de organização de
        dados atual, preenchendo os campos
        :param arquivo: arquivo binário aberto com permissão de leitura
        """
        bytes_arquivo = self.leia_de_arquivo(arquivo)
        self.de_bytes(bytes_arquivo)

    # code::start basico_leia
    def leia(self, arquivo):
        """
        Obtenção de um registro a partir do arquivo
        :param arquivo: arquivo binário aberto com permissão de leitura

        Sendo possível determinar o comprimento_bloco do registro como um valor
        fixo e conhecido, todos os bytes são lidos em uma única chamada de
        leitura; caso contrário, é feita a recuperação de acordo com a
        organização de registro utilizada.
        """
        # comprimento_registro = self.comprimento_fixo()
        # if comprimento_registro:
        #     # leitura do registro inteiro (tamanho fixo)
        #     comprimento_total = len(
        #         self.adicione_formatacao(b" " * comprimento_registro))
        #     bytes_registro = arquivo.read(comprimento_total)
        #     if len(bytes_registro) != comprimento_total:
        #         raise EOFError(
        #             "Quantidade de bytes lidos inferior ao solicitado")
        #     self.de_bytes(self.remova_formatacao(bytes_registro))
        # else:
        #     # leitura dependente da organização de registro
        self._leia_registro(arquivo)

    # code::end

    def escreva(self, arquivo):
        """
        Escrita do registro no arquivo
        :param arquivo:
        """
        bytes_dados = self.para_bytes()
        if hasattr(self, "comprimento_bloco") and len(bytes_dados) > self.comprimento:
            raise ValueError("Comprimento do dados excede máximo do registro.")
        arquivo.write(self.adicione_formatacao(bytes_dados))

    def __str__(self):
        texto = f"Registro: {self.tipo}\n"
        for nome, campo in self.lista_campos.items():
            em_bytes = campo.adicione_formatacao(campo.valor_para_bytes())
            texto += f"{nome}: {type(campo).__name__} = {campo.valor} " + \
                     f"({em_bytes})\n"
        return texto[:-1]

    def copy(self):
        """
        Cópia "profunda" deste campo
        :return: outra instância com os mesmos valores
        """
        return deepcopy(self)


class RegistroBruto(DadoBruto, RegistroBasico):
    """
    Classe básica para registro, com controle exclusivamente pelo número
    de campos

    Utiliza @DynamicAttrs
    """

    def __init__(self, *lista_campos):
        super().__init__("bruto", *lista_campos)

    # code::start bruto_leia_registro
    def _leia_registro(self, arquivo):
        """
        Leitura de registro bruto, campo a campo
        :param arquivo: arquivo binário aberto com permissão de leitura
        """
        for campo in self.lista_campos.values():
            campo.leia(arquivo)
    # code::end


class RegistroPrefixado(DadoPrefixado, RegistroBasico):
    """
    Classe para registros prefixados pelo comprimento_bloco
    """

    def __init__(self, *lista_campos):
        RegistroBasico.__init__(self, "prefixado", *lista_campos)
        DadoPrefixado.__init__(self)


class RegistroTerminador(DadoTerminador, RegistroBasico):
    """
    Classe para registros com terminador
    """

    def __init__(self, *lista_campos):
        RegistroBasico.__init__(self, "terminador", *lista_campos)
        DadoTerminador.__init__(self, terminador_de_registro)


class RegistroFixo(DadoFixo, RegistroBasico):
    """
    Classe para registros com terminador
    """

    def __init__(self, comprimento: int, *lista_campos):
        RegistroBasico.__init__(self, "fixo", *lista_campos)
        DadoFixo.__init__(self, comprimento,
                          preenchimento = preenchimento_de_registro)
