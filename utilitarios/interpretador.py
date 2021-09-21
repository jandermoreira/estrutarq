"""
Interpretador de comandos para manipulação de arquivos, registros e
campos
"""
import re

from pypeg2 import *


def comando_canonico(cadeia: str) -> str:
    """
    Limpa uma cadeia de caracteres, deixando-a em uma forma canônica.
    :param cadeia: cadeia de caracteres
    :return: a cadeia na forma canônica

    Forma canônica: somente minúsculas, sem brancos antes ou depois,
    espaçamento simples entre palavras.
    """
    return " ".join(cadeia.split())


class Comprimento(str):
    grammar = "(", re.compile(r"\d+"), ")"


class TipoRegistro(Keyword):
    grammar = Enum(
        K("terminador"),
        K("prefixado"),
        K("fixo"),
    )


class TipoCampo(Symbol):
    grammar = Enum(
        K("bruto"),
        K("terminador"),
        K("prefixado"),
        K("fixo")
    )


class CrieArquivo(str):
    grammar = (
        re.compile(r"crie\s+arquivo|ca"),
        attr("nome_arquivo", word),
        optional(TipoRegistro, optional(Comprimento)),
    )


class CrieIndice(str):
    grammar = (
        re.compile(r"crie\s+[ií]ndice|ci"),
        attr("nome_arquivo", word),
        attr("organizacao", TipoRegistro),
    )


class InsiraRegistro(str):
    grammar = (
        re.compile("insira registro|ir")
    )


class Comando(List):
    grammar = maybe_some([
        flag("crie_arquivo", CrieArquivo),
        CrieIndice,
        InsiraRegistro,
    ]), endl


import inspect

for comando in [
    "ca teste terminador",
    "crie    arquivo outro_teste prefixado",
    """ca um terminador(10)
ca dois fixo(17)
crie índice a terminador
insira registro
ca tres fixo(3)
    """,
    "insira registro",
    "ir"
]:
    # print(">", comando)
    try:
        k = parse(comando, Comando)
    except SyntaxError as erro:
        print("Erro na linha", erro.lineno)
        print(comando.split('\n')[erro.lineno - 1])
        print(f"{'':>{erro.offset - 1}}^")
        # for m in inspect.getmembers(erro):
        #     if m[0][0] != "_": print(m)
    else:
        print("k", k)
        for i, c in enumerate(k):
            print(type(c))
            nome_comando = comando_canonico(c)
            print(":", nome_comando)
            if nome_comando[0] in ["ca", "crie arquivo"]:
                print("::", i, "-", c.nome_arquivo, c.tipo_registro)
        print()

# from pyleri import Grammar, Regex, Sequence, Keyword, Choice, Repeat, Optional, \
#     Ref
#
#
# # Create a Grammar Class to define the format
# class LinguagemDeDados(Grammar):
#     # # Valores
#     # # r_inteiro = Regex("[0-9]+")
#     nome = Regex("[a-zA-Z0-9._]+")
#     #
#     # # Tipos de dados
#     # # k_inteiro = Keyword("int")
#     # # k_real = Keyword("real")
#     # # s_tipo = Choice(k_inteiro, k_real)
#     #
#     # Tipos de organização
#     tipo_bruto = Regex("bruto|b")
#     tipo_terminador = Regex("terminador|term|t")
#     tipo_prefixado = Regex("prefixado|pre|pref|p")
#     tipo_fixo = Regex("fixo|f")
#     tipo_registro = Choice(
#         tipo_terminador,
#         tipo_prefixado,
#         tipo_fixo,
#         tipo_bruto,
#     )
#     #
#     # Comandos de arquivos
#     nome_crie_arquivo = Regex("crie arquivo|ca")
#     CRIE_ARQUIVO = Sequence(nome_crie_arquivo, nome, Optional('usando'),
#                             tipo_registro)
#     #
#     # nome_remova_arquivo = Regex("remova arquivo|ra")
#     # REMOVA_ARQUIVO = Sequence(nome_remova_arquivo, nome)
#     #
#     # # Comandos de índices
#     arvore_b = Regex("[aá]rvore *b|b")
#     hash = Regex("hash|h")
#     nome_crie_indice = Regex("crie [ií]ndice|ci")
#     CRIE_INDICE = Sequence(nome_crie_indice, Choice(arvore_b, hash),
#                            "para", nome)
#     # # nome_remova_indice = Regex("remova [ií]ndice|ri")
#     #
#     START = Choice(
#         CRIE_ARQUIVO,
#         CRIE_INDICE,
#     )
#
#
# # Returns properties of a node object as a dictionary:
# # def node_props(node, children):
# #     return {
# #         'start': node.start,
# #         'end': node.end,
# #         'name': node.element.name if hasattr(node.element, 'name') else None,
# #         'element': node.element.__class__.__name__,
# #         'string': node.string,
# #         'children': children}
# #
# #
# # # Recursive method to get the children of a node object:
# # def get_children(children):
# #     return [node_props(c, get_children(c.children)) for c in children]
# #
# #
# # # View the parse tree:
# # def view_parse_tree(res):
# #     start = res.tree.children[0] if res.tree.children else res.tree
# #     return node_props(start, get_children(start.children))
#
#
# comando = "crie arquivo dados usando terminador"
#
# # p = LinguagemDeDados()
# # c = p.parse(comando)
# # print(comando)
# # import pprint
# #
# # pp = pprint.PrettyPrinter()
# # # pp.pprint(view_parse_tree(c))
# # print(view_parse_tree(c))
#
#
# class Interpretador:
#     def execute(self, comando: str):
#         estrutura_comando = ((LinguagemDeDados())).parse(comando)
#         if not estrutura_comando.is_valid:
#             print(comando)
#             print(f"{'^':>{estrutura_comando.pos + 1}s}--- esperado: " +
#                   f"{str(estrutura_comando.expecting)[1:-1]}\n")
#         else:
#             if not hasattr(self, "_comando"):
#                 self._comando = {}
#             print(self.view_parse_tree(estrutura_comando))
#
#     def node_props(self, node, children):
#         return {
#             'start': node.start,
#             'end': node.end,
#             'name': node.element.name if hasattr(node.element,
#                                                  'name') else None,
#             'element': node.element.__class__.__name__,
#             'string': node.string,
#             'children': children}
#
#     # Recursive method to get the children of a node object:
#     def get_children(self, children):
#         return [self.node_props(c, self.get_children(c.children)) for c in children]
#
#     # View the parse tree:
#     def view_parse_tree(self, res):
#         start = res.tree.children[0] if res.tree.children else res.tree
#         return self.node_props(start, self.get_children(start.children))
#
# interpretador = Interpretador()
# interpretador.execute(comando)
