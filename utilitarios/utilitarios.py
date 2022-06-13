"""
Rotinas utilitárias para dispositivos de armazenamento secundário.

..
    Licença: GNU GENERAL PUBLIC LICENSE V.3, 2007
    Jander Moreira, 2021, 2022
"""

from os import fstat, remove
from sys import version_info
from tempfile import mkstemp


def comprimento_de_bloco(diretorio: str = None) -> int:
    """
    Determina o comprimento de um bloco de um dispositivo, tendo como referência
    o armazenamento onde está o diretório temporário do sistema; para outro
    dispositivo externo, é preciso informar um diretório em que se tenha direito
    de criação de arquivos.

    Efeitos colaterais: é criado um arquivo temporário que, em seguida, é
    removido.

    :param diretorio: um nome diretório no dispositivo a ser usado como base
        para a verificação (padrão: `None`)
    :return: o comprimento do bloco de armazenamento em bytes
    """
    try:
        descritor, nome_arquivo = mkstemp(dir = diretorio)
        comprimento = fstat(descritor).st_blksize
        remove(nome_arquivo)
        return comprimento
    except IOError as erro:
        raise IOError(f"Criação de arquivo temporário mal sucedida. {erro}")


class ErroVersao(Exception):
    """
    Exceção para o caso de versões do Python incompatíveis com esta
    implementação.
    Veja :func:`~.estrutarq.utilitarios.utilitarios.verifique_versao`.
    """
    pass


def verifique_versao():
    """
    Verificação de versão do Python em uso. Há recursos que podem não funcionar
    em versões anteriores à 3.6.

    :raise ErroVersao: se a versão for inferior a 3.6
    """

    versao = ".".join(str(x) for x in version_info[:3])
    mensagem = f"""
    *** Importante: A versão do Python em uso é a {versao}.

    Versões anteriores à 3.6 não mantém a ordem das chaves em dicionários.
    Como os campos de registros são mantidos em dicionários, a recuperação
    de um registro deve falhar, pois os campos podem ser organizados de
    forma diferente da usada na gravação nas diferentes execuções do programa.
    """
    if f"{version_info.major:03d}{version_info.minor:03d}" < "003006":
        raise ErroVersao(mensagem)
