from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app)

# Carregar dados do CSV
df = pd.read_csv('operadoras.csv')

@app.route('/search', methods=['GET'])
def buscar_operadoras():
    query = request.args.get('query', '').lower()
    
    if not query:
        return jsonify({
            'total': 0,
            'resultados': []
        }), 400
    
    # Busca textual em todas as colunas
    resultados = df[
        df.apply(
            lambda row: row.astype(str).str.lower().str.contains(query).any(), 
            axis=1
        )
    ]
    
    # Calcular relevância 
    def calcular_relevancia(row):
        return sum(
            query in str(valor).lower() 
            for valor in row.values
        )
    
    resultados['relevancia'] = resultados.apply(calcular_relevancia, axis=1)
    
    # Ordenar por relevância
    resultados_ordenados = resultados.sort_values('relevancia', ascending=False)
    
    # Converter para lista de dicionários
    resultados_json = resultados_ordenados.to_dict('records')
    
    return jsonify({
        'total': len(resultados_json),
        'resultados': resultados_json
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)