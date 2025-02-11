from flask import Flask, request,jsonify
from flask_cors import CORS
from bisect import bisect_right
from datetime import datetime

app = Flask(__name__)
CORS(app)

atividades = [
    {"nome": "Estudar matemática", "tempo_minutos": 120, "prioridade": 10, "inicio": "08:00", "fim": "10:00"},
    {"nome": "Fazer exercícios físicos", "tempo_minutos": 60, "prioridade": 9, "inicio": "10:00", "fim": "11:00"},
    {"nome": "Ler um livro", "tempo_minutos": 45, "prioridade": 8, "inicio": "11:00", "fim": "12:00"},
    {"nome": "Responder e-mails", "tempo_minutos": 30, "prioridade": 7, "inicio": "12:00", "fim": "13:00"},
    {"nome": "Cozinhar jantar", "tempo_minutos": 90, "prioridade": 8, "inicio": "13:30", "fim": "15:00"},
    {"nome": "Meditação", "tempo_minutos": 15, "prioridade": 6, "inicio": "15:00", "fim": "15:30"},
    {"nome": "Assistir aula online", "tempo_minutos": 90, "prioridade": 9, "inicio": "15:00", "fim": "17:00"},
    {"nome": "Organizar a mesa de trabalho", "tempo_minutos": 20, "prioridade": 5, "inicio": "17:30", "fim": "17:50"},
    {"nome": "Fazer compras", "tempo_minutos": 60, "prioridade": 7, "inicio": "18:00", "fim": "19:00"},
    {"nome": "Chamar um amigo", "tempo_minutos": 20, "prioridade": 6, "inicio": "19:00", "fim": "19:35"},
    {"nome": "Trabalhar em um projeto pessoal", "tempo_minutos": 120, "prioridade": 9, "inicio": "19:00", "fim": "21:00"},
    {"nome": "Assistir TV", "tempo_minutos": 60, "prioridade": 4, "inicio": "22:00", "fim": "23:00"},
    {"nome": "Jogar videogame", "tempo_minutos": 90, "prioridade": 5, "inicio": "23:00", "fim": "00:00"},
    {"nome": "Limpar a casa", "tempo_minutos": 45, "prioridade": 7, "inicio": "07:00", "fim": "07:00"},
    {"nome": "Planejar a semana", "tempo_minutos": 30, "prioridade": 8, "inicio": "07:00", "fim": "08:00"},
    {"nome": "Academia", "tempo_minutos": 30, "prioridade": 10, "inicio": "06:30", "fim": "07:00"}
]

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



def hora_minuto(time_str):
    h, m = map(int, time_str.split(":"))
    return h * 60 + m

@app.route('/grade', methods=['GET'])
def weighted_interval_scheduling():
    global atividades
    n = len(atividades)

    inicio = [hora_minuto(t["inicio"]) for t in atividades]
    fim = [hora_minuto(t["fim"]) for t in atividades]
    prioridade = [int(t["prioridade"]) for t in atividades]
    nome = [t["nome"] for t in atividades]

    atividades_tratadas = sorted(zip(nome, prioridade, inicio, fim), key=lambda x: x[3])

    nome, prioridade, inicio, fim = zip(*atividades_tratadas)
    
    p = [0] * n
    for i in range(n):
        j = bisect_right(fim, inicio[i]) - 1
        p[i] = j
    
    peso = [0] * (n + 1)
    selecionadas = []
    ultima_fim = -1

    for i in range(1, n + 1):
        if prioridade[i - 1] + peso[p[i - 1] + 1] > peso[i - 1]:
            if inicio[i - 1] >= ultima_fim:
                peso[i] = prioridade[i - 1] + peso[p[i - 1] + 1]
                selecionadas.append({
                    "nome": nome[i - 1],
                    "inicio": f"{inicio[i - 1] // 60:02}:{inicio[i - 1] % 60:02}",
                    "fim": f"{fim[i - 1] // 60:02}:{fim[i - 1] % 60:02}",
                    "prioridade": prioridade[i - 1]
                })
                ultima_fim = fim[i - 1]
        else:
            peso[i] = peso[i - 1]

    return jsonify(selecionadas)

@app.route('/tarefa', methods=['POST'])
def criar_tarefa():
    data = request.get_json()
    tarefas = data.get('atividadesC')
    print(tarefas)

    for tarefa in tarefas:
        print(tarefa)
        atividades.append(tarefa)

    return jsonify({"message": "Tarefa adicionada com sucesso!"}), 200

@app.route('/tarefa', methods=['GET'])
def mostrar_tarefas():
    return jsonify(atividades), 200
 
@app.route('/dieta', methods=['POST'])
def dieta():
    print(alimentos)
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
    return jsonify(alimentos), 200

@app.route('/alimento', methods=['POST'])
def alimento():
    data = request.get_json()
    banquete = data.get('alimentos')

    for comida in banquete:
        alimentos.append(comida)

    return jsonify({"message": "Alimento adicionado com sucesso!"}), 200

@app.route('/delete', methods=['DELETE'])
def delete():
    global alimentos
    data = request.get_json()

    remove = data.get('nome')

    alimentos = [d for d in alimentos if d["nome"] != remove]
    return jsonify({"message": "Alimento deletado com sucesso!"}), 200
   
if __name__ == '__main__':
    app.run()
