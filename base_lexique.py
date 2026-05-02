# Lexique de base — phrases du cours
BASE_LEXIQUE_RAW: dict[str, list[str]] = {
    # Noms propres
    'Garfield': ['NP'], 'Mickey': ['NP'], 'Minnie': ['NP'],
    'Sylvestre': ['NP'], 'Jerry': ['NP'], 'Tweety': ['NP'],

    # Déterminants
    'le': ['NP/N'], 'la': ['NP/N'], 'les': ['NP/N'],
    'un': ['NP/N'], 'une': ['NP/N'],
    'ce': ['NP/N'], 'cet': ['NP/N'],
    'chaque': ['NP/N'], 'notre': ['NP/N'], 'leur': ['NP/N'],
    'au': ['NP/N', '(NP\\NP)/NP'],

    # Noms communs
    'chat': ['N'], 'souris': ['N'], 'poisson': ['N'],

    # Verbes intransitifs
    'dort': ['S\\NP'], 'vole': ['S\\NP'], 'court': ['S\\NP'],

    # Verbes transitifs
    'mange':    ['S\\NP', 'S\\NP/NP'],
    'devore':   ['S\\NP', 'S\\NP/NP'],
    'tue':      ['S\\NP', 'S\\NP/NP'],
    'bate':     ['S\\NP', 'S\\NP/NP'],
    'dépiaute': ['S\\NP', 'S\\NP/NP'],
    'attaque':  ['S\\NP', 'S\\NP/NP'],
    'manger':   ['S\\NP', 'S\\NP/NP'],
    'attraper': ['S\\NP/NP'],

    # Verbes ditransitifs
    'montre': ['S\\NP', 'S\\NP/NP', '(S\\NP/NP)/NP'],
    'donne':  ['S\\NP', 'S\\NP/NP', '(S\\NP/NP)/NP'],

    # Verbes à complétive
    'pense':  ['S\\NP', '(S\\NP)/S'],
    'croit':  ['S\\NP', '(S\\NP)/S'],
    'dit':    ['S\\NP', '(S\\NP)/S', '(S\\NP)/NP'],
    'décide': ['S\\NP', '(S\\NP)/S'],

    # Auxiliaires modaux
    'va':      ['(S\\NP)/(S\\NP)'],
    'devrait': ['(S\\NP)/(S\\NP)'],
    'peut':    ['(S\\NP)/(S\\NP)'],
    'doit':    ['(S\\NP)/(S\\NP)'],
    'est':     ['(S\\NP)/(S\\NP)', '(S\\NP)/NP'],
    'sont':    ['(S\\NP)/(S\\NP)'],

    # Auxiliaire avoir
    'a':   ['(S\\NP)/(S\\NP)', '(S\\NP)/((S\\NP)/NP)', '((S\\NP)/NP)/((S\\NP)/NP)', '(S\\NP)/((S\\NP)/S)'],
    'ont': ['(S\\NP)/(S\\NP)', '(S\\NP)/((S\\NP)/NP)', '((S\\NP)/NP)/((S\\NP)/NP)'],

    # Participes passés
    'mangé':   ['S\\NP', 'S\\NP/NP'],
    'dormi':   ['S\\NP'],
    'couru':   ['S\\NP'],
    'tué':     ['S\\NP', 'S\\NP/NP'],
    'dépauté': ['S\\NP', 'S\\NP/NP'],

    # Adverbes
    'voracement': ['S\\S', '(S\\NP/NP)\\(S\\NP/NP)'],
    'violemment': ['S\\S', '(S\\NP/NP)\\(S\\NP/NP)'],
    'rapidement': ['S\\S', '(S\\NP/NP)\\(S\\NP/NP)'],
    'lentement':  ['S\\S', '(S\\NP/NP)\\(S\\NP/NP)'],
    'souvent':    ['S\\S', '(S\\NP/NP)\\(S\\NP/NP)', '(S\\NP)/(S\\NP)'],
    'désormais':  ['S\\S', '(S\\NP)\\(S\\NP)', '(S\\NP/NP)\\(S\\NP/NP)', '(S\\NP)/(S\\NP)'],

    # Adjectifs prénominaux
    'grand': ['N/N'], 'grande': ['N/N'], 'petit': ['N/N'], 'petite': ['N/N'],
    'gros':  ['N/N'], 'grosse': ['N/N'], 'vieux': ['N/N'], 'jeune':  ['N/N'],

    # Prépositions
    'de':  ['(NP\\NP)/NP', '(NP\\NP)/N', 'S/S'],
    'sur': ['(NP\\NP)/NP', '((S\\NP)\\(S\\NP))/NP'],

    # Mots fonctionnels
    'et':  ['NP\\NP/NP', 'S\\S/S', '(S\\NP)\\(S\\NP)/(S\\NP)', '(S\\NP/NP)\\(S\\NP/NP)/(S\\NP/NP)'],
    'que': ['(NP\\NP)/(S/NP)', 'S/S'],
    'qui': ['(NP\\NP)/(S\\NP)'],
    'ne':  ['(S\\NP)/(S\\NP)'],

    # Adjectifs postnominaux (voir gorafi_lexique.py)
    'pas': ['(S\\NP)\\(S\\NP)', '(S\\NP/NP)\\(S\\NP/NP)'],
}

BASE_EXAMPLES = [
    'Garfield mange', 'Garfield mange Mickey', 'le chat mange la souris',
    'Garfield va manger Mickey', 'Sylvestre mange Mickey et Minnie',
    'Mickey dort voracement', 'Mickey bate Garfield violemment',
    'Garfield mange voracement Mickey', 'Garfield va attraper et devrait manger Minnie',
    'Garfield tue et Sylvestre dépiaute Jerry', 'Mickey que Garfield devore dort',
    'Garfield devore Mickey que Jerry tue', 'Garfield mange et Mickey mange',
    'le grand chat mange la petite souris', 'Garfield montre Mickey Jerry',
    'Garfield donne Minnie Jerry', 'Garfield montre le chat Jerry',
    'Garfield pense que Mickey dort', 'Garfield ne mange pas Mickey',
    'Garfield souvent mange Mickey', 'Garfield a mangé Minnie', 'Mickey a dormi',
    'Garfield a mangé Minnie voracement', 'Garfield Mickey mange',
    'Garfield mange voracement Minnie',
]
