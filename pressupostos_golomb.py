"""
PRESSUPOSTO DE GOLOMB - Criptografia

Este programa realiza a análise de uma sequência binária para verificar se ela cumpre os três pressupostos de Golomb. 

:Sequence is valid:
    1. Proporção entre zeros e uns: A quantidade de zeros e uns na sequência deve estar dentro de uma margem aceitável, 
        com cada valor representando uma porcentagem mínima.
    2. Frequência de subsequências de diferentes tamanhos: Bloques de tamanho menor devem ser mais frequentes do 
        que blocos de tamanhos maiores.
    3. Distribuição equilibrada de padrões binários: A sequência não deve apresentar padrões indesejados, 
        como repetições ou espelhamentos de blocos.

:Inicial options:
1. **Analisar uma sequência existente**: O usuário insere uma sequência binária para ser analisada conforme os pressupostos de Golomb.
2. **Gerar uma nova sequência binária**: O usuário pode optar por criar uma sequência aleatória ou gerar uma sequência que atenda aos pressupostos de Golomb.

:Program Flow:
- Recebimento da sequência binária.
- Cálculo e verificação dos pressupostos de Golomb.
- Exibição de um relatório detalhado com o cumprimento de cada pressuposto e mensagens de alerta ou aviso, quando necessário.
- Opcionalmente, o programa pode gerar uma nova sequência que satisfaça os pressupostos selecionados.

Autor: Lucas Marques
Data: 25/04/2025
Versão: 1.0
"""

try:
    from colorama import init, Fore, Style, Back
    init(autoreset=True)
except ImportError:
    print("⚠️  Este script usa cores. Por favor, instale 'colorama' com 'py -m pip install colorama' no propt de comando")
    Fore = Style = type('', (), {'GREEN':'', 'RED':'', 'RESET_ALL':''})()

from math import log, log10
from re import findall
from collections import defaultdict
from random import randint

debug = False
def debug_print(message: str):
    if debug:
        print(message)


#BASES
def gettin_sequence_basics(sequence: str) -> tuple[dict, dict, dict, dict]:
    """
    Obtém as informações básicas de uma sequência binária.
    Retorna dados essenciais como número de bits, blocos contínuos, frequência dos blocos e a ordem dos tamanhos desses blocos.

    :Note:
    - A sequência já deve ter sido validada como binária antes de ser passada para esta função.
    - Os dados retornados são fundamentais para análise posterior dos pressupostos de Golomb.

    :param sequence: Sequência binária (apenas 0s e 1s)
    :type sequence: str
    :return: num_bits, runs, run_frequencies, ordered_run_sizes
    :rtype: dict, dict, dict, dict

    :Example:
    >>> gettin_sequence_basics("100101110010")
    (
        {'all': 12, 'zeros': 5, 'ones': 7},                           #num_bits
        {'all': ['1', '00', '1', ...], 'zeros': [...], 'ones': [...]},      #runs
        {'all': {1: 6, 2: 2, 3: 1}, 'zeros': {...}, 'ones': {...}},         #run_frequencies
        {'all': [1, 2, 1, 1, ...], 'zeros': [...], 'ones': [...]}           #ordered_run_sizes
    )
    """
    debug_print('\n📖 Obtendo as bases da sequencia')

    num_bits = count_bits(sequence)
    runs = separete_runs(sequence)
    run_frequencies = count_run_lengths(runs)
    ordered_run_sizes = run_sizes_in_order(runs)

    return [num_bits, runs, run_frequencies, ordered_run_sizes]
#
def count_bits(sequence: str) -> dict[str, int]:
    """
    Conta o número de bits em uma sequência binária.
    Retorna um dicionário com o total de bits, o número de zeros e o número de uns.

    :Note:
    - A sequência deve conter apenas caracteres '0' e '1'.
    - Outros caracteres serão ignorados e não contabilizados.

    :param sequence: Sequência binária como string (ex: '100101')
    :type sequence: str
    :return: Dicionário com contagem total, de zeros e de uns
    :rtype: dict

    :Example:
    >>> count_bits('100110101')
    {'all': 9, 'zeros': 4, 'ones': 5}
    """
    debug_print('\t1️⃣  Contando o número de bits')
    num_zeros = sequence.count('0')
    num_ones = sequence.count('1')
    return {'all': num_zeros+num_ones, 'zeros': num_zeros, 'ones': num_ones}
#
def separete_runs(sequence: str) -> dict[str, list[str]]:
    """
    Separa uma sequência binária em blocos consecutivos de zeros e uns, 
    retornando um dicionário com listas desses blocos.
    
    :Note:
    A função pressupõe que a sequência fornecida contenha apenas os caracteres '0' e '1'.
    Se forem incluídos outros caracteres, o comportamento pode ser imprevisível.

    :param sequence: string de sequência de bits
    :type sequence: str
    :return: dicionário com 3 listas — 'all': lista com todos os blocos; 
             'zeros': lista apenas com os blocos de zeros; 'ones': lista apenas com os blocos de uns
    :rtype: dict[str, list[str]]

    :Example:
    >>> runs = separete_runs('100110101')
    >>> runs['all']
    ['1', '00', '11', '0', '1', '0', '1']
    >>> runs['zeros']
    ['00', '0', '0']
    >>> runs['ones']
    ['1', '11', '1', '1']
    """
    debug_print('\t2️⃣  Separarando a sequência por blocos')
    runs = findall(r'0+|1+', sequence)
    runs_zero = []
    runs_one = []

    for run in runs:
        if run[0] == '0':
            runs_zero.append(run)
        if run[0] == '1':
            runs_one.append(run)

    return {
        "all": runs, 
        "zeros": runs_zero,
        "ones": runs_one
    }
#
def count_run_lengths(runs: dict) -> dict[dict[int, int]]:
    """
    Conta a frequência com que diferentes tamanhos de blocos ocorrem na sequência, separados por tipo (todos, apenas zeros, apenas uns).

    :Note:
    A função espera que `runs` seja um dicionário retornado pela função `separete_runs`, contendo listas de blocos.
    Não é necessário verificar a validade da sequência neste ponto, pois presume-se que isso já tenha sido feito anteriormente.

    :param runs: Dicionário com as listas de blocos separados da sequência, incluindo todos, zeros e uns.
    :type runs: dict[str, list[str]]
    :return: Dicionário com 3 subdicionários:
        - 'all': frequência de todos os blocos por tamanho
        - 'zeros': frequência dos blocos de zeros por tamanho
        - 'ones': frequência dos blocos de uns por tamanho
    :rtype: dict[str, dict[int, int]]

    :Example:
    >>> runs = {
    ...     'all': ['1', '00', '11', '0', '1', '0', '1'],
    ...     'zeros': ['00', '0', '0'],
    ...     'ones': ['1', '11', '1', '1']
    ... }
    >>> count_run_lengths(runs)
    {
        'all': {1: 5, 2: 2},
        'zeros': {1: 2, 2: 1},
        'ones': {1: 3, 2: 1}
    }

    >>> list(count_run_lengths(runs)['ones'].values())
    [3, 1]
    """
    debug_print('\t3️⃣  Calculando a frequencia de cada bloco')
    run_counts = defaultdict(int)
    run_counts_zero = defaultdict(int)
    run_counts_one = defaultdict(int)

    for run in runs['zeros']:
        run_counts[len(run)] += 1
        run_counts_zero[len(run)] += 1

    for run in runs['ones']:
        run_counts_one[len(run)] += 1
        run_counts[len(run)] += 1
        
    return {
        "all": dict(sorted(run_counts.items())),
        "zeros": dict(sorted(run_counts_zero.items())),
        "ones": dict(sorted(run_counts_one.items()))
    }
