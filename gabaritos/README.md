# Gabarito das atividades da Aula 7

## Objetivo

Registrar as respostas esperadas para as perguntas e atividades da apresentação
de Programação da Produção, com cálculos reproduzíveis e critérios de correção.

## Arquivos

- `gabarito_atividades_aula07.docx`: documento docente pronto para uso;
- `01_gerar_gabarito_aula07.py`: script que reconstrói o documento.

## Base utilizada

Os enunciados, tempos, prazos, roteiros, capacidades e regras foram obtidos de
`../index.Rmd`.

## Fórmulas e critérios

- carga da ordem = setup + tempo unitário × quantidade;
- utilização = carga ÷ capacidade disponível;
- término = início + processamento;
- atraso = máximo entre zero e término − prazo;
- fluxo = término − chegada;
- MFE usa folga estática no tempo zero;
- empates são resolvidos pela ordem de chegada ou pela ordem original quando
  todos os demais critérios são iguais.

## Suposições e limitações

- os trabalhos da carteira de regras estão disponíveis no tempo zero;
- não há ociosidade entre trabalhos nas comparações das regras;
- os prazos em dias do estudo de caso foram convertidos em jornadas de oito
  horas;
- a carga agregada por máquina não representa todos os conflitos simultâneos
  de um ambiente job shop;
- a transferência entre tornos depende de compatibilidade de roteiro,
  ferramental, programa, operador e qualidade.

## Reprodução

Executar o script com Python e `python-docx` disponível. O documento será salvo
na mesma pasta do script.
