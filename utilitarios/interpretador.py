"""
Interpretador de comandos para manipulação de arquivos, registros e
campos
"""

from pyleri import Grammar, Regex, Sequence, Keyword, Choice


# Create a Grammar Class to define the format
class LinguagemDeDados(Grammar):
    # Valores
    # r_inteiro = Regex("[0-9]+")

    # Tipos de dados
    # k_inteiro = Keyword("int")
    # k_real = Keyword("real")
    # s_tipo = Choice(k_inteiro, k_real)

    # Comandos
    r_crie_arquivo = Regex("crie arquivo|ca")
    r_remova_arquivo = Regex("remova arquivo|ra")
    r_crie_indice = Regex("crie [ií]ndice|ci")
    r_remova_indice = Regex("remova [ií]ndice|ri")

    s_comando = Choice(r_crie_arquivo, r_remova_arquivo, r_crie_indice,
                       r_remova_indice)
    START = Sequence(s_comando)


# Compile your grammar by creating an instance of the Grammar Class.
interpretador = LinguagemDeDados()


# Returns properties of a node object as a dictionary:
def node_props(node, children):
    return {
        'start': node.start,
        'end': node.end,
        'name': node.element.name if hasattr(node.element, 'name') else None,
        'element': node.element.__class__.__name__,
        'string': node.string,
        'children': children}


# Recursive method to get the children of a node object:
def get_children(children):
    return [node_props(c, get_children(c.children)) for c in children]


# View the parse tree:
def view_parse_tree(res):
    start = res.tree.children[0] if res.tree.children else res.tree
    return node_props(start, get_children(start.children))


import pprint

pp = pprint.PrettyPrinter()

comando = "remova indice"
c = interpretador.parse(comando)
print(comando)
if not c.is_valid:
    print(f"{'^':>{c.pos + 1}s}--- esperado: {str(c.expecting)[1:-1].replace(', ', ' ou ')}\n")
pp.pprint(view_parse_tree(c))
