GORAFI_LEXIQUE_RAW: dict[str, list[str]] = {
    # Noms communs
    'mention':           ['N'],
    'culpabilité-score': ['NP', 'N'],
    'aliment':           ['N'],
    'aliments':          ['N'],
    'nutriscore':        ['N'],
    'nutriscores':       ['N'],
    'gouvernement':      ['N'],
    'nutritionniste':    ['N'],
    'principe':          ['N'],
    'objectif':          ['N'],
    'plaisir':           ['N'],
    'rayon':             ['N'],
    'friandise':         ['N'],
    'bol':               ['N'],
    'radis':             ['N'],
    'chagrin':           ['N'],
    'gens':              ['N'],
 
    # Auxiliaires et modaux
    'sera':      ['(S\\NP)/(S\\NP)'],
    'devraient': ['(S\\NP)/(S\\NP)'],
    'devront':   ['(S\\NP)/(S\\NP)'],
    'avoir':     ['(S\\NP)/(S\\NP)', '(S\\NP)/NP', '(S\\NP)/((S\\NP)/NP)'],
    'se':        ['(S\\NP)/(S\\NP)'],
 
    # Verbes
    'ajoutée':   ['S\\NP', '(S\\NP)/NP'],
    'noté':      ['S\\NP', '(S\\NP)/NP'],
    'décidé':    ['S\\NP', '(S\\NP)/S'],
    'porter':    ['S\\NP', '(S\\NP)/NP'],
    'noyer':     ['S\\NP', '(S\\NP)/NP'],
    'faire':     ['S\\NP', '(S\\NP)/NP'],
    'inciter':   ['(S\\NP)/NP', '((S\\NP)/NP)/NP'],
    'recommande':['(S\\NP)/S', '(S\\NP)/NP'],
    'fini':      ['S\\NP', 'S'],
 
    # Adjectifs postnominaux
    'simple':   ['N\\N', 'S\\NP'],
    'coupable': ['N\\N'],
    'plate':    ['N\\N'],
    'géant':    ['N\\N'],
 
    # Adverbes
    'aveuglément': ['S\\S', '(S\\NP)\\(S\\NP)'],
    'jamais':      ['(S\\NP)\\(S\\NP)'],
 
    # Prépositions
    'à':    ['(NP\\NP)/NP', '((S\\NP)\\(S\\NP))/NP'],
    'dans': ['(NP\\NP)/NP', '((S\\NP)\\(S\\NP))/NP'],
    'après': ['((S\\NP)\\(S\\NP))/NP', '(S\\S)/NP'],
}
 
GORAFI_EXAMPLES = [
    'chaque aliment sera noté',
    'le principe de ce culpabilité-score est simple',
    'une mention de culpabilité-score sera ajoutée sur les aliments',
    'le gouvernement a décidé que les aliments devraient désormais porter la mention de culpabilité-score',
    'Après les nutriscores le gouvernement a décidé que les aliments devraient désormais porter la mention de culpabilité-score',
    'Fini de se faire plaisir aveuglément au rayon friandise',
    'notre objectif est de inciter les gens à noyer leur chagrin dans un bol de radis',
]
