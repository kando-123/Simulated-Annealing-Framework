# CONLANG VOCABULARY GENERATION

VALS_1 = [
    'b', 'bl', 'br',
    'c',
    'd', 'dr',
    'f', 'fl', 'fr',
    'g', 'gl', 'gr',
    'h',
    'j',
    'k', 'kl', 'kr',
    'l',
    'm',
    'n',
    'p', 'pl', 'pr',
    'r',
    's',
    't', 'tr',
    'v',
    'w',
    'z'
]

VALS_2 = [
    'a', 'ia', 'ua', 'ai', 'au',
    'e', 'ie', 'ue', 'ei',
    'o', 'io', 'uo', 'oi',
    'i', 'ui',
    'u', 'iu'
]

VALS_3 = [
    'b', 'lb', 'mb', 'rb', 'zb', 'bl', 'br',
    'c', 'lc', 'nc', 'rc',
    'd', 'ld', 'nd', 'rd', 'zd', 'dr',
    'f', 'lf', 'rf', 'fl', 'fr',
    'g', 'lg', 'ng', 'rg', 'zg', 'gl', 'gr',
    'k', 'lk', 'nk', 'rk', 'sk', 'kl', 'kr',
    'l',
    'm',
    'n',
    'p', 'lp', 'mp', 'rp', 'sp', 'pl', 'pr',
    'r',
    's',
    't', 'lt', 'nt', 'rt', 'st', 'tr',
    'v', 'lv', 'rv', 'vl', 'vr',
    'z'
]

POOL = [
    f'{v1}{v2}{v3}' for v1 in VALS_1 for v2 in VALS_2 for v3 in VALS_3
    if not (
        len(v1) + len(v2) + len(v3) > 5
        or (('l' in v1 or 'r' in v1) and ('l' in v3 or 'r' in v3) and len(v1) + len(v3) == 4)
        or (v1, v2) in { ('j', 'i'), ('w', 'u') }
        or (
            v2 in { 'ia', 'ie', 'io', 'iu' } and (
                v1 in { 'c', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'r', 's', 'w', 'z' }
                or len(v1) > 1
                or (len(v3) > 1 and v3[0] in { 'l', 'r' })
            )
        )
        or (
            v2 in { 'ua', 'ue', 'ui', 'uo' } and (
                v1 in { 'b', 'f', 'h', 'j', 'l', 'm', 'n', 'p', 'r', 'v', 'w' }
                or len(v1) > 1
                or (len(v3) > 1 and v3[0] in { 'l', 'r' })
            )
        )
        or (v2 in { 'ai', 'ei', 'oi' } and len(v3) > 1)
        or (v2 == 'au' and (len(v3) > 1 or v3 in { 'b', 'f', 'm', 'p', 'v' }))
    )
]

def roots():
    return POOL[::]

def phonemize(root: str) -> str:
    phonemes = []
    for l, letter in enumerate(root):
        
        if letter == 'n':
            if l + 1 < len(root) and root[l + 1] in { 'k', 'g' }:
                phonemes.append('N')
            else:
                phonemes.append('n')
        
        elif letter == 'i':
            if l + 1 < len(root) and root[l + 1] in { 'a', 'e', 'o', 'u' }:
                phonemes.append('j')
            elif l > 0 and root[l - 1] in { 'a', 'e', 'o' }:
                phonemes.append('j')
            else:
                phonemes.append('i')
        
        elif letter == 'u':
            if l + 1 < len(root) and root[l + 1] in { 'a', 'e', 'i', 'o' }:
                phonemes.append('w')
            elif l > 0 and root[l - 1] in { 'a', 'e', 'o' }:
                phonemes.append('w')
            else:
                phonemes.append('u')
        
        else:
            phonemes.append(letter)
        
    return "".join(phonemes)

PHONEMIZER, DEPHONEMIZER = { r: phonemize(r) for r in POOL }, { phonemize(r): r for r in POOL }

def phroots():
    return PHONEMIZER.values()

def dephonemize(phroot):
    return DEPHONEMIZER[phroot]

CONSONANTS = {
    'b': ('voiced',   'bilabial',       'plosive'),
    'c': ('unvoiced', 'palatoalveolar', 'affricate'),
    'd': ('voiced',   'alveolar',       'plosive'),
    'f': ('unvoiced', 'labiodental',    'fricative'),
    'g': ('voiced',   'velar',          'plosive'),
    'h': ('unvoiced', 'glottal',        'fricative'),
    'j': ('sonorant', 'palatal',        'approximant'),
    'k': ('unvoiced', 'velar',          'plosive'),
    'l': ('sonorant', 'alveolar',       'lateral'),
    'm': ('sonorant', 'bilabial',       'nasal'),
    'n': ('sonorant', 'alveolar',       'nasal'),
    'N': ('sonorant', 'velar',          'nasal'),
    'p': ('unvoiced', 'bilabial',       'plosive'),
    'r': ('sonorant', 'alveolar',       'tap'),
    's': ('unvoiced', 'alveolar',       'fricative'),
    't': ('unvoiced', 'alveolar',       'plosive'),
    'v': ('voiced',   'labiodental',    'fricative'),
    'w': ('sonorant', 'bilabial',       'approximant'),
    'z': ('voiced',   'alveolar',       'fricative')
}
CONSONANT_ATTRIBUTE_WEIGHTS = [0.2, 0.3, 0.5]

