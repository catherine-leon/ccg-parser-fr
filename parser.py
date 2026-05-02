from __future__ import annotations
from dataclasses import dataclass
from typing import Union, Optional, Any

Cat = Union[str, dict]

from base_lexique import BASE_LEXIQUE_RAW, BASE_EXAMPLES

LEXIQUE_RAW = BASE_LEXIQUE_RAW
EXAMPLES = BASE_EXAMPLES




def strip_outer_parens(s: str) -> str:
    """Supprime les parenthèses extérieures redondantes d'une catégorie.
    Ex: '((S\\NP)/NP)' -> '(S\\NP)/NP'
    """
    s = s.strip()
    while s.startswith('(') and s.endswith(')'):
        depth = 0
        ok = True
        for i, ch in enumerate(s):
            if ch == '(':
                depth += 1
            elif ch == ')':
                depth -= 1
                if depth == 0 and i != len(s) - 1:
                    ok = False
                    break
        if ok:
            s = s[1:-1].strip()
        else:
            break
    return s


def parse_cat(s: str) -> Cat:
    """Convertit une chaîne de catégorie CCG en représentation interne récursive.
    Une catégorie atomique ('S', 'NP', 'N') est retournée comme chaîne.
    Une catégorie fonctionnelle est retournée comme dict {'dir': 'R'|'L', 'left': Cat, 'right': Cat}.
    Ex: '(S\\NP)/NP' -> {'dir': 'R', 'left': {'dir': 'L', 'left': 'S', 'right': 'NP'}, 'right': 'NP'}
    """
    s = strip_outer_parens(s)
    depth = 0
    for i in range(len(s) - 1, -1, -1):
        ch = s[i]
        if ch == ')':
            depth += 1
        elif ch == '(':
            depth -= 1
        elif depth == 0 and ch in ('/', '\\'):
            return {'dir': 'R' if ch == '/' else 'L', 'left': parse_cat(s[:i]), 'right': parse_cat(s[i+1:])}
    return s


def show_cat(cat: Cat) -> str:
    """Convertit une catégorie interne en notation textuelle CCG.
    Inverse de parse_cat. Ex: {'dir': 'R', 'left': 'S\\NP', 'right': 'NP'} -> '(S\\NP)/NP'
    """
    if isinstance(cat, str):
        return cat
    sep = '/' if cat['dir'] == 'R' else '\\'
    left = show_cat(cat['left']) if isinstance(cat['left'], str) else f"({show_cat(cat['left'])})"
    right = show_cat(cat['right']) if isinstance(cat['right'], str) else f"({show_cat(cat['right'])})"
    return f'{left}{sep}{right}'


def eq_cat(a: Cat, b: Cat) -> bool:
    """Teste l'égalité structurelle de deux catégories CCG.
    Deux catégories sont égales si elles ont la même direction et les mêmes sous-catégories.
    """
    if isinstance(a, str) and isinstance(b, str):
        return a == b
    if isinstance(a, str) or isinstance(b, str):
        return False
    return a['dir'] == b['dir'] and eq_cat(a['left'], b['left']) and eq_cat(a['right'], b['right'])


def type_raising(cat: Cat, y: Cat | str = 'S') -> Cat:
    """Applique la montée catégorielle (Type Raising) à une catégorie.
    Transforme X en T/(T\\X), par défaut T=S.
    Ex: NP -> S/(S\\NP), ce qui permet au sujet de se comporter comme une fonction.
    """
    yc = parse_cat(y) if isinstance(y, str) else y
    return {'dir': 'R', 'left': yc, 'right': {'dir': 'L', 'left': yc, 'right': cat}}


def make_lexique(extra: Optional[dict[str, list[str]]] = None) -> dict[str, list[Cat]]:
    """Construit le lexique opérationnel à partir de LEXIQUE_RAW.
    Convertit toutes les catégories de leur forme textuelle en représentation interne.
    Le paramètre extra permet d'étendre le lexique de base (utilisé pour le Gorafi).
    """
    raw = {k: list(v) for k, v in LEXIQUE_RAW.items()}
    if extra:
        raw.update(extra)
    return {w: [parse_cat(c) for c in cats] for w, cats in raw.items()}


def lookup(word: str, lexique: dict[str, list[Cat]]) -> list[Cat]:
    """Cherche les catégories d'un mot dans le lexique.
    Essaie d'abord la forme exacte, puis la forme en minuscules.
    Retourne une liste vide si le mot est inconnu.
    """
    return lexique.get(word) or lexique.get(word.lower()) or []


