import React, { useState } from 'react';
import CalorieTracker from './components/calorieTracker.jsx';
import Calendar from './components/agenda.jsx'; 

function App() {
  const [activeTab, setActiveTab] = useState('calories');

  return (
    <div className="App">
      <div className="tabs">
        <button onClick={() => setActiveTab('calories')} className={`tab-button ${activeTab === 'calories' ? 'active' : ''}`}>
          Alimentação
        </button>
        <button onClick={() => setActiveTab('agenda')} className={`tab-button ${activeTab === 'agenda' ? 'active' : ''}`}>
          Agenda
        </button>
      </div>

      <div className="tab-content">
        {activeTab === 'calories' ? (
          <CalorieTracker />
        ) : (
          <Calendar />
        )}
      </div>
    </div>
  );
}

export default App;

