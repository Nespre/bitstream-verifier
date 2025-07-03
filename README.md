# PRESSUPOSTOS DE GOLOMB - Criptografia
Ferramenta em Python para análise de sequências binárias com base nos postulados de Golomb: balanceamento, distribuição de sequências e autocorrelação.

Este programa realiza a análise de uma sequência binária para verificar se ela cumpre os três pressupostos de Golomb:
1. **Proporção entre zeros e uns**: Percentagens de 0’s e 1’s dentro de uma margem aceitável.  
2. **Frequência de subsequências de tamanhos diferentes**: Blocos menores devem ocorrer mais vezes que blocos maiores.  
3. **Distribuição equilibrada de padrões binários**: Evita repetições ou “espelhamentos” indesejados.

> **Nota:** Este projeto é apenas para fins educacionais.

<br>

## Índice
- [Como Funciona?](#como-funciona)
- [Como Usar?](#como-usar)
- [Parâmetros](#parâmetros)
- [Tipos de Verificação](#tipos-de-verificação-por-pressupostos)
- [Exemplo de Resultado](#exemplo-de-resultado)
- [Contribuição](#contribuição)
- [Licença](#licença)

<br><br>

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

<br><br>

## Como Usar?
1. Clone o repositório:  
   `git clone https://github.com/Nespre/bitstream-verifier.git`

2. Navegue até o diretório do projeto:  
   `cd bitstream-verifier`

3. Execute o script Python desejado. Exemplo:  
   `pressuposto_golomb.py`

<br><br>

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

<br><br>

## Tipos de Verificação por Pressupostos
### Pressuposto 1 – Proporção de Bits
_**Função**_: `check_first_postulate()`<br>
Verifica se a proporção de 0's e 1's está dentro de um limite mínimo aceitável com base no comprimento da sequência.

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
		→ ⚠️ Não cumpre pressuposto 1
<br>

### Pressuposto 2 – Frequência de Blocos
_**Função**_: `verify_frequency_runs()`
Verifica se blocos menores ocorrem com mais frequência que blocos maiores.

**Regras**:
- Um bloco de tamanho n deve ser mais frequente que um de tamanho n+1.
- Se houver empate ou inversão de frequência, o pressuposto é violado.
- Avisos opcionais são emitidos se a diferença for pequena.

**Exemplo**:

	Tamanhos: [1, 1, 2, 2]
	Contagem: [2, 2]
	→ Frequências iguais → ⚠️ Não cumpre
<br>

### Pressuposto 3 – Autocorrelação
Verificações relacionadas a padrões, simetrias ou repetições estruturais nos blocos. <br>
_**Função**_: `verify_sizes_pattern()`
Identifica padrões repetidos nos tamanhos dos blocos.

**Regras**:
- 2 blocos iguais consecutivos → ⚠️ Relevante
- 3 blocos com 2 repetições → 🔍 Aviso
- 3 blocos com 3+ repetições → ⚠️ Relevante
- 4+ blocos com 2+ repetições → ⚠️ Relevante
- Padrões só de tamanho 1 são ignorados

Exemplo:

	Tamanhos: [1, 2, 2, 1, 1, 2, 1, 1]
	→ [2,1,1] se repete 2x → 🔍 Aviso
- 
_**Função**_: `verify_excessive_run_frequency()`
Detecta se um tamanho específico ocorre em excesso, usando limites baseados em formulas.

**Regras**:
- Relevante se ultrapassa: max(40, 70 - 14 * log10(num_blocos))
- Aviso se ultrapassa: max(35, 60 - 14 * log10(num_blocos))
- Separado para blocos de 0 e de 1.

**Exemplo**:

	Blocos de '1': [1,1,1,1,111]
	→ 1 aparece 80% → ⚠️ Relevante
- 
_**Função**_: `verify_successively_same_size()`
Verifica blocos consecutivos com mesmo tamanho.

**Regras**:
- Até 3 blocos de tamanho 1–2 → 🔍 Aviso
- 3–4 blocos de tamanho >2 → ⚠️ Relevante
- 5+ blocos consecutivos (qualquer tamanho) → ⚠️ Relevante
- 2 blocos consecutivos de tamanho ≥ 4 → ⚠️ Relevante

**Exemplo**:

	Tamanhos: [2,2,2,2,2]
	→ 5 blocos de tamanho 2 → ⚠️ Relevante
- 
_**Função**_: `verify_mirror_pattern()`
Detecta padrões simétricos (espelhados) com base no centro da sequência.

**Regras**:
- Padrões de 5 blocos → 🔍 Aviso
- Padrões de 7+ blocos → ⚠️ Relevante
- Só analisa número ímpar de blocos

**Exemplo**:

	Blocos: [0,1,0,111,0,1,0]
	→ Padrão espelhado de 7 blocos → ⚠️ Relevante
- 
_**Função**_: `verify_match_between_zeros_and_ones()`
Compara padrões entre blocos de 0 e blocos de 1 em termos de padrão e proporção.

**Regras** (modo EXATO):
- Blocos exatamente iguais com mesma quantidade → ⚠️ Relevante
- Alternância perfeita > 5 blocos → ⚠️ Relevante
- 4+ blocos iguais → ⚠️ Relevante
- 3 blocos iguais com soma ≥ 8 → ⚠️ Relevante
- 3 blocos iguais com soma < 8 → 🔍 Aviso

**Regras** (modo RELATIVO):
- Qualquer padrão → 🔍 Aviso

**Exemplo**:

	Blocos 0: [3,1,1,3,1]
	Blocos 1: [1,1,3,1,1]
	→ Padrão [1,1,3,1] → ⚠️ Relevante

<br><br>

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

<br><br>

## Contribuição
Sinta-se à vontade para contribuir! Abra um pull request ou crie um issue para discutir melhorias.

<br><br>

## Licença
Este projeto está licenciado sob a MIT License. Veja LICENSE para mais detalhes.
