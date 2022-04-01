``estrutarq``
*************

.. toctree::
   :maxdepth: 1
   :caption: Conteúdo:

   dado
   campo
   registro
   arquivo
   modules

Introdução
==========

O pacote ``estrutarq`` foi moldado para dar suporte ao livro `Estruturas de arquivos: uma abordagem prática`.

A implementação desenhada é simplificada. Em especial:

* o código é voltado à legibilidade e não ao desempenho
* controle e recuperação de erros são mantidos no nível mínimo, restrito ao âmbito de controle de exceções
* aspectos de acesso simultâneo aos dados são ignorados e, assim, não estão disponíveis mecanismos de exclusão mútua ou escalonamento de acesso
