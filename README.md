# Aula 7 — Programação da produção

## Objetivo

Apresentar a relação entre roteiro, carregamento, sequenciamento e programação
da produção, com exemplos que permitam comparar regras de prioridade e analisar
a capacidade dos recursos.

## Arquivos principais

- `index.Rmd`: fonte editável da apresentação publicada;
- `index.html`: apresentação renderizada;
- `slides.css`: estilos da apresentação;
- `setup.Rmd`: configuração comum do xaringan;
- `index_files/figure-html/`: gráficos gerados durante a renderização;
- `gabaritos/`: gabarito docente, script de geração e documentação dos cálculos;
- `index1.Rmd` e `index1.html`: variante preservada, sem alterações nesta etapa.

## Melhorias realizadas em 29/10/2026

- inclusão do contexto entre PMP, MRP e programação operacional;
- distinção entre roteiro, carregamento, sequenciamento e programação;
- exemplo de cálculo da carga de um lote a partir do roteiro;
- comparação de FIFO, MTP, MDE e MFE na mesma carteira de ordens;
- correção do fluxo médio, calculado como média dos tempos de conclusão quando
  todos os trabalhos chegam no tempo zero;
- padronização do exemplo de sequenciamento em horas;
- exemplo de carga finita e infinita com 20 horas disponíveis por máquina;
- diagnóstico do déficit de 4,25 horas no Torno-02 e alternativas de decisão;
- pausa para resolução do estudo de caso antes dos slides de solução;
- revisão da seção de ferramentas e do protocolo de publicação do programa;
- remoção das dependências não utilizadas `DiagrammeR` e `plotly`.
- revisão da diagramação, com hierarquia tipográfica mais compacta e melhor
  aproveitamento do formato 16:9;
- correção do contraste em destaques com fundo azul claro e padronização das
  cores das tabelas;
- aplicação da mesma cor escura e do mesmo peso tipográfico da primeira linha
  a todo o conteúdo das caixas de perguntas, atividades, dicas e decisões;
- substituição do endereço `places.education` no rodapé pelo texto
  `Programação da Produção - Aula 07`;
- aplicação integral do estilo da primeira linha a todos os elementos internos
  das caixas de perguntas, atividades, dicas e decisões;
- remoção do negrito nas caixas de destaque, mantendo o mesmo peso regular em
  todas as linhas e elementos internos;
- transformação dos destaques em blocos de largura integral, para que fundo,
  borda e espaçamento permaneçam contínuos quando o texto ocupar várias linhas;
- inclusão de contadores clicáveis com o pacote `countdown` nas quatro
  atividades com tempo definido, posicionados no canto inferior direito;
- revisão da tabela do exemplo de carga, com remoção das colunas derivadas
  redundantes, rótulos didáticos e larguras ajustadas ao slide;
- identificação das linhas de referência do gráfico de utilização na legenda:
  atenção em 85% e capacidade em 100%;
- centralização horizontal e vertical de todas as informações do primeiro
  slide;
- adequação das tabelas da análise de carga e do caso completo, com rótulos
  compactos, larguras controladas, rolagem bidirecional e cabeçalho fixo no
  roteiro de 15 operações;
- revisão da tabela de solução do sequenciamento por prioridade, eliminando a
  coluna de prazo duplicada e adicionando rolagem horizontal;
- inclusão de respostas e gabaritos nas notas do apresentador, acessíveis pela
  tecla `P` durante a apresentação xaringan;
- síntese das notas do apresentador, mantendo apenas respostas-chave, cálculos
  de conferência e decisões esperadas;
- remoção da discussão de 4 minutos sobre prioridade estratégica, incluindo o
  contador e a respectiva nota do apresentador;
- inclusão de um slide sobre folga estática, com fórmula, interpretação dos
  sinais, exemplo e gráfico da carteira A–E;
- divisão da explicação de folga estática em dois slides, separando conceito e
  gráfico para preservar legibilidade e encaixe;
- compactação adicional dos slides de folga estática, com fórmula em uma linha,
  menos títulos internos e gráfico menor;
- correção do fluxo das colunas no slide conceitual de folga estática, mantendo
  a explicação final abaixo das duas colunas;
- inclusão de uma definição sintética de APS no slide de ferramentas;
- explicitação da sigla APS como *Advanced Planning and Scheduling*
  (Planejamento e Programação Avançados);
- remoção da atividade de 6 minutos sobre comparação das regras, incluindo o
  contador e o gabarito das notas do apresentador;
- remoção da atividade de 5 minutos sobre alternativas para o déficit,
  incluindo contador e nota do apresentador;
- ampliação equilibrada das fontes de títulos, corpo, tabelas, códigos e
  rodapé, com ajuste dos espaçamentos para preservar o encaixe dos slides;
- criação de um gabarito comentado para todas as perguntas e atividades em
  sala, incluindo cálculos, interpretações e critérios sugeridos de correção;
- separação dos dados dos pedidos e do roteiro do estudo de caso em dois
  slides, preservando a legibilidade.

## Convenções dos exemplos

- todos os trabalhos do exemplo de regras estão disponíveis no tempo zero;
- fluxo de um trabalho = término − chegada;
- atraso = máximo entre zero e término − prazo;
- MFE usa folga estática no tempo zero;
- empates são resolvidos pela ordem de chegada;
- carga = setup + tempo unitário × quantidade;
- utilização = carga ÷ capacidade disponível.

## Reprodução

No diretório da aula, renderizar com:

```r
rmarkdown::render("index.Rmd", output_file = "index.html")
```

O Pandoc distribuído com o RStudio pode ser indicado pela variável
`RSTUDIO_PANDOC` quando não estiver disponível no `PATH`.
