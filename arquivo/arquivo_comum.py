#############################
# Implementação de arquivos
#############################

# from registro import RegistroBasico
from bloco import Bloco
from os.path import exists


class Arquivo:
    def __init__(self, nome: str,
                 cabecalho: bool = True,
                 novo: bool = False,

                 ):
        self.nome_arquivo = nome
        self._usa_cabecalho = cabecalho
        self._inicia_arquivo(novo)

    def _inicia_arquivo(self, novo: bool):
        if not exists(self.nome_arquivo) or novo:
            modo = "wb"  # cria arquivo novo
        else:
            modo = "rb"  # arquivo já existe

        try:
            self._arquivo = open(self.nome_arquivo, modo)
        except IOError:
            raise IOError(f"Erro de abertura do arquivo {self.nome_arquivo}.")
        else:
            self.bloco = Bloco(self._arquivo)

    # def registro(self, formato):
    #     if isinstance(formato, str):
    #         # cria arquivo a partir de especificação textual
    #         ""
    #     elif isinstance(RegistroBasico):
    #         # cria arquivo a partir de um registro pré-existente
    #         ""
    #     else:
    #         raise TypeError("Esperado um registro ou uma especificação.")

    def feche(self):
        """
        Fecha o arquivo
        """
        self._arquivo.close()
