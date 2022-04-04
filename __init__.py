"""
O pacote ``estrutarq`` reúnde uma série de recursos para o entendimento de
diversas formas de estruturação de dados em arquivos e em várias formas
organizacionais.

Este pacote foi moldado para dar suporte ao livro `Estruturas de arquivos: uma
abordagem prática`.

A implementação desenhada é simplificada. Em especial:

* o código é voltado à legibilidade e não ao desempenho

* controle e recuperação de erros são mantidos no nível mínimo, restrito ao
  âmbito de controle de exceções

* aspectos de acesso simultâneo aos dados são ignorados e, assim, não estão
  disponíveis mecanismos de exclusão mútua ou escalonamento de acesso

..
    Licença: GNU GENERAL PUBLIC LICENSE V.3, 2007
    Jander Moreira, 2021-2022
"""