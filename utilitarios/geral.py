"""
Funções gerais
"""

from sys import version_info

class ErroVersao(Exception):
    pass


def verifique_versao():
    """
    Verificação de versão do Python em uso. Há recursos que podem não funcionar
    em versões anteriores à 3.6.

    :return: código de erro 2 em caso de falha
    """

    versao = ".".join(str(x) for x in version_info[:3])
    mensagem = f"""*** Importante:
    A versão do Python em uso é a {versao}.
    
    Versões anteriores à 3.6 não mantém a ordem das
    chaves em dicionários. Como os campos de registros
    são mantidos em dicionários, a recuperação de um
    registro deve falhar, pois os campos podem ser
    organizados de forma diferente da usada na gravação
    em diferentes execuções do programa.
    """
    if f"{version_info.major:03d}{version_info.minor:03d}" < "003106":
        raise ErroVersao(mensagem)
