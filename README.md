## PRESSUPOSTO DE GOLOMB - Criptografia
Ferramenta em Python para análise de sequências binárias com base nos postulados de Golomb: balanceamento, distribuição de sequências e autocorrelação.

Este programa realiza a análise de uma sequência binária para verificar se ela cumpre os três pressupostos de Golomb:
1. **Proporção entre zeros e uns**: percentagens de 0’s e 1’s dentro de uma margem aceitável.  
2. **Frequência de subsequências de tamanhos diferentes**: blocos menores devem ocorrer mais vezes que blocos maiores.  
3. **Distribuição equilibrada de padrões binários**: evita repetições ou “espelhamentos” indesejados.

<br><br> 

## Índice
- [Como Funciona?](#como-funciona)
- [Como usar?](#como-usar)
- [Parâmetros](#parâmetros)
- [Exemplo de Resultado](#exemplo-de-resultado)
- [Contribuição](#contribuição)
- [Licença](#licença)
<br><br>

## Como Funciona?

1. **O programa apresenta duas opções:**
   - Analisar uma sequência existente;  
   - Gerar uma nova sequência (aleatória ou que cumpra os pressupostos).

2. **Para análise:** 
   - Recebe uma sequência binária do usuário.  
   - Extrai dados básicos (número de bits, blocos contínuos, frequências e tamanhos em ordem).  
   - Verifica cada um dos três pressupostos, acumulando “compliance”, avisos relevantes e alertas.
   - Exibe um relatório final com ✔/✘ e mensagens de alerta.

3. **Para geração:**
   - O usuário pode gerar uma aleatória ou uma nova sequência binária que satisfaça os pressupostos de Golomb.
   - Pergunta comprimento e quais pressupostos ativar.  
   - Tenta gerar até 5 000 sequências aleatórias que cumpram os requisitos.  
   - Mostra a sequência válida criada.
<br><br>

## Como usar?
1. Clone o repositório: <br> `git clone https://github.com/Nespre/bitstream-verifier.git`

2. Navegue até o diretório do projeto:  <br> `cd bitstream-verifier`

3. Execute o script Python desejado. Exemplo:  <br> `pressuposto_golomb.py`
<br><br>

## Parâmetros
Estes valores são internos ao programa e representam os dados usados em cada verificação:

- **num_bits** (`dict`): contagens totais

        all: número de bits,
		zeros: contagem de 0’s,
        ones: contagem de 1’s.

- **runs** (`dict`): listas de blocos contínuos encontrados em

        all,
        zeros,
        ones.

- **run_frequencies** (`dict`): frequência de ocorrência de cada tamanho de bloco em

        all,
        zeros,
        ones.

- **ordered_run_sizes** (`dict`): tamanhos dos blocos, na ordem em que aparecem, em

        all,
        zeros,
        ones.

- **postulates** (`dict`): para cada pressuposto 1, 2 e 3, armazena:

        comply (bool),
        relevants (list[str]),
        warnings (list[str]).
<br><br>

## Exemplo de Resultado
Pressupostos de Golomb analisados:
1. Proporção (✔)  
2. Frequência (✘) — “Blocos de tamanho 1 (5) não mais frequentes que tamanho 2 (5)” 
3. Padrões   (✘) — “Repetição de [00 1]”  

Tabela resumo:

| Pressup. | Status | Mensagens |
|----------|:------:|----------:|
|    1     | ✔ True | —        |
|    2     | ✘ False | Blocos de tamanho 1 não são mais frequentes |
|    3     | ✘ False | Padrão [00 1] repete-se |

<br>

## Contribuição
Sinta-se à vontade para contribuir! Abra um pull request ou crie um issue para discutir melhorias.
<br><br>

## Licença
Este projeto está licenciado sob a MIT License. Veja LICENSE para mais detalhes.