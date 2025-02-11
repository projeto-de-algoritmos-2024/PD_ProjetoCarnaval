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

    
if __name__ == '__main__':
    app.run()
