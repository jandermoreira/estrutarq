"""
Interpretador de comandos para manipulação de arquivos, registros e
campos
"""

from pypeg2 import *

abreviacoes_comandos = {
    "ca": "crie arquivo",
    "ci": "crie índice",
    "ir": "insira registro"
}


def comando_canonico(cadeia: str) -> str:
    """
    Limpa uma cadeia de caracteres, deixando-a em uma forma canônica:
    somente minúsculas, sem brancos antes ou depois, espaçamento simples
    entre palavras
    :param cadeia: cadeia de caracteres
    :return: a cadeia na forma canônica
    """
    comando = " ".join(cadeia.split())
    if len(comando) == 2:
        comando = abreviacoes_comandos[comando]
    return comando


class Comprimento(str):
    grammar = "(", re.compile(r"\d+"), ")"


class OrganizacaoRegistro(List):
    grammar = [
        K("bruto"),
        K("terminador"),
        K("prefixado"),
        # (K("fixo"), Comprimento),
    ]


class OrganizacaoCampo(Keyword):
    grammar = Enum(
        K("terminador"),
        K("prefixado"),
        K("fixo"),
        K("binário"),
    )


class TipoCampo(Keyword):
    grammar = Enum(
        K("cadeia"),
        K("inteiro"),
        K("real"),
        K("tempo"),
        K("data"),
        K("hora"),
    )


class EspecificacaoCampo(List):
    grammar = (
        name(), ":",
        attr("tipo_campo", TipoCampo),
        attr("organizacao_campo", OrganizacaoCampo),
        attr("comprimento", optional(Comprimento)),
    )


class ListaEspecificacaoCampos(List):
    grammar = EspecificacaoCampo, maybe_some(",", EspecificacaoCampo)


class CrieArquivo(str):
    grammar = (
        attr("comando", re.compile(r"crie\s+arquivo|ca")),
        attr("nome_arquivo", word),
        attr("tipo_registro", optional(OrganizacaoRegistro)),
        attr("comprimento", optional(Comprimento)),
        "com",
        attr("campos", ListaEspecificacaoCampos)
    )


class CrieIndice(str):
    grammar = (
        re.compile(r"crie\s+[ií]ndice|ci"),
        attr("nome_arquivo", word),
        attr("organizacao", OrganizacaoRegistro),
    )
    comando = "crie índice"


class InsiraRegistro(str):
    grammar = (
        attr("comando", re.compile("insira registro|ir")),
    )


class Comando(List):
    grammar = maybe_some([
        # comandos
        some(
            [
                CrieArquivo,
                CrieIndice,
                InsiraRegistro,
                ";"
            ], ";"
        ),

        # comentário
        ignore(comment_sh),
    ])


import inspect


def ins(c):
    for m in inspect.getmembers(c):
        if m[0][0] != "_": print(m)


for comando in [
    "crie arquivo outroteste com x:real binário, a: data fixo(10);",
    "ca teste terminador com nome_arquivo: cadeia terminador,"
    "telefone: inteiro prefixado;",
    """crie    arquivo  arq fixo(10) com
        nome_arquivo: inteiro terminador, x: real fixo(20);
    ir;
    ci a fixo;""",
    "# nada aqui...",
    "ci a fixo; # nothing",
    "insira registro;",
    "ir;"
]:
    # print(">", comando)
    try:
        k = parse(comando, Comando)
    except SyntaxError as erro:
        print(f"Erro em {erro.lineno}, {erro.offset}")
        print(comando.split('\n')[erro.lineno - 1])
        print(f"{'':>{erro.offset - 1}}^-- Erro de sintaxe")
    else:
        print("k", k)
        for c in k:
            # ins(c)
            c.comando = comando_canonico(c.comando)
            print(":", c.comando)
            # if c.comando == "crie arquivo":
            #     print("::", c.nome_arquivo, c.tipo_registro,
            #           c.comprimento if hasattr(c, "comprimento") else "")
            #     for campo in c.campos:
            #         print(":::", campo.name, campo.tipo_campo,
            #               campo.organizacao_campo, campo.comprimento)
            #     print("\n\n\n")
        print()
