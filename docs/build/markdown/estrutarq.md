# Pacote `estrutarq`

O pacote `estrutarq` reúnde uma série de recursos para o entendimento de
diversas formas de estruturação de dados em arquivos e em várias formas
organizacionais.

Este pacote foi moldado para dar suporte ao livro Estruturas de arquivos: uma
abordagem prática.

A implementação desenhada é simplificada. Em especial:


* o código é voltado à legibilidade e não ao desempenho


* controle e recuperação de erros são mantidos no nível mínimo, restrito ao
âmbito de controle de exceções


* aspectos de acesso simultâneo aos dados são ignorados e, assim, não estão
disponíveis mecanismos de exclusão mútua ou escalonamento de acesso

<!-- Licença: GNU GENERAL PUBLIC LICENSE V.3, 2007
Jander Moreira, 2021-2022 -->

* [Pacote `estrutarq.dado`](estrutarq.dado.md)


    * [Módulo `dado_comum`](estrutarq.dado.md#modulo-dado-comum)


        * [Dado básico](estrutarq.dado.md#dado-basico)


        * [Dado bruto](estrutarq.dado.md#dado-bruto)


        * [Dado com terminador](estrutarq.dado.md#dado-com-terminador)


        * [Dado prefixado pelo comprimento](estrutarq.dado.md#dado-prefixado-pelo-comprimento)


        * [Dado binário](estrutarq.dado.md#dado-binario)


        * [Dado de comprimento fixo](estrutarq.dado.md#dado-de-comprimento-fixo)


* [Pacote `estrutarq.campo`](estrutarq.campo.md)


    * [Organização básica](estrutarq.campo.md#module-estrutarq.campo.campo_comum)


        * [Campo básico](estrutarq.campo.md#campo-basico)


        * [Campo bruto](estrutarq.campo.md#campo-bruto)


    * [Cadeias de caracteres](estrutarq.campo.md#module-estrutarq.campo.campo_cadeia)


        * [Campo cadeia básico](estrutarq.campo.md#campo-cadeia-basico)


        * [Campo cadeia com terminador](estrutarq.campo.md#campo-cadeia-com-terminador)


        * [Campo cadeia prefixado pelo comprimento](estrutarq.campo.md#campo-cadeia-prefixado-pelo-comprimento)


        * [Campo cadeia de comprimento fixo](estrutarq.campo.md#campo-cadeia-de-comprimento-fixo)


    * [Valores inteiros](estrutarq.campo.md#module-estrutarq.campo.campo_inteiro)


        * [Campo inteiro básico](estrutarq.campo.md#campo-inteiro-basico)


        * [Campo inteiro com terminador](estrutarq.campo.md#campo-inteiro-com-terminador)


        * [Campo inteiro prefixado pelo comprimento](estrutarq.campo.md#campo-inteiro-prefixado-pelo-comprimento)


        * [Campo inteiro binário](estrutarq.campo.md#campo-inteiro-binario)


        * [Campo inteiro de comprimento fixo](estrutarq.campo.md#campo-inteiro-de-comprimento-fixo)


    * [Valores reais](estrutarq.campo.md#module-estrutarq.campo.campo_real)


        * [Campo real básico](estrutarq.campo.md#campo-real-basico)


        * [Campo real com terminador](estrutarq.campo.md#campo-real-com-terminador)


        * [Campo real prefixado pelo comprimento](estrutarq.campo.md#campo-real-prefixado-pelo-comprimento)


        * [Campo real binário](estrutarq.campo.md#campo-real-binario)


        * [Campo real de comprimento fixo](estrutarq.campo.md#campo-real-de-comprimento-fixo)


* [Pacote `estrutarq.registro`](estrutarq.registro.md)


    * [Módulo `estrutarq.registro.registro_comum`](estrutarq.registro.md#modulo-estrutarq-registro-registro-comum)


* [Pacote `estrutarq.arquivo`](estrutarq.arquivo.md)


* [Pacote estrutarq.utilitarios](estrutarq.utilitarios.md)
