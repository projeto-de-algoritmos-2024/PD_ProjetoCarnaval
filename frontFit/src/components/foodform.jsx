import React, { useState } from 'react';

function FoodForm({ addFood }) {
  const [nome, setFoodName] = useState('');
  const [calorias, setCalories] = useState('');
  const [nutritivo, setNutritivo] = useState('');
 
  const handleSubmit = (e) => {
    e.preventDefault();
    if (nome && calorias && nutritivo) {
      addFood({
        nome,
        calorias: parseInt(calorias),
        nutritivo: parseFloat(nutritivo),

      });
      setFoodName('');
      setCalories('');
      setNutritivo('');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Adicionar Alimento</h2>
      <input
        type="text"
        placeholder="Nome do alimento"
        value={nome}
        onChange={(e) => setFoodName(e.target.value)}
      />
      <input
        type="number"
        placeholder="Calorias"
        value={calorias}
        onChange={(e) => setCalories(e.target.value)}
      />
      <input
        type="number"
        placeholder="Nutritivo (g)"
        value={nutritivo}
        onChange={(e) => setNutritivo(e.target.value)}
      />
      <button type="submit">Adicionar</button>
    </form>
  );
}

export default FoodForm;