#
def run_sizes_in_order(runs: dict) -> dict[str, list[int]]:
    """
    Extrai os tamanhos dos blocos de uma sequência e os organiza na mesma ordem em que aparecem, separando por tipo (todos, zeros e uns).

    :Note:
    A função presume que a entrada foi gerada pela função `separete_runs`, portanto não realiza validações adicionais sobre o conteúdo.

    :param runs: Dicionário com listas de blocos separados da sequência, incluindo 'all', 'zeros' e 'ones'.
    :type runs: dict[str, list[str]]
    :return: Dicionário com listas de inteiros representando os tamanhos dos blocos na ordem da sequência:
        - 'all': tamanhos de todos os blocos
        - 'zeros': tamanhos dos blocos de zero
        - 'ones': tamanhos dos blocos de um
    :rtype: dict[str, list[int]]

    :Example:
    >>> runs = {
    ...     'all': ['1', '00', '11', '0', '1', '0', '1'],
    ...     'zeros': ['00', '0', '0'],
    ...     'ones': ['1', '11', '1', '1']
    ... }
    >>> run_sizes_in_order(runs)
    {
        'all': [1, 2, 2, 1, 1, 1, 1],
        'zeros': [2, 1, 1],
        'ones': [1, 2, 1, 1]
    }
    """
    debug_print('\t4️⃣  Colocando o tamanho dos blocos por ordem da sequencia')
    run_sizes = []
    run_sizes_zero = []
    run_sizes_one = []

    for run in runs['all']:
        run_sizes.append(len(run))
    for run in runs['zeros']:
        run_sizes_zero.append(len(run))
    for run in runs['ones']:
        run_sizes_one.append(len(run))

    return {
        'all': run_sizes,
        'zeros': run_sizes_zero,
        'ones': run_sizes_one
    }


#1 GOLOMB
def check_first_postulate(num_bits: dict, postulates: dict) -> list[dict, float, float, float]:
    """
    Verifica se a sequência cumpre o primeiro pressuposto de Golomb com base na percentagem de bits 0 e 1.

    :Note:
    Calcula a percentagem de 0's e 1's na sequência e compara com o mínimo aceitável (min_percentage).
    Se alguma percentagem for menor que o mínimo, o pressuposto é marcado como não cumprido e é adicionado um aviso relevante.
    O dicionário `postulates` é atualizado diretamente.

    :param num_bits: dicionário com número total de bits, e quantos são 0's e 1's
    :type num_bits: dict[str, int]
    :param postulates: dicionário que armazena o estado dos pressupostos
    :type postulates: dict[int, dict[str, Any]]

    :return: lista contendo o dicionário `postulates` atualizado, o valor mínimo de percentagem aceitável, a percentagem de 0's e de 1's
    :rtype: list[dict, float, float, float]

    :Example:
    >>> num_bits = {'all': 11, 'zeros': 6, 'ones': 5}
    >>> postulates = {1: {'comply': True, 'relevants': [], 'warnings': []}}
    >>> check_first_postulate(num_bits, postulates)
    [{1: {'comply': True, 'relevants': [], 'warnings': []}}, 43.47, 54.55, 45.45]
    """
    debug_print('\n🔍 Iniciando verificação de pressuposto 1')
    n_zeros = num_bits['zeros']
    n_ones = num_bits['ones']
    relevants = []
    comply = True
    length = n_zeros + n_ones
    percent_zero = round(n_zeros / length * 100, 2)
    percent_one = round(n_ones / length * 100, 2)

    min_percentage = get_min_percentage(length)
    debug_print(f'\tErro minimo calculado - {min_percentage}%')

    for percentage in [percent_zero, percent_one]:
        if percentage < min_percentage:
            comply = False
            relevants.append(f"~{percentage}% é menor que o mínimo permitido ~{min_percentage:.2f}%")

    if comply:
        debug_print('✅ Resultado, cumpre pressuposto 2')
    else:
        debug_print('❌ Resultado, não cumpre pressuposto 1')

    postulates[1]['comply'] = comply
    postulates[1]['relevants'] += relevants

    return [postulates, min_percentage , percent_zero, percent_one]
#
def get_min_percentage(length: int) -> float:
    """
    Retorna a percentagem mínima aceitável de bits 0 ou 1 numa sequência, com base no seu comprimento.

    :Note:
    A percentagem mínima cresce de forma ajustada ao tamanho da sequência:
    - ≤ 10 bits: 40%
    - Entre 10 e 20 bits: crescimento linear de 40% a 45%
    - Entre 21 e 1000 bits: fórmula logarítmica (natural) que garante equilíbrio crescente
    - > 1000 bits: 49%

    :param length: comprimento total da sequência
    :type length: int

    :return: percentagem mínima aceitável
    :rtype: float

    :Example:
    >> get_min_percentage(16)
    43.5

    >> get_min_percentage(25)
    45.3
    """
    debug_print('\tCalculando erro mínimo permitido')
    if length <= 10:
        return 40.00
    elif 10 < length <= 20:
        return round(0.5 * length + 35, 2)  # cresce de 40% a 45%
    elif 20 < length <= 1000:
        return round(41.6 + 1.15 * log(length), 2)  # log natural (ln)
    else:
        return 49.00


#2 GOLOMB
def check_second_postulate(run_frequencies: dict, postulates: dict) -> dict[list]:
    """
    Verifica se a sequência cumpre o segundo pressuposto de Golomb.
    O segundo pressuposto avalia a frequência dos blocos: blocos de tamanho menor devem ser mais frequentes 
    que blocos de tamanho maior.
    Esta função apenas coleta os dados resultantes (compliance, avisos relevantes e alertas secundários) e atualiza o 
    dicionário `postulates`.

    :Note:
    Esta função assume que `run_frequencies` foi gerado corretamente a partir de `count_run_lengths()`
    e que o dicionário `postulates` já contém a estrutura esperada para os pressupostos.

    :param run_frequencies: dicionário com contagem de blocos por tamanho (gerado por `count_run_lengths()`)
    :type run_frequencies: dict
    :param postulates: dicionário que armazena os resultados das verificações dos pressupostos
    :type postulates: dict

    :return: dicionário `postulates` atualizado com os resultados do segundo pressuposto
    :rtype: dict

    :Example:
    >>> run_frequencies = {
    ...     'all': {1: 5, 2: 5},
    ...     'zeros': {1: 2, 2: 3},
    ...     'ones': {1: 3, 2: 2}
    ... }
    >>> check_second_postulate(run_frequencies, postulates)
    {
        ...
        2: {
            'comply': True,
            'relevants': ['- Blocos de tamanho 1 (5) não são mais frequentes que de tamanho 2 (5)'],
            'warnings': []
        },
        ...
    }
    """
    debug_print('\n🔍 Iniciando verificação de pressuposto 2')
    run_counts = list(run_frequencies['all'].values())
    warnings = []

    comply, relevants, warnings = verify_frequency_runs(run_counts)

    postulates[2]['comply'] = comply
    postulates[2]['relevants'] += relevants
    postulates[2]['warnings'] += warnings

    return postulates
#
def verify_frequency_runs(run_counts: list) -> tuple[bool, list[str], list[str]]:
    """
    Verifica se os tamanhos menores de blocos são mais frequentes que os maiores,
    conforme definido pelo segundo pressuposto de Golomb.
    Essa verificação é feita comparando blocos consecutivos: um bloco de tamanho *n*
    deve ser mais frequente que um de tamanho *n+1*. Também emite avisos quando as
    frequências são muito próximas, mesmo que a ordem seja respeitada.

    :Note:
    A função assume que `run_counts` é uma lista de inteiros onde cada índice
    representa o tamanho do bloco (iniciando em 1) e o valor é sua frequência.

    :param run_counts: Lista de frequências de blocos por tamanho.
    :type run_counts: list[int]
    :return: Uma tupla contendo:
        - comply (bool): Indica se a sequência cumpre o segundo pressuposto.
        - relevants (list[str]): Avisos que invalidam o pressuposto.
        - warnings (list[str]): Alertas secundários (frequências muito próximas).
    :rtype: tuple[bool, list[str], list[str]]

    :Example:
    >>> run_counts = [5, 4, 2, 2]
    >>> comply, relevants, warnings = verify_frequency_runs(run_counts)
    >>> comply
    False
    >>> relevants
    ['Blocos de tamanho 3 (2) não são mais frequentes que de tamanho 4 (2)']
    >>> warnings
    ['Frequência de blocos tamanho 4 muito próxima de 5 (2 vs 2)']
    """
    debug_print('  🛠️  Verificando frequência de blocos')
    relevants = []
    warnings = []
    comply = True

    for size, (i1, i2) in enumerate(zip(run_counts, run_counts[1:])):
        if i1 <= i2:
            comply = False
            relevants.append(f"Blocos de tamanho {size+1} ({i1}) não são mais frequentes que de tamanho {size+2} ({i2})")
            debug_print(f'\t⚠️  Encontrado tamanhos superiores com maior frequência ({i1} < {i2})')
        elif i1 * 0.8 <= i2:
            warnings.append(f"Frequência de blocos tamanho {size+1} muito próxima de {size+2} ({i1} vs {i2})")
            debug_print(f'\t🧭 Encontrado frequências de blocos próximas ({i1} vs {i2})')

    if comply:
        if not warnings:
            debug_print('\t✔️  Nenhum padrão encontrado')
        debug_print('✅ Resultado, cumpre pressuposto 2')
    else:
        debug_print('❌ Resultado, não cumpre pressuposto 2')

    return [comply, relevants, warnings]


