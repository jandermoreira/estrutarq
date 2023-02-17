"""
Teste de hash linear
"""

quantidade = 0
nivel = 0


def hash(chave, nivel):
    return chave % (tamanho * 2 ** nivel)


posicao_divisao = 0


def insira(chave):
    global posicao_divisao
    global nivel
    global quantidade

    if hash(chave, nivel < posicao_divisao):
        endereco = hash(chave, nivel)
    else:
        endereco = hash(chave, nivel + 1)

    print(f"Chave {chave} --> {endereco}")
    quantidade += 1


tamanho = 5
for nivel in range(3):
    print(f"h0 = C mod {tamanho * 2 ** nivel}", end = ";\t")
    print(f"h1 = C mod {tamanho * 2 ** (nivel + 1)}")
