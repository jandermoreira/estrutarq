"""
Interpretador de comandos para manipulação de arquivos, registros e
campos
"""

from pypeg2 import *

abreviacoes_comandos = {
    "ca": "crie arquivo",
    "ci": "crie índice",
    "ir": "insira registro_teste"
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
        attr("comprimento_bloco", optional(Comprimento)),
    )


class ListaEspecificacaoCampos(List):
    grammar = EspecificacaoCampo, maybe_some(",", EspecificacaoCampo)


class CrieArquivo(str):
    grammar = (
        attr("comando", re.compile(r"crie\s+arquivo|ca")),
        attr("nome_arquivo", word),
        attr("tipo_registro", optional(OrganizacaoRegistro)),
        attr("comprimento_bloco", optional(Comprimento)),
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
        attr("comando", re.compile("insira registro_teste|ir")),
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
    "insira registro_teste;",
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
            #           c.comprimento_bloco if hasattr(c, "comprimento_bloco") else "")
            #     for campo in c.campos:
            #         print(":::", campo.name, campo.tipo_campo,
            #               campo.organizacao_campo, campo.comprimento_bloco)
            #     print("\n\n\n")
        print()


#         $ rsync - -version
#         rsync
#         version
#         3.2
#         .3
#         protocol
#         version
#         31
#         Copyright(C)
#         1996 - 2020
#         by
#         Andrew
#         Tridgell, Wayne
#         Davison, and others.
#         Web
#         site: https: // rsync.samba.org /
#         Capabilities:
#         64 - bit
#         files, 64 - bit
#         inums, 64 - bit
#         timestamps, 64 - bit
#         long
#         ints,
#         socketpairs, hardlinks, hardlink - specials, symlinks, IPv6, atimes,
#         batchfiles, inplace, append, ACLs, xattrs, optional
#         protect - args, iconv,
#         symtimes, prealloc, stop - at, no
#         crtimes
#     Optimizations:
#     SIMD, no
#     asm, openssl - crypto
# Checksum
# list:
# xxh128
# xxh3
# xxh64(xxhash)
# md5
# md4
# none
# Compress
# list:
# zstd
# lz4
# zlibx
# zlib
# none