#3 GOLOMB
def check_third_postulate(run_frequencies: dict, ordered_run_sizes: dict, runs: dict, postulates: dict) -> dict[list]:
    """
    Verifica se a sequência cumpre o terceiro pressuposto de Golomb.
    Esse pressuposto avalia se a sequência apresenta padrões estruturais indesejados, como repetições,
    espelhamentos ou distribuições muito homogêneas nos blocos de 0s e 1s.

    A verificação é feita por meio de cinco funções auxiliares, cada uma responsável por identificar
    um tipo específico de padrão. Os resultados são reunidos e adicionados ao dicionário 'postulates'.

    :Note:
    Esta função assume que os dados fornecidos foram gerados pelas funções auxiliares apropriadas:
    'run_frequencies' (via 'count_run_lengths()'), 'ordered_run_sizes' (via 'run_sizes_in_order()'),
    'runs' (via 'separate_runs()'), e que o dicionário 'postulates' já contém a estrutura esperada.

    :param run_frequencies: Frequência de ocorrência de blocos por tamanho.
    :type run_frequencies: dict
    :param ordered_run_sizes: Tamanhos dos blocos na ordem da sequência.
    :type ordered_run_sizes: dict
    :param runs: Lista dos blocos de 0s e 1s encontrados na sequência.
    :type runs: dict
    :param postulates: Dicionário onde os resultados dos pressupostos são armazenados.
    :type postulates: dict
    :return: Dicionário `postulates` com os resultados do terceiro pressuposto atualizados.
    :rtype: dict[list]

    :Example:
    >>> sequencia = '00010010100000'
    >>> runs = {
    ...     'all': ['000', '1', '00', '1', '0', '1', '00000'],
    ...     'zeros': ['000', '00', '0', '00000'],
    ...     'ones': ['1', '1', '1']
    ... }
    >>> ordered_run_sizes = {
    ...     'all': [3, 1, 2, 1, 1, 1, 5],
    ...     'zeros': [3, 2, 1, 5],
    ...     'ones': [1, 1, 1]
    ... }
    >>> run_frequencies = {
    ...     'all': {1: 4, 2: 1, 3: 1, 5: 1},
    ...     'zeros': {1: 1, 2: 1, 3: 1, 5: 1},
    ...     'ones': {1: 3}
    ... }
    >>> postulates = {3: {'comply': None, 'relevants': [], 'warnings': []}}
    >>> postulates = check_third_postulate(run_frequencies, ordered_run_sizes, runs, postulates)
    >>> postulates[3]['comply']
    False
    >>> postulates[3]['relevants']
    ['Muitos blocos de [1] (~100.0%)']
    >>> postulates[3]['warnings']
    ['Tamanhos iguais consecutivos [1, 0, 1]', 'Três blocos de [1] consecutivos [1 - 1 - 1]']
    """
    debug_print('\n🔍 Iniciando verificação de pressuposto 3')
    comply = True
    relevants = []
    warnings = []

    comply1, relevants1, warnings1 = verify_sizes_patterns(runs, ordered_run_sizes)
    comply2, relevants2, warnings2 = verify_excessive_run_frequency(run_frequencies, ordered_run_sizes)
    comply3, relevants3, warnings3 = verify_successively_same_size(ordered_run_sizes, runs)
    comply4, relevants4, warnings4 = verify_mirror_pattern(runs)
    comply5, relevants5, warnings5 = verify_match_between_zeros_and_ones(ordered_run_sizes)

    comply = all([comply1, comply2, comply3, comply4, comply5])
    relevants.extend([*relevants1, *relevants2, *relevants3, *relevants4, *relevants5])
    warnings.extend([*warnings1, *warnings2, *warnings3, *warnings4, *warnings5])

    if comply:
        debug_print('✅ Resultado, cumpre o pressuposto 3')
    else:
        debug_print('❌ Resultado, não cumpre pressuposto 3')

    postulates[3]['comply'] = comply
    postulates[3]['relevants'] += relevants
    postulates[3]['warnings'] += warnings

    return postulates
#
def verify_sizes_patterns(runs: dict, ordered_run_sizes: dict) -> tuple[bool, list[str], list[str]]:
    """
    Verifica se há padrões repetitivos nos tamanhos dos blocos da sequência.
    Essa função identifica padrões estruturais baseados na repetição de blocos
    ou tamanhos de blocos consecutivos. Se detectados, esses padrões podem
    violar o terceiro pressuposto de Golomb.

    :Note:
    - Padrões de dois blocos repetidos sucessivamente são considerados RELEVANTES.
    - Grupos de três blocos:
        - Com 2 repetições → OPCIONAL.
        - Com 3+ repetições → RELEVANTE.
    - Grupos de quatro ou mais blocos com 2+ repetições → RELEVANTE.
    - Ignora padrões compostos apenas por blocos de tamanho 1.
    - Relevantes impactam diretamente na validação do pressuposto; warnings são alertas secundários.

    :param runs: Dicionário contendo os blocos separados da sequência.
    :type runs: dict
    :param ordered_run_sizes: Dicionário com os tamanhos dos blocos, na ordem original da sequência.
    :type ordered_run_sizes: dict
    :return: Tupla contendo:
             - `comply`: booleano indicando se não foram encontrados padrões relevantes,
             - `relevants`: lista de mensagens de padrões que violam o pressuposto,
             - `warnings`: lista de mensagens de padrões não críticos mas suspeitos.
    :rtype: tuple[bool, list[str], list[str]]

    :Example:
    >>> sequencia = '1001101001010'
    >>> runs = {'all': ['1', '00', '11', '0', '1', '00', '1', '0', '1', '0'], ...}
    >>> ordered_run_sizes = {'all': [1, 2, 2, 1, 1, 2, 1, 1, 1, 1], ...}
    >>> comply, relevants, warnings = verify_sizes_patterns(runs, ordered_run_sizes)
    >>> comply
    False
    >>> relevants
    ['Bloco [1 0] repete-se sucessivamente']
    >>> warnings
    ['Tamanhos de blocos [2, 1, 1] repete-se 2 vezes.']
    """
    debug_print('  🛠️  Verificando padrões nos tamanhos de blocos')
    comply = True
    relevants = []
    warnings = []
    count_groups = {}
    len_runs_sizes = len(runs['all'])

    for size_groups_run in range(2, len_runs_sizes):

        if size_groups_run == 2:
            for start in range(len_runs_sizes-3):
                end = start +2
                try:
                    group = ' '.join(runs['all'][start : end])
                    next_group = ' '.join(runs['all'][start +2 : end +2])

                    if len(group) == 2:
                        continue
                    if group == next_group:
                        comply = False
                        relevants.append(f'Bloco [{group}] repete-se sucessivamente')
                        debug_print(f'\t⚠️  Bloco [{group}] repete-se sucessivamente')

                except IndexError:
                    break
      
        if size_groups_run > 2:
            groups_to_scan = len_runs_sizes - size_groups_run +1

            for index_group in range(groups_to_scan):
                start_group = index_group
                end_group = start_group + size_groups_run
                group = ordered_run_sizes['all'][start_group : end_group]
                group_str = ', '.join(str(run) for run in group)
                
                if group_str in count_groups.keys():
                    count_groups[group_str] += 1
                else:
                    count_groups[group_str] = 1


    for group, qtt in count_groups.items():
        sizes_in_group = group.split(', ')
        runs_in_group = len(sizes_in_group)
        sum_group_sizes = sum([int(size) for size in sizes_in_group])

        if sum_group_sizes > runs_in_group:
            if qtt > 2:
                comply = False
                relevants.append(f"Tamanhos de blocos [{group}] repete-se {qtt} vezes.")
                debug_print(f'\t⚠️  Tamanho de blocos [{group}] repetem-se em excesso')
            elif qtt == 2:
                if runs_in_group == 3:
                    warnings.append(f"Tamanhos de blocos [{group}] repete-se {qtt} vezes.")
                    debug_print(f'\t🧭 Tamanho de blocos [{group}] repetem-se com frequência')
                else:
                    comply = False
                    relevants.append(f"Tamanhos de blocos [{group}] repete-se {qtt} vezes.")
                    debug_print(f'\t⚠️  Tamanho de blocos [{group}] repetem-se em excesso')


    if not (warnings or relevants):
        debug_print('\t✔️  Nenhum padrão encontrado')

    return [comply, relevants, warnings]