VOWELS = {
    'a': ('open',  'central', 'unrounded'),
    'e': ('mid',   'front',   'unrounded'),
    'i': ('close', 'front',   'unrounded'),
    'o': ('mid',   'back',    'rounded'),
    'u': ('close', 'back',    'rounded')
}
VOWEL_ATTRIBUTE_WEIGHTS = [0.4, 0.4, 0.2]

# 0.0 = identical, 0.5 = similar, 1.0 = completely different
ATTRIBUTE_DIFFERENCES = {
    
    # Voicedness
    ('voiced', 'sonorant'): 0.5,
    
    # Place of articulation
    ('bilabial', 'labiodental'):    0.2,
    ('bilabial', 'alveolar'):       0.5,
    ('labiodental', 'alveolar'):    0.4,
    ('alveolar', 'palatoalveolar'): 0.5,
    ('palatoalveolar', 'palatal'):  0.5,
    ('palatal', 'velar'):           0.5,
    ('palatal', 'glottal'):         0.6,
    ('velar', 'glottal'):           0.2,
    
    # Manner of articulation
    ('plosive', 'fricative'):   0.5,
    ('plosive', 'affricate'):   0.3,
    ('fricative', 'affricate'): 0.3,
    ('plosive', 'nasal'):       0.5,
    ('nasal', 'approximant'):   0.5,
    ('nasal', 'lateral'):       0.5,
    ('nasal', 'tap') :          0.5,
    ('approximant', 'lateral'): 0.4,
    ('approximant', 'tap'):     0.4,
    ('lateral', 'tap'):         0.3,
    
    # Vertical position
    ('open', 'mid'):  0.5,
    ('close', 'mid'): 0.5,
    
    # Horizontal position
    ('front', 'central'): 0.5,
    ('back',  'central'): 0.5
}

def attribute_difference(lhs, rhs):
    if lhs == rhs: return 0.0
    elif (lhs, rhs) in ATTRIBUTE_DIFFERENCES: return ATTRIBUTE_DIFFERENCES[lhs, rhs]
    elif (rhs, lhs) in ATTRIBUTE_DIFFERENCES: return ATTRIBUTE_DIFFERENCES[rhs, lhs]
    else: return 1.0

# 0.00 = identical,
# 0.50 = similar in-group (vowel/vowel, consonant/consonant),
# 0.75 = vowel/semivowel pair (borderline cases),
# 1.00 = different in-group or vowel,
# 3.00 = vowel/consonant difference (implicit)
SUBSTITUTION_COSTS = {
   ('i', 'j'): 0.75,
   ('j', 'i'): 0.75,
   ('u', 'w'): 0.75,
   ('w', 'u'): 0.75
}

for cons1, attr1 in CONSONANTS.items():
    for cons2, attr2 in CONSONANTS.items():
        difference = 0
        for a1, a2, w in zip(attr1, attr2, CONSONANT_ATTRIBUTE_WEIGHTS):
            difference += w * attribute_difference(a1, a2)
        SUBSTITUTION_COSTS[cons1, cons2] = round(difference, 2)

for vow1, attr1 in VOWELS.items():
    for vow2, attr2 in VOWELS.items():
        difference = 0
        for a1, a2, w in zip(attr1, attr2, VOWEL_ATTRIBUTE_WEIGHTS):
            difference += w * attribute_difference(a1, a2)
        SUBSTITUTION_COSTS[vow1, vow2] = round(difference, 2)

for (l, r), dist in SUBSTITUTION_COSTS.items():
    diff = SUBSTITUTION_COSTS.get((r, l))
    if diff is None:   raise Exception(f'Pair ({r}, {l}) absent in the dictionary despite ({l}, {r}) being present.')
    elif diff != dist: raise Exception(f'Value {diff} for pair ({r}, {l}) different than value {dist} for pair ({l}, {r}).')

# print('Substitution costs have been calculated.')

IDENTITY = 0.0
VOWEL_CONSONANT_DIFFERENCE = 3.0

def substitution_cost(x, y):
    if x == y:
        return IDENTITY
    else:
        return SUBSTITUTION_COSTS.get((x, y), VOWEL_CONSONANT_DIFFERENCE)

DELETION_COST = 1.0
INSERTION_COST = 1.0
TRANSPOSITION_COST = 1.0

def levenshtein(root1, root2):
    
    n_rows, n_cols = len(root1) + 1, len(root2) + 1
    
    matrix = [[0 for col in range(n_cols)] for row in range(n_rows)]
    
    for row in range(n_rows): matrix[row][0] = row
    for col in range(n_cols): matrix[0][col] = col
    
    for row in range(1, n_rows):
        for col in range(1, n_cols):
            deletion     = matrix[row - 1][col] + DELETION_COST
            insertion    = matrix[row][col - 1] + INSERTION_COST
            substitution = matrix[row - 1][col - 1] + substitution_cost(root1[row - 1], root2[col - 1])
            distance = min(deletion, insertion, substitution)
            if row >= 2 and col >= 2:
                transposition = (matrix[row - 2][col - 2]
                                 + substitution_cost(root1[row - 1], root2[col - 2])
                                 + substitution_cost(root1[row - 2], root2[col - 1])
                                 + TRANSPOSITION_COST)
                distance = min(distance, transposition)
            matrix[row][col] = distance
    
    return matrix[-1][-1]
