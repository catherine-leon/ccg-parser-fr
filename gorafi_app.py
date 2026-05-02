from __future__ import annotations
import time
from flask import Flask, jsonify, render_template, request
from parser import LEXIQUE_RAW, parse
from gorafi_lexique import GORAFI_LEXIQUE_RAW, GORAFI_EXAMPLES

app = Flask(__name__)

# Lexique combiné: base + Gorafi
GORAFI_FULL_LEXIQUE = {**LEXIQUE_RAW, **GORAFI_LEXIQUE_RAW}

@app.get('/')
def index():
    return render_template('gorafi.html')

@app.get('/api/lexique')
def api_lexique():
    return jsonify({'lexique': GORAFI_FULL_LEXIQUE, 'examples': GORAFI_EXAMPLES})

@app.post('/api/parse')
def api_parse():
    data = request.get_json(silent=True) or {}
    phrase = (data.get('phrase') or '').strip()
    type_raise = bool(data.get('typeRaise', True))
    max_trees = int(data.get('maxTrees', 999))
    extra_lexique = data.get('extraLexique') or {}
    # Merge: base + gorafi + extra
    full_extra = {**GORAFI_LEXIQUE_RAW, **extra_lexique}
    t0 = time.perf_counter()
    result = parse(phrase, type_raise=type_raise, max_trees=max_trees, extra_lexique=full_extra)
    result['elapsedMs'] = round((time.perf_counter() - t0) * 1000, 2)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