#
def verify_excessive_run_frequency(run_frequencies: dict, ordered_run_sizes: dict) -> tuple[bool, list[str], list[str]]:
    """
    Verifica se algum tamanho específico de bloco de 0s ou 1s aparece em excesso na sequência.
    Usa limites baseados em logaritmo para detectar repetições excessivas que violariam o terceiro pressuposto de Golomb.

    :Note:
    - Um tamanho de bloco é considerado RELEVANTE se aparecer acima de `max_percentage`:
        max(40, 70 - 14 * log10(num_blocks))
    - É considerado um alerta OPCIONAL se ultrapassar `warning_percentage`:
        max(35, 60 - 14 * log10(num_blocks))
    - A verificação é feita separadamente para blocos de zeros e de uns.
    - O cálculo considera a frequência de cada tamanho de bloco em relação ao total de blocos do mesmo tipo.

    :param run_frequencies: Dicionário com a quantidade de vezes que blocos de cada tamanho aparecem, separados por tipo ('zeros' ou 'ones').
    :type run_frequencies: dict
    :param ordered_run_sizes: Dicionário com os tamanhos dos blocos, organizados por tipo ('zeros' ou 'ones').
    :type ordered_run_sizes: dict
    :return: Tupla contendo:
             - 'comply': booleano indicando se não há blocos em excesso,
             - 'relevants': lista de mensagens com padrões que violam o pressuposto,
             - 'warnings': lista de alertas secundários com padrões que ocorrem com frequência.
    :rtype: tuple[bool, list[str], list[str]]

    :Example:
    >>> sequencia = '10001110100101'
    >>> run_frequencies = {..., 'zeros': {1: 2, 2: 1, 3: 1}, 'ones': {1: 4, 3: 1}}
    >>> ordered_run_sizes = {..., 'zeros': [3, 1, 2, 1], 'ones': [1, 3, 1, 1, 1]}
    >>> comply, relevants, warnings = verify_excessive_run_frequency(run_frequencies, ordered_run_sizes)
    >>> comply
    False
    >>> relevants
    ['Muitos blocos de [1] (~80.0%)']
    >>> warnings
    []
    """
    debug_print('  🛠️  Verificando blocos em excesso')
    relevants = []
    warnings = []
    comply = True

    for bit_type in ['zeros', 'ones']:
        run_counts_dict = run_frequencies[bit_type]
        total_runs = sum(run_counts_dict.values())

        num_blocks = len(ordered_run_sizes[bit_type])
        if num_blocks == 0: num_bits = 1
        bit = '0' if bit_type == 'zeros' else '1'

        max_percentage = max(40, 70 - 14 * log10(num_blocks))
        warning_percentage = max(35, 60 - 14 * log10(num_blocks))

        for size, count in run_counts_dict.items():
            percentage = count / total_runs * 100
            if percentage > max_percentage:
                block = bit * size
                debug_print(f'\t⚠️  Excesso de blocos de [{block}] (~{percentage:.1f}%)')
                comply = False
                relevants.append(f"Muitos blocos de [{block}] (~{percentage:.1f}%)")

            elif percentage >= warning_percentage:
                block = bit * size
                debug_print(f'\t🧭  Frequente de blocos de [{block}] (~{percentage:.1f}%)')
                warnings.append(f"Talvez muitos blocos de [{block}] (~{percentage:.1f}%)?")
    
    if not (warnings or relevants):
        debug_print('\t✔️  Nenhum padrão encontrado')

    return comply, relevants, warnings
#
def verify_successively_same_size(ordered_run_sizes: dict, runs: dict) -> tuple[bool, list[str], list[str]]:
    """
    Verifica se há blocos consecutivos com o mesmo tamanho, o que pode indicar repetição artificial e violar o terceiro pressuposto de Golomb.
    A análise é feita separadamente para todos os blocos, blocos de zeros e blocos de uns.

    :Note:
    - Regras aplicadas:
        - Até 3 blocos consecutivos de tamanho 1–2 → IRRELEVANTE
        - 3 ou 4 blocos consecutivos:
            - tamanho 1–2 → OPCIONAL
            - tamanho >2 → RELEVANTE
        - 5 ou mais blocos consecutivos (qualquer tamanho) → RELEVANTE
        - 2 blocos consecutivos com tamanho ≥ 4 → RELEVANTE

    :param ordered_run_sizes: Dicionário com listas ordenadas de tamanhos de blocos por tipo: 'all', 'zeros', 'ones'.
    :type ordered_run_sizes: dict
    :param runs: Dicionário com os blocos separados em listas por tipo: 'all', 'zeros', 'ones'.
    :type runs: dict
    :return: Tupla contendo:
             - 'comply': booleano indicando se a sequência cumpre as regras,
             - 'relevants': lista de mensagens com violações relevantes,
             - 'warnings': lista de alertas opcionais de possíveis padrões suspeitos.
    :rtype: tuple[bool, list[str], list[str]]

    :Example:
    >>> sequencia = '0101111101010111'
    >>> ordered_run_sizes = {
    ...     'all': [1, 1, 1, 5, 1, 1, 1, 1, 1, 3],
    ...     'zeros': [1, 1, 1, 1, 1],
    ...     'ones': [1, 5, 1, 1, 3]
    ... }
    >>> runs = {
    ...     'all': ['0', '1', '0', '11111', '0', '1', '0', '1', '0', '111'],
    ...     'zeros': ['0', '0', '0', '0', '0'],
    ...     'ones': ['1', '11111', '1', '1', '111']
    ... }
    >>> comply, relevants, warnings = verify_successively_same_size(ordered_run_sizes, runs)
    >>> comply
    False
    >>> relevants
    ['Tamanhos iguais consecutivos [0, 1, 0, 1, 0]', 'Três blocos de [0] consecutivos [0 - 0 - 0]']
    >>> warnings
    ['Tamanhos iguais consecutivos [0, 1, 0]']
    """
    debug_print('  🛠️  Verificando tamanho de blocos iguais sucessivos')
    comply = True
    warnings = {}
    relevants = {}

    def warning_result(bit, run_sizes, index, count, level):
        sign2 = '⚠️' if level == 1 else '🧭'
        if bit == 'all':
            content = ', '.join(runs['all'][index:index+count])
            debug_print(f'\t{sign2}  Tamanhos iguais consecutivos [{content}]')
            return f"Tamanhos iguais consecutivos [{content}]"
        else:
            block = bit * run_sizes[index]
            debug_print(f'\t{sign2}  Blocos de [{block}] consecutivos')
            return f"{count} blocos consecutivos com o mesmo tamanho [{block}] [{' - '.join([block]*count)}]"

    for bit_type in ['all', 'zeros', 'ones']:
        run_sizes = ordered_run_sizes[bit_type]
        bit = '0' if bit_type == 'zeros' else '1' if bit_type == 'ones' else 'all'

        i = 0
        while i < len(run_sizes):
            count = 1
            while i + count < len(run_sizes) and run_sizes[i] == run_sizes[i + count]:
                count += 1

            if count >= 5:
                comply = False
                relevants[f"{bit_type}{i}"] = warning_result(bit, run_sizes, i, count, 1)
            elif count in [3, 4]:
                if run_sizes[i] > 2:
                    comply = False
                    relevants[f"{bit_type}{i}"] = warning_result(bit, run_sizes, i, count, 1)
                else:
                    warnings[f"{bit_type}{i}"] = warning_result(bit, run_sizes, i, count, 0)
            elif count == 2:
                if run_sizes[i] >= 4:
                    comply = False
                    relevants[f"{bit_type}{i}"] = warning_result(bit, run_sizes, i, count, 1)

            i += count
    
    if not(warnings or relevants):
        debug_print('\t✔️  Nenhum padrão encontrado')

    return [comply, list(relevants.values()), list(warnings.values())]
