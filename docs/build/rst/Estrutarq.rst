
Pacote ``estrutarq``
********************

O pacote ``estrutarq`` reúnde uma série de recursos para o
entendimento de diversas formas de estruturação de dados em arquivos e
em várias formas organizacionais.

Este pacote foi moldado para dar suporte ao livro *Estruturas de
arquivos: uma abordagem prática*.

A implementação desenhada é simplificada. Em especial:

*   o código é voltado à legibilidade e não ao desempenho

*   controle e recuperação de erros são mantidos no nível mínimo,
    restrito ao âmbito de controle de exceções

*   aspectos de acesso simultâneo aos dados são ignorados e, assim,
    não estão disponíveis mecanismos de exclusão mútua ou
    escalonamento de acesso

*   `Pacote estrutarq.dado <Estrutarq.Dado>`_
    *   `Módulo dado_comum <Estrutarq.Dado#modulo-dado-comum>`_
        *   `Dado básico <Estrutarq.Dado#dado-basico>`_
        *   `Dado bruto <Estrutarq.Dado#dado-bruto>`_
        *   `Dado com terminador
            <Estrutarq.Dado#dado-com-terminador>`_
        *   `Dado prefixado pelo comprimento
            <Estrutarq.Dado#dado-prefixado-pelo-comprimento>`_
        *   `Dado binário <Estrutarq.Dado#dado-binario>`_
        *   `Dado de comprimento fixo
            <Estrutarq.Dado#dado-de-comprimento-fixo>`_
*   `Pacote estrutarq.campo <Estrutarq.Campo>`_
    *   `Módulo campo_comum <Estrutarq.Campo#modulo-campo-comum>`_
        *   `Campo básico <Estrutarq.Campo#campo-basico>`_
    *   `Módulo campo_cadeia <Estrutarq.Campo#modulo-campo-cadeia>`_
        *   `Campo cadeia básico
            <Estrutarq.Campo#campo-cadeia-basico>`_
        *   `Campo cadeia com terminador
            <Estrutarq.Campo#campo-cadeia-com-terminador>`_
        *   `Campo cadeia prefixado pelo comprimento
            <Estrutarq.Campo#campo-cadeia-prefixado-pelo-comprimento>`_
        *   `Campo cadeia de comprimento fixo
            <Estrutarq.Campo#campo-cadeia-de-comprimento-fixo>`_
    *   `Módulo campo_inteiro <Estrutarq.Campo#modulo-campo-inteiro>`_
        *   `Campo inteiro básico
            <Estrutarq.Campo#campo-inteiro-basico>`_
        *   `Campo inteiro com terminador
            <Estrutarq.Campo#campo-inteiro-com-terminador>`_
        *   `Campo inteiro prefixado pelo comprimento
            <Estrutarq.Campo#campo-inteiro-prefixado-pelo-comprimento>`_
        *   `Campo inteiro binário
            <Estrutarq.Campo#campo-inteiro-binario>`_
        *   `Campo inteiro de comprimento fixo
            <Estrutarq.Campo#campo-inteiro-de-comprimento-fixo>`_
    *   `Módulo campo_real <Estrutarq.Campo#modulo-campo-real>`_
        *   `Campo real básico <Estrutarq.Campo#campo-real-basico>`_
        *   `Campo real com terminador
            <Estrutarq.Campo#campo-real-com-terminador>`_
        *   `Campo real prefixado pelo comprimento
            <Estrutarq.Campo#campo-real-prefixado-pelo-comprimento>`_
        *   `Campo real binário <Estrutarq.Campo#campo-real-binario>`_
        *   `Campo real de comprimento fixo
            <Estrutarq.Campo#campo-real-de-comprimento-fixo>`_
*   `Pacote estrutarq.registro <Estrutarq.Registro>`_
    *   `Módulo estrutarq.registro.registro_comum
        <Estrutarq.Registro#module-estrutarq.registro.registro_comum>`_
*   `estrutarq.arquivo package <Estrutarq.Arquivo>`_
    *   `Submodules <Estrutarq.Arquivo#submodules>`_
    *   `estrutarq.arquivo.arquivo_comum module
        <Estrutarq.Arquivo#module-estrutarq.arquivo.arquivo_comum>`_
    *   `Module contents <Estrutarq.Arquivo#module-contents>`_
*   `estrutarq.utilitarios package <Estrutarq.Utilitarios>`_
    *   `Submodules <Estrutarq.Utilitarios#submodules>`_
    *   `estrutarq.utilitarios.disco module
        <Estrutarq.Utilitarios#module-estrutarq.utilitarios.disco>`_
    *   `estrutarq.utilitarios.dispositivo module
        <Estrutarq.Utilitarios#module-estrutarq.utilitarios.dispositivo>`_
    *   `estrutarq.utilitarios.geral module
        <Estrutarq.Utilitarios#module-estrutarq.utilitarios.geral>`_
    *   `estrutarq.utilitarios.interpretador module
        <Estrutarq.Utilitarios#estrutarq-utilitarios-interpretador-module>`_
    *   `Module contents <Estrutarq.Utilitarios#module-contents>`_