def apply_rules(g: Cat, d: Cat) -> list[tuple[Cat, str]]:
    """Applique les règles de combinaison CCG à deux catégories adjacentes.
    Retourne la liste des (catégorie résultante, nom de la règle) possibles.
    Règles implémentées :
    - App>  : X/Y + Y   -> X  (application droite)
    - App<  : Y + X\\Y  -> X  (application gauche)
    - Comp>B: X/Y + Y/Z -> X/Z  (composition harmonique droite)
    - Comp<B: Y\\Z + X\\Y -> X\\Z  (composition harmonique gauche)
    La coordination <*> est traitée séparément dans la boucle CYK (règle ternaire).
    """
    results: list[tuple[Cat, str]] = []
    if isinstance(g, dict) and g['dir'] == 'R' and eq_cat(g['right'], d):
        results.append((g['left'], 'App>'))
    if isinstance(d, dict) and d['dir'] == 'L' and eq_cat(d['right'], g):
        results.append((d['left'], 'App<'))
    if isinstance(g, dict) and g['dir'] == 'R' and isinstance(d, dict) and d['dir'] == 'R' and eq_cat(g['right'], d['left']):
        results.append(({'dir': 'R', 'left': g['left'], 'right': d['right']}, 'Comp>B'))
    if isinstance(g, dict) and g['dir'] == 'L' and isinstance(d, dict) and d['dir'] == 'L' and eq_cat(d['right'], g['left']):
        results.append(({'dir': 'L', 'left': d['left'], 'right': g['right']}, 'Comp<B'))
    return results


def leaf(word: str, cat: Cat, pos: int) -> dict[str, Any]:
    """Crée un nœud feuille de l'arbre de dérivation (entrée lexicale)."""
    return {'type': 'leaf', 'mot': word, 'cat': show_cat(cat), 'pos': pos}