#
def verify_mirror_pattern(runs: dict) -> tuple[bool, list[str], list[str]]:
    """
    Verifica a existência de padrões simétricos (em espelho) dentro da sequência de blocos.

    A função busca padrões onde os blocos à esquerda e à direita de um ponto central são espelhados.
    Padrões simétricos de 5 blocos são considerados avisos opcionais. Padrões de 7 ou mais blocos
    violam o terceiro pressuposto e são considerados relevantes.

    :Note:
    Só avalia padrões com número ímpar de blocos (3, 5, 7, ...) e exige pelo menos simetria visual
    ao redor de um bloco central.

    :param runs: dicionário contendo os blocos da sequência já separados por tipo.
    :type runs: dict

    :return:
        - 'comply': booleano indicando se a sequência cumpre as regras de simetria,
        - 'relevants': lista de mensagens com violações relevantes (padrões espelhados grandes),
        - 'warnings': lista de alertas opcionais (padrões espelhados pequenos).
    :rtype: tuple[bool, list[str], list[str]]

    :Example:
    >>> runs = {'all': ['0', '1', '0', '11111', '0', '1', '0', '1', '0', '111']}
    >>> comply4, relevants4, warnings4 = verify_mirror_pattern(runs)
    >>> comply4
    False
    >>> relevants4
    ['Padrão espelhado [0 1 0 11111 0 1 0]']
    >>> warnings4
    ['Talvez um padrão espelhado? [1 0 11111 0 1]',
     'Talvez um padrão espelhado? [0 1 0 1 0]']
    """
    debug_print('  🛠️  Verificando padrões em espelho')
    len_runs_sizes = len(runs['all'])
    max_len_groups_run = int(len_runs_sizes/2)
    comply = True
    warnings = {}
    relevants = {}

    for size_groups_run in range(3, max_len_groups_run +1):

        for center_scan in range(size_groups_run -1, len_runs_sizes - size_groups_run +1):

            start = center_scan - size_groups_run +1
            end = center_scan + size_groups_run -1

            group = ' '.join(runs['all'][start : center_scan+1])
            next_mirror_group = ' '.join(reversed(runs['all'][center_scan: end+1]))

            if group == next_mirror_group:
                if size_groups_run == 3:
                    debug_print(f'\t🧭 Padrão espelhado fraco {runs['all'][start : end+1]}')
                    warnings[center_scan] = (f"Talvez um padrão espelhado? [{' '.join(runs['all'][start : end+1])}]")
                else:
                    debug_print(f'\t⚠️ Padrão espelhado forte {runs['all'][start : end+1]}')
                    comply = False
                    relevants[center_scan] = (f"Padrão espelhado [{' '.join(runs['all'][start : end+1])}]")

    if not(warnings or relevants):
        debug_print('\t✔️  Nenhum padrão encontrado')
                
    return [comply, list(relevants.values()), list(warnings.values())]
#
def verify_match_between_zeros_and_ones(ordered_run_sizes: dict) -> tuple[bool, list[str], list[str]]:
    """
    Verifica se existem padrões semelhantes entre blocos de zeros e uns.

    A função compara blocos consecutivos de tamanhos em 'zeros' e 'ones', tanto de forma exata
    quanto relativa, procurando padrões que possam violar o 3º pressuposto de Golomb.

    :Note:
    Pode gerar:
    - Violações relevantes (modo EXATO):
        • Blocos exatamente iguais com mesma quantidade.
        • Alternância perfeita com mais de 5 blocos.
        • 3 blocos iguais com soma ≥ 8.
        • 4 ou mais blocos iguais.
    - Avisos secundários:
        • 3 blocos iguais com soma < 8.
        • Qualquer padrão no modo RELATIVO (inclusive alternância perfeita com +5 blocos).

    :param ordered_run_sizes: Dicionário com listas ordenadas dos tamanhos dos blocos 'zeros' e 'ones'.
    :type ordered_run_sizes: dict

    :return:
        - 'comply': indica se a sequência está de acordo com o 3º pressuposto,
        - 'relevants': mensagens de padrões que violam o pressuposto,
        - 'warnings': mensagens de padrões suspeitos, mas não críticos.
    :rtype: tuple[bool, list[str], list[str]]

    :Example:
    >>> ordered_run_sizes = {
    ...     'zeros': [3, 1, 1, 3, 1, 1],
    ...     'ones' : [1, 1, 3, 1, 1, 1, 1]
    ... }
    >>> comply5, relevants5, warnings5 = verify_match_between_zeros_and_ones(ordered_run_sizes)
    >>> comply5
    False
    >>> relevants5
    ["Blocos de tamanhos [1|1|3|1|1] aparecem 1 vezes em blocos de '1' e '0'"]
    >>> warnings5
    []
    """
    debug_print('  🛠️  Verificando coerências entre zeros e uns')
    relative_sizes: dict[list, list] = classify_run_relative(ordered_run_sizes)
    relevants = []
    warnings = []
    comply = True
    len_zeros = len(ordered_run_sizes['zeros'])
    len_ones = len(ordered_run_sizes['ones'])
    count_groups = {'exact': {}, 'relative': {}}

    def is_subpattern_of_existing(group_0_str, count_groups, relation) -> dict:
        for group_str in count_groups[relation].keys():
            if group_0_str in group_str:
                if group_0_str == group_str:
                    count_groups[relation][group_str] += 1
                break
        else:
            count_groups[relation][group_0_str] = 1
        return count_groups

    def warnings_message(debug_label, target_list, which_message, relation, group):
        if relation == 'exact':
            relat = ''
        else:
            relat = 'relativos '

        if which_message == 1:
            target_list.append(f"Blocos de tamanhos {relat}[{group}] aparecem {qtt} vezes em blocos de '1' e '0'")
            debug_print(f"{debug_label}Blocos de tamanhos {relat}[{group}] em excesso em blocos de '1' e '0'")
        elif which_message == 2:
            target_list.append(f"Blocos {relat}de 0 e 1, totalmente iguais")
            debug_print(f"{debug_label}Blocos {relat}de 0 e 1, totalmente iguais")
        elif which_message == 3:
            target_list.append(f"Blocos {relat}de 0 e 1, com padrões alternados repetivivos")
            debug_print(f"{debug_label}Blocos {relat}de 0 e 1, com padrões alternados repetivivos")

        return target_list


    for process_type in [ordered_run_sizes, relative_sizes]:
        relation = 'exact' if process_type == ordered_run_sizes else 'relative'

        for size_groups_run in range(len_zeros, 2, -1):
            groups_to_scan_0 = len_zeros - size_groups_run +1
            groups_to_scan_1 = len_ones - size_groups_run +1

            for index_zero in range(groups_to_scan_0):
                group_0 = process_type['zeros'][index_zero : index_zero + size_groups_run]
                group_0_str = '|'.join(str(run) for run in group_0)

                for index_one in range(groups_to_scan_1):
                    group_1 = process_type['ones'][index_one : index_one + size_groups_run]
                    group_1_str = '|'.join(str(run) for run in group_1)
                    
                    if group_0_str == group_1_str:
                        count_groups = is_subpattern_of_existing(group_0_str, count_groups, relation)
                        
        for group, qtt in count_groups[relation].items():
            sizes = group.split('|')
            runs = len(sizes)
            min_len = min(len_zeros, len_ones)
            is_alternating = all(sizes[0] == size for size in sizes)

            debug_label = '\t⚠️  ' if relation == 'exact' else '\t🧭 '
            target_list = relevants if relation == 'exact' else warnings

            # Regra 1: padrões totalmente iguais
            if runs >= min_len:
                target_list = warnings_message(debug_label, target_list, 2, relation, group)

            # Regra 2: padrões alternados longos
            elif is_alternating and runs >= 5:
                target_list = warnings_message(debug_label, target_list, 3, relation, group)

            # Regras específicas para modo exact
            elif relation == 'exact':
                total = sum(int(size) for size in sizes)
                if runs >= 4:
                    relevants = warnings_message('\t⚠️  ', relevants, 1, relation, group)
                elif runs == 3:
                    if total >= 8:
                        relevants = warnings_message('\t⚠️  ', relevants, 1, relation, group)
                    else:
                        warnings = warnings_message('\t🧭 ', warnings, 1, relation, group)

            # Regras específicas para modo relative
            else:
                warnings = warnings_message('\t🧭 ', warnings, 1, relation, group)

    if not (warnings + relevants):
        debug_print('\t✔️  Nenhum encontrado')
    if relevants:
        comply = False
    return [comply, relevants, warnings]
