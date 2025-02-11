import { useState } from 'react';
import axios from 'axios';
import './agenda.css';

const Calendar = () => {
  const [atividades, setActivities] = useState([]);
  const [newActivity, setNewActivity] = useState({
    nome: '',
    prioridade: 1,
    inicio: 0,
    fim: 0,
  });

  const hours = Array.from({ length: 24 }, (_, i) => `${i}:00`);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewActivity((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!newActivity.nome || !newActivity.prioridade || !newActivity.inicio || !newActivity.fim) {
      alert('Por favor, preencha todos os campos!');
      return;
    }

    const updatedActivity = {
      ...newActivity,
      inicio: `${newActivity.inicio}:00`,
      fim: `${newActivity.fim}:00`,
    };

    setActivities((prev) => [...prev, updatedActivity]);
    setNewActivity({
      nome: '',
      prioridade: 1,
      inicio: 0,
      fim: 0,
    });
  };

  const sendActivitiesToAPI = async () => {
    try {
      const atividadesC = atividades.map((activity) => ({
        ...activity,
        inicio: `${activity.inicio}:00`,
        fim: `${activity.fim}:00`,
      }));
      console.log(atividadesC);
      const response = await axios.post(
        'http://localhost:5000/tarefa',
        { atividadesC },
        { headers: { 'Content-Type': 'application/json' } }
      );
      alert('Atividades enviadas com sucesso!');
      console.log('Atividades enviadas:', atividadesC);
    } catch (error) {
      console.error('Erro ao enviar atividades:', error);
      alert('Erro ao enviar atividades!');
    }
  };

  const fetchCorrectedActivities = async () => {
    try {
      const response = await axios.get('http://localhost:5000/grade');
      setActivities(response.data);
      alert('Atividades corrigidas recebidas!');
    } catch (error) {
      console.error('Erro ao buscar atividades corrigidas:', error);
      alert('Erro ao buscar atividades corrigidas!');
    }
  };

  return (
    <div className="calendar-container">
      <div className="calendar">
        <div className="hours">
          {hours.map((hour, index) => (
            <div key={index} className="hour">
              {hour}
            </div>
          ))}
        </div>
        <div className="activities">
          {atividades.map((activity, index) => (
            <div
              key={index}
              className="activity"
              style={{
                top: `${parseFloat(activity.inicio) * 60}px`, // Convertendo para número inteiro
                height: `${(parseFloat(activity.fim) - parseFloat(activity.inicio)) * 60}px`,
              }}
            >
              <div className="activity-details">
                <div className="activity-name">{activity.nome}</div>
                <div className="activity-time">{`${activity.inicio} - ${activity.fim}`}</div>
                <div className="activity-priority">Prioridade: {activity.prioridade}</div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="form-container">
        <h2>Criar Nova Tarefa</h2>
        <form onSubmit={handleSubmit}>
          <label htmlFor="nome">Nome da Atividade</label>
          <input
            type="text"
            id="nome"
            name="nome"
            value={newActivity.nome}
            onChange={handleInputChange}
            required
          />

          <label htmlFor="prioridade">Prioridade</label>
          <select
            id="prioridade"
            name="prioridade"
            value={newActivity.prioridade}
            onChange={handleInputChange}
            required
          >
            <option value={1}>1 - Baixa</option>
            <option value={2}>2 - Média</option>
            <option value={3}>3 - Alta</option>
          </select>

          <label htmlFor="inicio">Início</label>
          <input
            type="number"
            id="inicio"
            name="inicio"
            value={newActivity.inicio}
            onChange={handleInputChange}
            min="0"
            max="23"
            required
          />

          <label htmlFor="fim">Fim</label>
          <input
            type="number"
            id="fim"
            name="fim"
            value={newActivity.fim}
            onChange={handleInputChange}
            min="0"
            max="23"
            required
          />

          <button type="submit" className="send-button">Criar Atividade</button>
        </form>

        <button onClick={sendActivitiesToAPI} className="send-button">
          Enviar Atividades
        </button>

        <button onClick={fetchCorrectedActivities} className="get-corrected-button">
          Calcular e Mostrar Atividades Corrigidas
        </button>
      </div>
    </div>
  );
};

export default Calendar;

