import React, { useState } from 'react';

function FoodForm({ addFood }) {
  const [foodName, setFoodName] = useState('');
  const [calories, setCalories] = useState('');
  const [protein, setProtein] = useState('');
  const [carbs, setCarbs] = useState('');
  const [fat, setFat] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (foodName && calories && protein && carbs && fat) {
      addFood({
        foodName,
        calories: parseInt(calories),
        protein: parseFloat(protein),
        carbs: parseFloat(carbs),
        fat: parseFloat(fat),
      });
      setFoodName('');
      setCalories('');
      setProtein('');
      setCarbs('');
      setFat('');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Adicionar Alimento</h2>
      <input
        type="text"
        placeholder="Nome do alimento"
        value={foodName}
        onChange={(e) => setFoodName(e.target.value)}
      />
      <input
        type="number"
        placeholder="Calorias"
        value={calories}
        onChange={(e) => setCalories(e.target.value)}
      />
      <input
        type="number"
        placeholder="Proteínas (g)"
        value={protein}
        onChange={(e) => setProtein(e.target.value)}
      />
      <input
        type="number"
        placeholder="Carboidratos (g)"
        value={carbs}
        onChange={(e) => setCarbs(e.target.value)}
      />
      <input
        type="number"
        placeholder="Gorduras (g)"
        value={fat}
        onChange={(e) => setFat(e.target.value)}
      />
      <button type="submit">Adicionar</button>
    </form>
  );
}

export default FoodForm;