#
def classify_run_relative(ordered_run_sizes: dict) -> dict:
    """
    Classifica os tamanhos dos blocos de zeros e uns em categorias relativas (small → large).

    Cria uma régua baseada nos quartis dos tamanhos totais da sequência e aplica essa escala
    para categorizar cada bloco como 'small', 'mid_small', 'mid_large' ou 'large', mantendo a ordem original.

    :Note:
    Deve ser usada como suporte para análise relativa de padrões em verify_match_between_zeros_and_ones().

    :param ordered_run_sizes: Dicionário com listas ordenadas dos tamanhos dos blocos, incluindo 'zeros', 'ones' e 'all'.
    :type ordered_run_sizes: dict

    :return: Dicionário com os mesmos campos ('zeros', 'ones'), mas com os tamanhos classificados em categorias relativas.
    :rtype: dict

    :raises KeyError: Se a chave 'all' estiver ausente no dicionário de entrada.
    :raises ValueError: Se a lista associada à chave 'all' estiver vazia.

    :Example:
    >>> ordered_run_sizes = {
    ...     'zeros': [1, 2, 3, 3],
    ...     'ones' : [1, 2, 3, 4],
    ...     'all'  : [1, 2, 3, 3, 1, 2, 3, 4]
    ... }
    >>> classify_run_relative(ordered_run_sizes)
    {
        'zeros': ['small', 'mid_small', 'mid_large', 'mid_large'],
        'ones' : ['small', 'mid_small', 'mid_large', 'large']
    }
    """
    sorted_all = sorted(ordered_run_sizes['all'])
    min_val = sorted_all[0]
    max_val = sorted_all[-1]
    margin = max_val - min_val

    if margin == 0:
        q1 = q2 = q3 = min_val
    else:
        q1 = min_val + margin * 0.25
        q2 = min_val + margin * 0.50
        q3 = min_val + margin * 0.75
    
    relative_size = {'zeros': [], 'ones': []}

    for bit_type in ['zeros', 'ones']:
        for run in ordered_run_sizes[bit_type]:
            if run <= q1:
                relative_size[bit_type].append('small')
            elif run <= q2:
                relative_size[bit_type].append('mid_small')
            elif run <= q3:
                relative_size[bit_type].append('mid_large')
            else:
                relative_size[bit_type].append('large')

    return relative_size


#INPUT & OUTPUT
def verify_sequence(sequence: str) -> bool:
    """
    Verifica se a sequência fornecida é binária (apenas 0s e 1s).
    Retorna True se válida, ou False caso contenha qualquer caractere diferente de 0 ou 1.

    :Note:
    - Espaços, letras ou outros símbolos além de '0' e '1' tornam a sequência inválida.
    - A função espera que o argumento seja do tipo string.

    :param sequence: Sequência a ser verificada
    :type sequence: str
    :return: True se a sequência for binária, False caso contrário
    :rtype: bool

    :Example:
    >>> verify_sequence("10010111001")
    True

    >>> verify_sequence("1001 0111")
    False

    >>> verify_sequence("ola mundo")
    False
    """
    debug_print('\n🔍 Vericando se sequencia é binária')
    try:
        int(sequence) #ValueError
        for bit in sequence:
            if bit not in '01': #ValueError
                raise ValueError
        debug_print('✅ Sequencia válida')
        return True
                    
    except ValueError:
        debug_print('❌ Sequência inválido')
        return False
#
def create_random_sequence(length: int) -> str:
    """
    Gera uma sequência binária aleatória com o comprimento definido.

    :Note:
    - Cada bit é gerado de forma independente, com valores 0 ou 1 escolhidos aleatoriamente.
    - Assume que o parâmetro `length` já foi validado previamente.

    :param length: Número total de bits a serem gerados na sequência.
    :type length: int

    :return: Sequência binária gerada aleatoriamente.
    :rtype: str

    :Example:
    >>> length = 23
    >>> create_random_sequence(length)
    '01100001000001111100100'
    """
    debug_print('\n🔄️ Gerando sequência aleatoria')
    sequence = ''
    for bit in range(length):
        sequence += str(randint(0,1))
    debug_print('📁 Sequencia completa')
    return sequence
#
def create_postulates_sequence(postulate_to_match: list, postulates: dict, length: int) -> str:
    """
    Cria uma sequência binária que cumpre os pressupostos de Golomb selecionados.

    :Note:
    - Tenta gerar até 5000 sequências aleatórias até encontrar uma que atenda aos pressupostos marcados.
    - Se nenhuma sequência válida for encontrada dentro do limite, uma exceção é lançada.
    - Cada tentativa envolve gerar uma sequência aleatória, extrair suas características e aplicar os testes de conformidade.

    :param postulate_to_match: Lista com 3 valores representando os pressupostos a cumprir ('' ou 'x').
    :type postulate_to_match: list
    :param postulates: Dicionário contendo os estados de conformidade de cada pressuposto.
    :type postulates: dict
    :param length: Comprimento da sequência binária a ser gerada.
    :type length: int

    :return: Sequência binária que cumpre os pressupostos especificados.
    :rtype: str

    :raise Exception: Se após 5000 tentativas nenhuma sequência cumprir todos os pressupostos indicados.

    :Example:
    >>> postulates_to_match = ['x', '', 'x']
    >>> length = 14
    >>> postulates = {
    ...     1: {'comply': True, 'relevants': [], 'warnings': []},
    ...     2: {'comply': True, 'relevants': [], 'warnings': []},
    ...     3: {'comply': True, 'relevants': [], 'warnings': []}
    ... }
    >>> create_postulates_sequence(postulates_to_match, postulates, length)
    '11100000011001'
    """
    p1, p2, p3 = postulate_to_match
    debug_print('\n🔄️ Gerando sequencia que cumpra os pressupostos selecionados')
    attemps = 0
    max_attemps = 5000
    while attemps <= max_attemps:
        attemps += 1
        random_seq = create_random_sequence(length)

        #Analise sequence
        num_bits, runs, run_frequencies, ordered_run_sizes = gettin_sequence_basics(random_seq)

        #Analise sequence by golomb
        if p1 != '':
            postulates, _, _, _ = check_first_postulate(num_bits, postulates)
            if not postulates[1]['comply']:
                continue
        if p2 != '':
            postulates = check_second_postulate(run_frequencies, postulates)
            if not (postulates[2]['comply'] or postulates[2]['relevants']):
                continue
        if p3 != '':
            postulates = check_third_postulate(run_frequencies, ordered_run_sizes, runs, postulates)
            if not (postulates[3]['comply'] or postulates[3]['relevants']):
                continue
        if postulates[1]['comply'] and postulates[2]['comply'] and postulates[3]['comply']:
                break
    else:
        debug_print('\n❗ Excesso de tentativas')
        raise Exception("🚨 Não foi possível gerar uma sequência válida que cumpra os pressupostos selecionados. 5000 tentativas.")
    debug_print('\n📦 Sequencia completa')
    return random_seq
