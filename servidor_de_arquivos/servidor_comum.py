"""
Servidor de arquivos, com função de aceitar requisições de dados simplificadas
e fornecer respostas (registros ou coleções de registros).

..
    Licença: GNU GENERAL PUBLIC LICENSE V.3, 2007
    Jander Moreira, 2021--2023
"""

import socket

class ServidorDeArquivos():
    """"
    Servidor
    """

    def __init__(self, hospedeiro, porta):
        self.hospedeiro = hospedeiro
        self.porta = porta

    def inicie(self) -> None:
        """
        Inicia o servidor em modo de escuta.
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        with self.socket as s:
            s.bind((self.hospedeiro, self.porta))
            s.listen()

            conexao, endereco = s.accept()

            with conexao:
                print(f"Conexão de {endereco}")
                while True:
                    dado_entrada = conexao.recv(1024)
                    if not dado_entrada:
                        break
                    conexao.sendall(dado_entrada)
