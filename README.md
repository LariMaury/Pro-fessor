# Gerenciador de notas de caderno

Ferramenta desktop desenvolvida para automação de processos pedagógicos e otimização do tempo de lançamento de notas escolares. O sistema automatiza o cálculo de regras de três simples para notas proporcionais de cadernos e integra os resultados diretamente em planilhas do Excel, permitindo uma gestão eficiente para diferentes turmas e séries.

---

## Funcionalidades

*   **Configuração dinâmica:** Fixação do valor máximo do caderno e do total de atividades da etapa uma única vez ao iniciar o sistema.
*   **Seleção de turmas:** Interface gráfica integrável que permite navegar nos arquivos do computador e carregar planilhas específicas (`.xlsx`) de diferentes séries.
*   **Fluxo de chamada inteligente:** Exibe o nome do aluno em destaque, posiciona o cursor automaticamente para digitação e avança para o próximo registro ao pressionar a tecla `Enter`.
*   **Engenharia de dados direta:** Lê a lista de chamada e grava as notas finais calculadas em tempo real na coluna correspondente da planilha selecionada.

---

## Tecnologias Utilizadas

*   **Python 3:** Linguagem base do projeto.
*   **CustomTkinter:** Biblioteca de interface gráfica (GUI) moderna com suporte nativo a temas do sistema (modo escuro/claro).
*   **Pandas & OpenPyXL:** Manipulação, tratamento e persistência de dados em arquivos de planilhas.
*   **PyInstaller:** Compilação do código-fonte em um executável portável `.exe` isolado de console.

---

## Estrutura da Planilha (`.xlsx`)

Para o correto funcionamento do sistema, as planilhas das turmas precisam conter ao menos a seguinte estrutura na primeira linha (cabeçalho):

| Nome | Nota |
|---|---|
| Aluno A | *[Preenchido pelo sistema]* |
| Aluno B | *[Preenchido pelo sistema]* |

---

## Sobre a autora

Desenvolvido por **Maurylia Loureiro**  
Estudante de Ciência da Computação na Gran Faculdade e Graduada em Letras. Apaixonada por aplicar a lógica da programação para resolver problemas reais e otimizar fluxos de trabalho no ambiente educacional.

*   **LinkedIn:** https://www.linkedin.com/in/maurylia-loureiro-1154ab11a/
*   **E-mail:** maurylia@gmail.com

---

> *Nota de Desenvolvimento: Este projeto foi concebido e estruturado com foco em arquitetura de software limpa, contando com o apoio de ferramentas de inteligência artificial generativa para o refinamento estético da interface de usuário.*