#
def print_final_output(sequence, num_bits, percent_zeros, percent_ones, min_percentage, runs, run_frequencies, 
                       ordered_run_sizes, postulates) -> None:
    """
    Exibe os resultados finais da análise de uma sequência binária, de forma visualmente clara e organizada.

    :Note:
    Esta função **não realiza cálculos**, apenas imprime os dados finais da análise.
    Ela mostra se os três pressupostos de Golomb foram cumpridos, destaca os problemas relevantes que impediram a conformidade
    e também apresenta alertas secundários (warnings) que podem indicar padrões suspeitos.

    :param sequence: Sequência binária original analisada.
    :type sequence: str

    :param num_bits: Dicionário com contagens de bits {'all': int, 'zeros': int, 'ones': int}.
    :type num_bits: dict

    :param percent_zeros: Percentagem de zeros na sequência.
    :type percent_zeros: float

    :param percent_ones: Percentagem de uns na sequência.
    :type percent_ones: float

    :param min_percentage: Percentagem mínima exigida de 0's ou 1's para cumprir o Pressuposto 1.
    :type min_percentage: float

    :param runs: Dicionário com listas de blocos da sequência (todos, apenas 0's, apenas 1's).
    :type runs: dict

    :param run_frequencies: Frequência de blocos por tamanho. Ex: {1: 5, 2: 4, 3: 1}.
    :type run_frequencies: dict

    :param ordered_run_sizes: Dicionário com os tamanhos dos blocos, ordenados por tipo ('zeros', 'ones').
    :type ordered_run_sizes: dict

    :param postulates: Dicionário com os resultados de conformidade e mensagens por Pressuposto.
    :type postulates: dict

    :return: Nenhum valor é retornado. A função apenas imprime os resultados.
    :rtype: None

    :raises: Esta função não lança exceções, desde que os dados recebidos estejam corretamente estruturados.

    :Example:

    >>> print_final_output(
    ...     sequence='0100111100100101100',
    ...     num_bits={'all': 19, 'zeros': 10, 'ones': 9},
    ...     percent_zeros=52.63,
    ...     percent_ones=47.37,
    ...     min_percentage=44.50,
    ...     runs={'all': ['0', '1', '00', '1111', '00', '1', '00', '1', '0', '11', '00'],
    ...           'zeros': ['0', '00', '00', '00', '0', '00'],
    ...           'ones': ['1', '1111', '1', '1', '11']},
    ...     run_frequencies={'all': {1: 5, 2: 5, 4: 1}},
    ...     ordered_run_sizes={'zeros': [1, 2, 2, 2, 1, 2], 'ones': [1, 4, 1, 1, 2]},
    ...     postulates={
    ...         1: {'comply': True, 'relevants': [], 'warnings': []},
    ...         2: {'comply': False, 'relevants': ['Blocos de tamanho 1 (5) não são mais frequentes que de tamanho 2 (5)'], 'warnings': []},
    ...         3: {'comply': False, 'relevants': ['Bloco [00 1] repete-se sucessivamente'], 'warnings': ['Tamanhos de blocos [1, 1, 2] repete-se 2 vezes.']}
    ...     }
    ... )"""
    # Exibe os resultados da análise em blocos visuais formatados.
    debug_print('\n📝 Exibindo resultado')
    separator = '-' * 50
    len_sep = 50
    bright_blue = Fore.BLUE + Style.BRIGHT
    dim = Style.DIM
    brigth = Style.BRIGHT
    red = Fore.RED
    green = Fore.GREEN
    yellow = Fore.YELLOW

    print("\n\n\n" + separator)
    print(bright_blue + "📊 RESULTADO FINAL DA ANÁLISE".center(len_sep))
    print(separator)
    print(f"\tSequencia:      \t{sequence}")
    print(f"\tTotal de bits:  \t{num_bits['all']}")
    print(f"\tNumero de 0's:  \t{num_bits['zeros']}")
    print(f"\tNumero de 1's:  \t{num_bits['ones']}")


    print("\n\n\n" + separator)
    print(bright_blue + "☯️  PRESSUPOSTO 1 - Proporção de bits".center(len_sep))
    print(separator)
    print("   - percentagem de 0's e 1's tem de ser o mais próximo possível de 50%.")
    print(f"\n\tPercentagem de 0's      \t{percent_zeros:.2f}%")
    print(f"\tPercentagem de 1's      \t{percent_ones:.2f}%")
    print(f"\tErro mínimo permitido   \t{min_percentage:.2f}%")
    if postulates[1]['comply']:
        p1 = f'✅ {green}{postulates[1]['comply']}'
    else:
        p1 = f'❌ {red}{postulates[1]['comply']}'
    print(brigth + f"\nCUMPRE PRESSUPOSTO 1? {p1}")
    print(dim + "Nota: Erro mínimo permitido: minimo de percentagem de 0's ou 1's para que o pressuposto seja verdadeiro.\n" +
          "Varia entre 40% a 49%, dependendo do comprimento da sequencia. Calculado em get_min_percentage()")


    print("\n\n\n" + separator)
    print(bright_blue + "🔗 PRESSUPOSTO 2 - Comprimento de Runs".center(len_sep))
    print(separator)
    print("   - blocos menores têm de ser bem mais frequentes que blocos maiores")
    print(f"\n\tBlocos           \t{' '.join(runs['all'])}")
    print(f"\tTamanho de blocos  \t{list(run_frequencies['all'].items())}")
    if postulates[2]['comply']:
        p2 = f'✅ {green}{postulates[2]['comply']}'
    else:
        p2 = f'❌ {red}{postulates[2]['comply']}'
    print(brigth + f"\nCUMPRE PRESSUPOSTO 2? {p2}")
    print(dim + "Nota: 'Tamanho de blocos: quantidade de vezes que blocos de tamanho 1, 2, 3, 4... aparecem na sequencia'")


    print("\n\n\n" + separator)
    print(bright_blue + "🧩 PRESSUPOSTO 3 - Autocorreção".center(len_sep))
    print(separator)
    print("   - sequencia não deve apresentar padrões estruturais")
    print(f"\n\tBlocos          \t{' '.join(runs['all'])}")
    print(f"\tBlocos de 0's   \t[{' '.join(runs['zeros'])}]")
    print(f"\tTamanho Blc 0's \t{ordered_run_sizes['zeros']}")
    print(f"\tBlocos de 1's   \t[{' '.join(runs['ones'])}]")
    print(f"\tTamanho Blc 1's \t{ordered_run_sizes['ones']}")    
    if postulates[3]['comply']:
        p3 = f'✅ {green}{postulates[3]['comply']}'
    else:
        p3 = f'❌ {red}{postulates[3]['comply']}'
    print(brigth + f"\nCUMPRE PRESSUPOSTO 3? {p3}")
    

    print("\n\n\n" + separator)
    print(bright_blue + "⚖️  ANÁLISE FINAL DOS PRESSUPOSTOS DE GOLOMB".center(len_sep))
    print(separator)
#
    if not postulates[1]['comply']:
        print(f"\n{red}❌ Problemas RELEVANTES encontrados no PRESSUPOSTO 1")
        print(f"{yellow}  ⚠️  Relevants:")
        for relevant in postulates[1]["relevants"]:
            print('\t- ' + relevant)
    else:
        print(f"\n{green}📌 PRESSUPOSTO 1 - Proporção de bits: {p1}")
        print('  🎉 Nenhum problema encontrado')
#
    if not postulates[2]['comply']:
        print(f"\n{red}❌ Problemas RELEVANTES encontrados no PRESSUPOSTO 2")
        print(f"{yellow}  ⚠️  Relevants:")
        for relevant in postulates[2]["relevants"]:
            print('\t- ' + relevant)
    else:
        print(f"\n{green}📌 PRESSUPOSTO 2 - Comprimento de Runs: {p2}")
    if postulates[2]['warnings']:
        print(f"{yellow}  🔍 Warnings:")
        for warning in postulates[2]["warnings"]:
            print('\t- ' + warning)
    elif postulates[2]['comply']:
        print('  🎉 Nenhum problema encontrado')
#
    if not postulates[3]['comply']:
        print(f"\n{red}❌ Problemas RELEVANTES encontrados no PRESSUPOSTO 3")
        print(f"{yellow}  ⚠️  Relevants:")
        for relevant in postulates[3]["relevants"]:
            print('\t- ' + relevant)
    else:
        print(f"\n{green}📌 PRESSUPOSTO 3 - Autocorreção: {p3}")
    if postulates[3]['warnings']:
        print(f"{yellow}  🔍 Warnings:")
        for warning in postulates[3]["warnings"]:
            print('\t- ' + warning)
    elif postulates[3]['comply']:
        print('  🎉 Nenhum problema encontrado')

        


#STARTING CHOICES
def beginning_text(separator: str) -> str:
    """
    Exibe a introdução do programa com título, autor, explicação dos pressupostos e apresenta as opções de escolha inicial.

    :Note:
    - Não realiza validação da entrada. Qualquer valor digitado será retornado.
    - Se o 'separator' for uma string vazia ou mal formatada, a estética da apresentação será comprometida.

    :param separator: Separador visual exibido antes e depois do cabeçalho (ex: '-' * 50)
    :type separator: str
    :return: Escolha digitada pelo usuário (pode ser "1", "2", "3" ou qualquer outro valor)
    :rtype: str

    :Example:
    >>> separator = '-' * 50
    >>> opcao = beginning_text(separator)
    >>> print(opcao)
    1
    """
    print('\n\n\n' + separator)
    print(f"{Style.BRIGHT}{Fore.BLUE}Analisador de aleatoriedade - PRESSUPOSTOS DE GOLOMB".center(len(separator)))
    print(f"\t{Style.DIM}feito por: Lucas Marques".center(50))
    print(separator)
    print("\nPara uma sequencia de bits ser considerada imprevisivel, precisa cumprir os 3 pressupostos")
    print(f"{Style.DIM}Nota: muitas das regras aqui aplicadas são a minha interpretação de aleatoriedade")

    print(f'\nO que deseja fazer?')
    print(f'\t1. Analisar aleatoriedade de sequência.')
    print(f'\t2. Gerar uma sequência de bits.')
    print(f'\t3. Sair.')
    choice_to_do = input('')
    return choice_to_do

