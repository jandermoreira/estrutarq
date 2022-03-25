"""
Testes para classes de dados
"""
from os import remove, system

from estrutarq.dado import *


def imprima(msg, dado):
    print(f"> {msg}: {dado} / {len(dado)}")


def verifique(dado1, dado2, termina = True):
    global numero_verificacoes
    global numero_falhas
    numero_verificacoes += 1
    if dado1 == dado2:
        print("Tudo ok")
    else:
        numero_falhas += 1
        print("Verificação:", dado1, "!=", dado2, " <-------------")
        # if termina:
        #     exit(1)


def teste_classe(dado, classe):
    print(f"Testando: {type(classe).__name__}")
    imprima("dado", dado)
    dado_formatado = classe.adicione_formatacao(dado)
    imprima("dado formatado", dado_formatado)
    dado_desformatado = classe.remova_formatacao(dado_formatado)
    imprima("dado desformatado", dado_desformatado)
    verifique(dado_desformatado, dado,
              termina = type(classe).__name__ != "DadoFixo")

    with open("/tmp/teste-dados.tmp", "wb") as arquivo:
        arquivo.write(dado_formatado + dado + b"X")
    system("hd /tmp/teste-dados.tmp")
    with open("/tmp/teste-dados.tmp", "rb") as arquivo:
        dado_lido = classe.leia_de_arquivo(arquivo)
        imprima("dado gravado e lido de arquivo", dado_lido)
        verifique(dado_lido, dado,
                  termina = type(classe).__name__ != "DadoFixo")
        bytes_restantes = arquivo.read(1024)
        imprima("bytes restantes no arquivo", bytes_restantes)
        verifique(bytes_restantes, dado + b"X")
    remove("/tmp/teste-dados.tmp")

    dado_escaneado, resto = classe.leia_de_bytes(dado_formatado + dado + b"X")
    imprima("dado obtido de sequência de bytes", dado_escaneado)
    verifique(dado_escaneado, dado,
              termina = type(classe).__name__ != "DadoFixo")
    imprima("restante da sequência de bytes", resto)
    verifique(resto, dado + b"X")

    print()
    print(f"Erros/Total: {numero_falhas / numero_verificacoes * 100:.2f}%")
    print(f"{numero_falhas}/{numero_verificacoes}")


def main():
    global numero_verificacoes
    global numero_falhas
    numero_verificacoes = 0
    numero_falhas = 0

    dado = b'\xffA\x00B\x01C\xfeD\xffE'
    teste_classe(dado, DadoBinario(len(dado)))
    teste_classe(dado, DadoFixo(len(dado) + 5))
    teste_classe(dado, DadoFixo(len(dado) - 5))
    teste_classe(dado, DadoPrefixado())
    teste_classe(dado, DadoTerminador(b'\x00'))


if __name__ == "__main__":
    main()
