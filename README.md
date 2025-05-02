## PRESSUPOSTOS DE GOLOMB - Criptografia
Ferramenta em Python para análise de sequências binárias com base nos postulados de Golomb: balanceamento, distribuição de sequências e autocorrelação.

Este programa realiza a análise de uma sequência binária para verificar se ela cumpre os três pressupostos de Golomb:
1. **Proporção entre zeros e uns**: Percentagens de 0’s e 1’s dentro de uma margem aceitável.  
2. **Frequência de subsequências de tamanhos diferentes**: Blocos menores devem ocorrer mais vezes que blocos maiores.  
3. **Distribuição equilibrada de padrões binários**: Evita repetições ou “espelhamentos” indesejados.

<br>

## Índice
- [Como Funciona?](#como-funciona)
- [Como Usar?](#como-usar)
- [Parâmetros](#parâmetros)
- [Exemplo de Resultado](#exemplo-de-resultado)
- [Contribuição](#contribuição)
- [Licença](#licença)

<br>

## Como Funciona?

1. **O programa apresenta duas opções:**
   - Analisar uma sequência existente;  
   - Gerar uma nova sequência (aleatória ou que cumpra os pressupostos).

2. **Para Análise:** 
   - Recebe uma sequência binária do usuário.  
   - Extrai dados básicos: número de bits, blocos contínuos, frequências e tamanhos em ordem.  
   - Verifica cada um dos três pressupostos, acumulando informações sobre conformidade, avisos relevantes e alertas.
   - Exibe um relatório final com ✔/✘ e mensagens de alerta.

3. **Para Geração:**
   - O usuário pode gerar uma sequência binária aleatória ou que satisfaça os pressupostos de Golomb.
   - O programa solicita o comprimento da sequência e os pressupostos a serem ativados.  
   - Tenta gerar até 5.000 sequências aleatórias que cumpram os requisitos.  
   - Exibe a sequência válida gerada.

<br>

## Como Usar?
1. Clone o repositório:  
   `git clone https://github.com/Nespre/bitstream-verifier.git`

2. Navegue até o diretório do projeto:  
   `cd bitstream-verifier`

3. Execute o script Python desejado. Exemplo:  
   `pressuposto_golomb.py`

<br>

## Parâmetros
Estes valores são internos ao programa e representam os dados usados em cada verificação:

- **num_bits** (`dict`): Contagens totais de bits

        all: número de bits,
        zeros: contagem de 0’s,
        ones: contagem de 1’s.

- **runs** (`dict`): Listas de blocos contínuos encontrados em

        all,
        zeros,
        ones.

- **run_frequencies** (`dict`): Frequência de ocorrência de cada tamanho de bloco em

        all,
        zeros,
        ones.

- **ordered_run_sizes** (`dict`): Tamanhos dos blocos, na ordem em que aparecem, em

        all,
        zeros,
        ones.

- **postulates** (`dict`): Para cada pressuposto (1, 2 e 3), armazena:

        comply (bool),
        relevants (list[str]),
        warnings (list[str]).

<br>

## Tipos de Verificação por Pressupostos
### Pressuposto 1 – Proporção de Bits
**Função**: `check_first_postulate()`<br>
Verifica se há equilíbrio entre a quantidade de 0’s e 1’s na sequência.

**Regras**:<br>
A percentagem mínima permitida para cada bit (0 ou 1) depende do comprimento da sequência:
- `≤ 10`: 40.00%
- `11–20`: 0.5 * length + 35 (ex: length 16 → 43.5%)
- `21–1000`: 41.6 + 1.15 * ln(length)
- `> 1000`: 49.00%

**Exemplo**:

		Sequência: 00001001
		0's: 75.00%
		1's: 25.00%
		Mínimo permitido: 40.00%
		→ Não cumpre pressuposto 1

<br>

## Exemplo de Resultado
**Pressupostos de Golomb analisados:**
1. Proporção (✔)  
2. Frequência (✘) — “Blocos de tamanho 1 (5) não mais frequentes que tamanho 2 (5)” 
3. Padrões   (✘) — “Repetição de [00 1]”  

**Tabela Resumo:**

| Pressuposto | Status | Mensagens |
|-------------|:------:|----------:|
|     1       |   ✔    | —        |
|     2       |   ✘    | Blocos de tamanho 1 não são mais frequentes |
|     3       |   ✘    | Padrão [00, 1] repete-se |

<br>

## Contribuição
Sinta-se à vontade para contribuir! Abra um pull request ou crie um issue para discutir melhorias.

<br>

## Licença
Este projeto está licenciado sob a MIT License. Veja LICENSE para mais detalhes.