def chose_analise_sequence(separator: str, postulates: dict) -> None:
    """
    Analisa uma sequência de bits e verifica se ela cumpre os três pressupostos de Golomb. 
    Solicita a entrada do usuário, valida a sequência e exibe os resultados formatados.

    :Note:
    - Se a sequência contiver caracteres diferentes de 0 ou 1, o usuário será alertado e solicitado a tentar novamente.
    - Não há retorno: a função apenas imprime os resultados no terminal.

    :param separator: Separador visual usado para a apresentação do título
    :type separator: str
    :param postulates: Estrutura contendo os três pressupostos com status de conformidade e avisos
    :type postulates: dict
    :return: None
    :rtype: None

    :Example:
    >>> separator = '-' * 50
    >>> postulates = {
    ...     1: {'comply': True, 'relevants': [], 'warnings': []},
    ...     2: {'comply': True, 'relevants': [], 'warnings': []},
    ...     3: {'comply': True, 'relevants': [], 'warnings': []}
    ... }
    >>> chose_analise_sequence(separator, postulates)
    --------------------------------------------------
          ANALISADOR DE SEQUÊNCIA    	 
    --------------------------------------------------
       - Introduza a sua sequência de bits:
    >>> 101010100110101
    (resultados analisados são impressos via print_final_output)
    """
    debug_print('📌 Escolheu analisar uma sequência')

    print('\n\n' + separator)
    print(f'{Style.BRIGHT}{Fore.BLUE}ANALISADOR DE SEQUÊNCIA'.center(len(separator)))
    print(separator)

    while True:
        sequence = input('   - Introduza a sua sequência de bits: ')
        status = verify_sequence(sequence)
        if not status:
            print(f'⚠️  {Fore.RED}Valor inválido: {Style.RESET_ALL}\"{sequence}\". Apenas bits. Ex: 100101101')
        else: break

    #Getting sequence basics
    num_bits, runs, run_frequencies, ordered_run_sizes = gettin_sequence_basics(sequence)

    #Verifying if matches golomb
    postulates, min_percentage, percent_zeros, percent_ones = check_first_postulate(num_bits, postulates)
    postulates = check_second_postulate(run_frequencies, postulates)
    postulates = check_third_postulate(run_frequencies, ordered_run_sizes, runs, postulates)

    debug_print('\n📁 Fim da Analise')

    print_final_output(sequence, num_bits, percent_zeros, percent_ones, min_percentage, runs, run_frequencies, ordered_run_sizes, postulates)

def chose_generate_sequence(separator: str, postulates: dict) -> None:
    """
    Gera uma sequência de bits, podendo ser aleatória ou cumprir os pressupostos de Golomb.

    :Note:
    - Sempre pergunta ao usuário o comprimento da sequência e valida se é um número inteiro.
    - Em caso de geração com regras, permite escolher quais pressupostos deseja cumprir (1, 2 e/ou 3).
    - Usa funções auxiliares 'create_random_sequence()' ou 'create_postulates_sequence()' para gerar a sequência.

    :param separator: Linha de separação usada para exibir o título (geralmente 50*'-').
    :type separator: str

    :param postulates: Dicionário contendo os três pressupostos e seu estado atual de conformidade.
    :type postulates: dict

    :return: None
    :rtype: None

    :Example:
    >>> postulates = {
    ...     1: {'comply': True, 'relevants': [], 'warnings': []},
    ...     2: {'comply': True, 'relevants': [], 'warnings': []},
    ...     3: {'comply': True, 'relevants': [], 'warnings': []}
    ... }
    >>> chose_generate_sequence('-'*50, postulates)
    --------------------------------------------------
          	GERADOR DE SEQUÊNCIA      	 
    --------------------------------------------------
    Que tipo de sequencia deseja criar?
        	1. Sequencia gerada aleatoriamente.
        	2. Sequencia que cumpra os pressupostos
    2
    Qual o comprimento da sequência? 23
    Selecione com um 'X' os que deseja cumprir
        	Pressuposto 1, equilibrio: x
        	Pressuposto 2, frequência: x
        	Pressuposto 3, padrões:	x
    Sequência: 00101111101100011010001
    """
    debug_print('📌 Escolheu gerar uma sequência')

    print('\n\n' + separator)
    print(f'{Fore.BLUE}{Style.BRIGHT}GERADOR DE SEQUÊNCIA'.center(len(separator)))
    print(separator)
    print('Que tipo de sequencia deseja criar?')
    print('\t1. Sequencia gerada aleatoriamente.')
    print('\t2. Sequencia que cumpra os pressupostos')
    choice_seq_type = input('')
    
    while True:
        try:
            lenght = input('\nQual o comprimento da sequência? ')
            debug_print('\n🔍 Verificando se comprimento é inteiro')
            lenght = int(lenght)
            debug_print('✅ Comprimento válido')
            break
        except ValueError:
            debug_print('❌ Comprimento inválido')
            print(f'⚠️  {Fore.RED}Valor inválido: {Style.RESET_ALL}\"{lenght}\". Apenas números')

    debug_print('\n🧐 Analisando o tipo de sequência a gerar')

    if choice_seq_type == '2':
        #Geração baseada nos pressupostos selecionados
        debug_print('📌 Escolheu gerar sequencia com regras')
        print('\nSelecione com um \'X\' os que deseja cumprir')

        postulates_to_match = []
        postulates_to_match.append(input('\tPressuposto 1, equilibrio: '))
        postulates_to_match.append(input('\tPressuposto 2, frequência: '))
        postulates_to_match.append(input('\tPressuposto 3, padrões:    '))

        postulate_sequence = create_postulates_sequence(postulates_to_match, postulates, lenght)
        debug_print('\n📝 Exibindo resultado')
        print(f'\n{Fore.YELLOW}Sequência:', postulate_sequence)

    else:
        #Geração aleatória
        debug_print('📌 Escolheu gerar sequencia aleatoria')

        random_sequence = create_random_sequence(lenght)
        debug_print('\n📝 Exibindo resultado')
        print(f'\n{Fore.YELLOW}Sequência aleatoria:', random_sequence)


#MAIN
if __name__ == '__main__': 
    """
    O bloco if __name__ == '__main__': executa a lógica principal do programa, permitindo ao usuário inserir 
    uma sequência binária e visualizar se ela cumpre ou não os três pressupostos de Golomb.

    :Program Flow:
    1. Solicita uma sequência binária ao usuário.
    2. Exibe a sequência recebida.
    3. Realiza a verificação de conformidade com os três pressupostos:
        Pressuposto 1: Proporção entre zeros e uns.
        Pressuposto 2: Frequência de subsequências de comprimentos diferentes.
        Pressuposto 3: Distribuição equilibrada de padrões binários.
    4. Mostra, para cada pressuposto:
        Se cumpre ou não (Comply: True/False);
        Avisos relevantes (se houver);
        Alertas secundários (se houver).
    5. Exibe uma tabela-resumo com os três resultados de conformidade (✔ ou ✘).
    6. Permite opcionalmente gerar uma nova sequência binária que satisfaça os pressupostos marcados como "ativos".
    """
    while True:
        separator = '-' * 50
        choice_to_do = beginning_text(separator)

        postulates = {
            1: {'comply': True, 'relevants': [], 'warnings': []},
            2: {'comply': True, 'relevants': [], 'warnings': []},
            3: {'comply': True, 'relevants': [],'warnings': []}
        }

        debug_print('\n🧐 Analisando escolha')

        if choice_to_do == '1':
            chose_analise_sequence(separator, postulates)

        elif choice_to_do == '2':

            chose_generate_sequence(separator, postulates)
        else:
            debug_print('❌ Escolheu sair do programa')
            break

        choice_restart = input('\n\nDeseja recomeçar? (S/N)')
        if choice_restart not in 'Ss':
            break
