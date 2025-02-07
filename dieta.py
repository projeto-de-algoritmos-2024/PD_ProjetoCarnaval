from flask import Flask, request,jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

alimentos = [
    {"nome": "Maçã", "calorias": 52, "nutritivo": 8},
    {"nome": "Brócolis", "calorias": 55, "nutritivo": 10}, {"nome": "Salmão", "calorias": 208, "nutritivo": 10},
    {"nome": "Aveia", "calorias": 68, "nutritivo": 9},
    {"nome": "Quinoa", "calorias": 120, "nutritivo": 9},
    {"nome": "Iogurte Natural", "calorias": 59, "nutritivo": 8},
    {"nome": "Amêndoas", "calorias": 576, "nutritivo": 9},
    {"nome": "Espinafre", "calorias": 23, "nutritivo": 10},
    {"nome": "Batata Doce", "calorias": 86, "nutritivo": 8},
    {"nome": "Frango Grelhado", "calorias": 165, "nutritivo": 9},
    {"nome": "Refrigerante", "calorias": 150, "nutritivo": 2},
    {"nome": "Batata Frita", "calorias": 312, "nutritivo": 3},
    {"nome": "Hambúrguer", "calorias": 295, "nutritivo": 4},
    {"nome": "Pizza", "calorias": 266, "nutritivo": 4},
    {"nome": "Sorvete", "calorias": 207, "nutritivo": 3},
    {"nome": "Chocolate", "calorias": 535, "nutritivo": 5},
    {"nome": "Salgadinho", "calorias": 550, "nutritivo": 2},
    {"nome": "Donuts", "calorias": 452, "nutritivo": 3},
    {"nome": "Macarrão Instantâneo", "calorias": 400, "nutritivo": 2},
    {"nome": "Coxinha", "calorias": 280, "nutritivo": 3}
]

@app.route('/dieta', methods=['POST'])
def dieta():
    data = request.get_json()

    calorias = data.get('calorias')

    matriz = [[0 for _ in range(calorias + 1)] for _ in range(len(alimentos) + 1)]

    for i in range(1, len(alimentos) + 1):
        for j in range(1, calorias + 1):
            if alimentos[i - 1]["calorias"] > j:
                matriz[i][j] = matriz[i - 1][j]
            else:
                matriz[i][j] = max(matriz[i - 1][j], alimentos[i - 1]["nutritivo"] + matriz[i - 1][j - alimentos[i - 1]["calorias"]])

    j = calorias
    alimentos_usados = []
    for i in range(len(alimentos), 0, -1):
        if matriz[i][j] != matriz[i - 1][j]:
            alimentos_usados.append(alimentos[i - 1])
            j -= alimentos[i - 1]["calorias"]

    return jsonify(alimentos_usados)

@app.route('/disponiveis', methods=['GET'])
def lista():
    return jsonify(alimentos)

@app.route('/alimento', methods=['POST'])
def alimento():
    comida = request.get_json()
    alimentos.append(comida)
    return jsonify({"message": "Alimento adicionado com sucesso!"}), 201

@app.route('/delete', methods=['DELETE'])
def delete():
    global alimentos
    data = request.get_json()

    remove = data.get('nome')

    alimentos = [d for d in alimentos if d["nome"] != remove]
    return jsonify({"message": "Alimento deletado com sucesso!"}), 201

if __name__ == '__main__':
    app.run()
