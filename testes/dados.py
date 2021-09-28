"""
Testes para classes de dados
"""

from estrutarq.dado import *


def imprima(msg, dado):
    print(f"> {msg}: {dado} / {len(dado)}")


def teste_classe(dado, classe):
    print(f"Testando: {type(classe).__name__}")
    imprima("dado", dado)
    dado_formatado = classe.adicione_formatacao(dado)
    imprima("adicione_formatacao", dado_formatado)
    imprima("remova_formatacao", classe.remova_formatacao(dado_formatado))

    with open("/tmp/teste-dados.tmp", "wb") as arquivo:
        arquivo.write(dado_formatado + b'XYZ123ASDF')
    with open("/tmp/teste-dados.tmp", "rb") as arquivo:
        dado_lido = classe.leia_de_arquivo(arquivo)
        imprima("leia_de_arquivo", dado_lido)

    dado_lido, resto = classe.leia_de_bytes(dado_formatado + b"XYZABCDEFGHIJ")
    imprima("leia_de_bytes (dado)", dado_lido)
    imprima("leia_de_bytes (restante)", resto)

    print()


def main():
    dado = b'123 ABC_abc'
    teste_classe(dado, DadoBinario(len(dado)))
    teste_classe(dado, DadoFixo(len(dado) + 5))
    # teste_classe(dado, DadoPrefixado())
    teste_classe(dado, DadoTerminador(b'\x00'))


if __name__ == "__main__":
    main()