def node(cat: Cat, rule: str, left: dict[str, Any], right: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    """Crée un nœud interne de l'arbre de dérivation (résultat d'une règle)."""
    return {'type': 'node', 'cat': show_cat(cat), 'rule': rule, 'left': left, 'right': right}


def span_of(t: dict[str, Any]) -> tuple[int, int]:
    """Retourne le span (début, fin) couvert par un nœud de l'arbre."""
    if t['type'] == 'leaf':
        return t['pos'], t['pos']
    if not t.get('right'):
        return span_of(t['left'])
    return span_of(t['left'])[0], span_of(t['right'])[1]


def tree_steps(t: dict[str, Any]) -> list[dict[str, Any]]:
    """Sérialise un arbre de dérivation en liste d'étapes pour le frontend.
    Chaque étape contient : span (d, f), catégorie résultante et règle appliquée.
    L'ordre respecte la progression gauche-droite de la dérivation.
    """
    steps: list[dict[str, Any]] = []
    def visit(n: dict[str, Any]):
        if not n or n['type'] == 'leaf':
            return
        if not n.get('right'):
            visit(n['left'])
            d, f = span_of(n['left'])
            steps.append({'d': d, 'f': f, 'cat': n['cat'], 'rule': n['rule']})
            return
        if n['rule'] == '<*>':
            inner = n['right']
            visit(n['left'])
            if inner and inner.get('type') != 'leaf' and inner.get('rule') == '<*>':
                visit(inner['left']); visit(inner['right'])
            else:
                visit(inner)
            d = span_of(n['left'])[0]
            f = span_of(inner)[1]
            steps.append({'d': d, 'f': f, 'cat': n['cat'], 'rule': n['rule']})
            return
        visit(n['left']); visit(n['right'])
        d = span_of(n['left'])[0]
        f = span_of(n['right'])[1]
        steps.append({'d': d, 'f': f, 'cat': n['cat'], 'rule': n['rule']})
    visit(t)
    return steps


def word_cats(t: dict[str, Any]) -> dict[str, str]:
    """Extrait la catégorie assignée à chaque mot (par position) dans un arbre.
    Retourne un dict {position: catégorie} utilisé par le frontend pour l'affichage.
    """
    cats: dict[str, str] = {}
    def visit(n: dict[str, Any]):
        if not n:
            return
        if n['type'] == 'leaf':
            cats[str(n['pos'])] = n['cat']
            return
        visit(n['left'])
        if n.get('right'):
            visit(n['right'])
    visit(t)
    return cats


def parse(phrase: str, type_raise: bool = True, max_trees: int = 5, extra_lexique: Optional[dict[str, list[str]]] = None) -> dict[str, Any]:
    """Parse une phrase en CCG et retourne toutes les analyses.

    Algorithme CYK (Cocke-Younger-Kasami) bottom-up :
    - Initialisation : chaque mot reçoit ses catégories lexicales + TypeR si NP
    - Remplissage : pour chaque span [i,j], on essaie toutes les partitions [i,k]+[k+1,j]
      et on applique les règles binaires (App>, App<, Comp>B, Comp<B) et la coordination (<*>)
    - TypeR est aussi appliqué à tous les spans NP construits (pas seulement les feuilles)

    Args:
        phrase:       La phrase à analyser (séparée par espaces).
        type_raise:   Active/désactive la montée catégorielle.
        max_trees:    Nombre maximum d'arbres stockés par cellule CYK.
        extra_lexique: Entrées lexicales supplémentaires (ex: lexique Gorafi).

    Returns:
        Dict contenant :
        - mots       : liste des tokens
        - complete   : analyses complètes (menant à S) sérialisées
        - partials   : chemins partiels (impasses) sérialisés, max 50
        - metrics    : successes, impasses (comptage réel), rulesAttempted, etc.
        - lexique    : lexique utilisé pour cette phrase
    """
    mots = [m for m in phrase.strip().split() if m]
    n = len(mots)
    if n == 0:
        return {'mots': [], 'complete': [], 'partials': [], 'metrics': {}}
    lexique = make_lexique(extra_lexique)
    T: list[list[dict[str, dict[str, Any]]]] = [[{} for _ in range(n)] for _ in range(n)]
    NP = parse_cat('NP')
    S = parse_cat('S')
    S_KEY = show_cat(S)

    for i, mot in enumerate(mots):
        for cat in lookup(mot, lexique):
            key = show_cat(cat)
            T[i][i].setdefault(key, {'cat': cat, 'trees': []})
            T[i][i][key]['trees'].append(leaf(mot, cat, i))
        if type_raise and any(eq_cat(c, NP) for c in lookup(mot, lexique)):
            tr = type_raising(NP)
            k = show_cat(tr)
            T[i][i].setdefault(k, {'cat': tr, 'trees': []})
            for entry in list(T[i][i].values()):
                for t in entry['trees']:
                    if t['type'] == 'leaf' and t['cat'] == 'NP' and len(T[i][i][k]['trees']) < max_trees:
                        T[i][i][k]['trees'].append(node(tr, 'TypeR', t))

    for length in range(2, n + 1):
        for i in range(0, n - length + 1):
            j = i + length - 1
            for k in range(i, j):
                for eg in list(T[i][k].values()):
                    for ed in list(T[k+1][j].values()):
                        for res, rule in apply_rules(eg['cat'], ed['cat']):
                            sk = show_cat(res)
                            T[i][j].setdefault(sk, {'cat': res, 'trees': []})
                            lst = T[i][j][sk]['trees']
                            for tg in eg['trees']:
                                for td in ed['trees']:
                                    if len(lst) < max_trees:
                                        lst.append(node(res, rule, tg, td))
                # coordination X conj X -> X, using lexical category X\X/X on the conjunction cell
                for ec in list(T[k][k].values()):
                    cat_c = ec['cat']
                    if isinstance(cat_c, dict) and cat_c['dir'] == 'R' and isinstance(cat_c['left'], dict) and cat_c['left']['dir'] == 'L':
                        x_d, x_g, x_r = cat_c['right'], cat_c['left']['right'], cat_c['left']['left']
                        if eq_cat(x_d, x_g) and eq_cat(x_g, x_r) and k > i:
                            for eg2 in list(T[i][k-1].values()):
                                if not eq_cat(eg2['cat'], x_g):
                                    continue
                                for ed2 in list(T[k+1][j].values()):
                                    if not eq_cat(ed2['cat'], x_d):
                                        continue
                                    sk = show_cat(x_r)
                                    T[i][j].setdefault(sk, {'cat': x_r, 'trees': []})
                                    lst = T[i][j][sk]['trees']
                                    for tg in eg2['trees']:
                                        for tc in ec['trees']:
                                            for td in ed2['trees']:
                                                if len(lst) < max_trees:
                                                    lst.append(node(x_r, '<*>', tg, node(x_r, '<*>', tc, td)))
            if type_raise and show_cat(NP) in T[i][j]:
                tr = type_raising(NP)
                tr_key = show_cat(tr)
                T[i][j].setdefault(tr_key, {'cat': tr, 'trees': []})
                for t in T[i][j][show_cat(NP)]['trees']:
                    if len(T[i][j][tr_key]['trees']) < max_trees:
                        T[i][j][tr_key]['trees'].append(node(tr, 'TypeR', t))

    complete_trees = T[0][n-1].get(S_KEY, {'trees': []})['trees']

    def find_partials(pos: int, path: list[dict[str, Any]], results: list[list[dict[str, Any]]], max_p: int):
        if len(results) >= max_p:
            return
        if pos == n:
            if len(path) == 1 and path[0]['i'] == 0 and path[0]['j'] == n-1 and path[0].get('cat') == S_KEY:
                return
            is_block = False
            if len(path) == 1 and path[0].get('cat') and path[0]['cat'] != S_KEY:
                is_block = True
            if len(path) >= 2:
                for kk in range(len(path) - 1):
                    a, b = path[kk], path[kk+1]
                    if a.get('cat_obj') is not None and b.get('cat_obj') is not None:
                        if len(apply_rules(a['cat_obj'], b['cat_obj'])) == 0:
                            is_block = True
                            break
                last = path[-1]
                if isinstance(last.get('cat_obj'), dict) and last['cat_obj']['dir'] == 'R':
                    is_block = True
            if is_block:
                results.append([dict(x) for x in path])
            return
        for end in range(pos, n):
            entries = list(T[pos][end].values())
            if entries:
                for ent in entries:
                    path.append({'i': pos, 'j': end, 'cat': show_cat(ent['cat']), 'cat_obj': ent['cat'], 'tree': ent['trees'][0] if ent['trees'] else None})
                    find_partials(end + 1, path, results, max_p)
                    path.pop()
                    if len(results) >= max_p:
                        return
            else:
                path.append({'i': pos, 'j': end, 'cat': None, 'cat_obj': None, 'tree': None})
                results.append([dict(x) for x in path])
                path.pop()
                break

    all_partials: list[list[dict[str, Any]]] = []
    find_partials(0, [], all_partials, 1000)
    seen: set[str] = set()
    partials_clean: list[list[dict[str, Any]]] = []
    for p in all_partials:
        if len(p) == 1 and p[0]['i'] == 0 and p[0]['j'] == n-1 and p[0].get('cat'):
            continue
        nulls = [x for x in p if not x.get('cat')]
        if len(nulls) > 1:
            continue
        sig = '|'.join(f"{x['i']}-{x['j']}-{x.get('cat') or 'null'}" for x in p)
        if sig in seen:
            continue
        seen.add(sig)
        partials_clean.append(p)

    rules_attempted = 0
    rules_failed = 0
    failed_pairs: list[dict[str, str]] = []
    for length in range(2, n + 1):
        for i in range(0, n - length + 1):
            j = i + length - 1
            for k in range(i, j):
                for eg in T[i][k].values():
                    for ed in T[k+1][j].values():
                        rules_attempted += 1
                        if not apply_rules(eg['cat'], ed['cat']):
                            rules_failed += 1
                            if len(failed_pairs) < 50:
                                failed_pairs.append({'left': show_cat(eg['cat']), 'right': show_cat(ed['cat']), 'span': f'[{i}-{k}]+[{k+1}-{j}]'})

    def serialize_analysis(t: dict[str, Any], label: str) -> dict[str, Any]:
        return {'label': label, 'tree': t, 'steps': tree_steps(t), 'wordCats': word_cats(t), 'partial': False}

    complete = [serialize_analysis(t, f'Analyse {idx+1}') for idx, t in enumerate(complete_trees)]

    partials = []
    for idx, path in enumerate(partials_clean[:50]):
        serial_path = []
        wc: dict[str, str] = {}
        steps: list[dict[str, Any]] = []
        for item in path:
            tree = item.get('tree')
            if tree:
                wc.update(word_cats(tree))
                steps.extend(tree_steps(tree))
            serial_path.append({k: v for k, v in item.items() if k != 'cat_obj'})
        partials.append({'label': f'Blocage {idx+1}', 'path': serial_path, 'steps': steps, 'wordCats': wc, 'partial': True})

    # Compter les vraies impasses sans limite pour affichage correct
    all_impasses_count: list[list[dict[str, Any]]] = []
    find_partials(0, [], all_impasses_count, 999999)
    seen_count: set[str] = set()
    true_impasse_count = 0
    for p in all_impasses_count:
        if len(p) == 1 and p[0]['i'] == 0 and p[0]['j'] == n-1 and p[0].get('cat'):
            continue
        nulls = [x for x in p if not x.get('cat')]
        if len(nulls) > 1:
            continue
        sig = '|'.join(f"{x['i']}-{x['j']}-{x.get('cat') or 'null'}" for x in p)
        if sig in seen_count:
            continue
        seen_count.add(sig)
        true_impasse_count += 1

    return {
        'mots': mots,
        'complete': complete,
        'partials': partials,
        'metrics': {
            'successes': len(complete_trees),
            'impasses': true_impasse_count,
            'rulesAttempted': rules_attempted,
            'rulesFailed': rules_failed,
            'failedPairs': failed_pairs,
        },
        'lexique': {w: [show_cat(c) for c in cats] for w, cats in lexique.items()},
    }
