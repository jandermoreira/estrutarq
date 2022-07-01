"""
Compressão pelo método LZW.

Código baseado no pseudocódigo apresentado em:
Drozdek, A. "Estrutura de dados e algoritmos em C++".
Cengage Learning, 2016

..
    Licença: GNU GENERAL PUBLIC LICENSE V.3, 2007
    Jander Moreira, 2021, 2022
"""

from estrutarq.utilitarios.fluxo import Fluxo


class LZW:
    """

    """

    def __init__(self):
        self.lista_codigos = []

    def processe_de_bytes(self, sequencia: bytes):
        """
        Realiza a compressão da sequência de bytes, considerando que cada
        byte é um símbolo do conjunto original.

        :param sequencia: sequência de bytes
        """
        dicionario = dict([(bytes([x]), x) for x in range(256)])

        simbolo = bytes([sequencia[0]])

        comprimento_longo = 1
        comprimento = 8
        comprimento_codificacao = 0
        self.lista_codigos = []
        n = 1
        for simbolo_corrente in sequencia[1:]:
            simbolo_corrente = bytes([simbolo_corrente])
            if simbolo + simbolo_corrente in dicionario:
                simbolo += simbolo_corrente
                if len(simbolo) > comprimento_longo:
                    comprimento_longo = len(simbolo)
            else:
                self.lista_codigos.append(dicionario[simbolo])
                print(
                    f"[{simbolo.decode('latin'):30s}; {dicionario[simbolo]:>0{comprimento}b}] --- ",
                    end = "")
                print(f"{dicionario[simbolo]:7d}", ' ', end = '')
                dicionario[simbolo + simbolo_corrente] = len(dicionario)
                simbolo = simbolo_corrente
                comprimento_codificacao += comprimento
                print(f" ({n * 8}/{comprimento_codificacao}: " +
                      f"{100 * (n * 8 - comprimento_codificacao) / (n * 8):.1f}%) ")

            if len(dicionario) >= 2 ** comprimento:
                comprimento += 1
                # print(f"comprimento: {comprimento}")
            n += 1
            # if comprimento_codificacao > n * 8:
            #     print(" <<<", len(dicionario))
            # else:
            #     print()
            # if len(dicionario) > 2 ** 12:
            #     self.lista_codigos.append(None)
            #     dicionario = dict([(bytes([x]), x) for x in range(256)])
            #     print("reset")
        self.lista_codigos.append(dicionario[simbolo])
        # print(dicionario[simbolo])
        print(">>>", comprimento_longo)
        print(f"{len(sequencia) * 8}; {comprimento_codificacao}; " +
              f"{100 * (len(sequencia) * 8 - comprimento_codificacao) / len(sequencia) / 8:.1f}")

    def recupere_de_lista(self):

        dicionario = dict([(x, bytes([x])) for x in range(256)])

        codigo_base = self.lista_codigos[0]
        # print(dicionario[codigo_base], end = "")
        sequencia = dicionario[codigo_base]
        comprimento = 8
        for codigo_corrente in self.lista_codigos[1:]:
            if codigo_corrente in dicionario:
                dicionario[len(dicionario)] = dicionario[codigo_base] + \
                                              bytes([dicionario[
                                                         codigo_corrente][0]])
                # print(dicionario[codigo_corrente], end = "")
                sequencia += dicionario[codigo_corrente]
            else:
                dicionario[len(dicionario)] = dicionario[codigo_base] + \
                                              bytes(
                                                  [dicionario[codigo_base][0]])
                # print(dicionario[codigo_base] + bytes([dicionario[codigo_corrente][0]]),
                #       end = "")
                sequencia += dicionario[codigo_base] + \
                             bytes([dicionario[codigo_corrente][0]])
            codigo_base = codigo_corrente
            if codigo_corrente is None:
                dicionario = dict([(x, bytes([x])) for x in range(256)])
        return sequencia
