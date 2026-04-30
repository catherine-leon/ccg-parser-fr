from __future__ import annotations
import time
from flask import Flask, jsonify, render_template, request
from parser import EXAMPLES, LEXIQUE_RAW, parse

app = Flask(__name__)

@app.get('/')
def index():
    return render_template('index.html')

@app.get('/api/lexique')
def api_lexique():
    return jsonify({'lexique': LEXIQUE_RAW, 'examples': EXAMPLES})

@app.post('/api/parse')
def api_parse():
    data = request.get_json(silent=True) or {}
    phrase = (data.get('phrase') or '').strip()
    type_raise = bool(data.get('typeRaise', True))
    max_trees = int(data.get('maxTrees', 20))
    extra_lexique = data.get('extraLexique') or {}
    t0 = time.perf_counter()
    result = parse(phrase, type_raise=type_raise, max_trees=max_trees, extra_lexique=extra_lexique)
    result['elapsedMs'] = round((time.perf_counter() - t0) * 1000, 2)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
