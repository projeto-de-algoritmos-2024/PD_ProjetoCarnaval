import React, { useState } from 'react';
import axios from 'axios';
import FoodForm from './foodform.jsx';

function CalorieTracker() {
    const [calorias, setCalorias] = useState('');
    const [totalCalories, setTotalCalories] = useState(0);
    const [foods, setFoods] = useState([]);
    const [responseData, setResponseData] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (calorias) {
            try {

                const response = await axios.post("http://localhost:5000/dieta",
                    { calorias: parseInt(calorias) }, 
                    { headers: { 'Content-Type': 'application/json' } } 
                );

                setResponseData(response.data);
                console.log(response.data);
                setCalorias('');
            } catch (error) {
                console.error("Erro:", error);
            }
        }
    };

    const sendFoodList = async () => {
        try {
            const response = await axios.post("http://localhost:5000/alimento", 
                {alimentos: foods},
                { headers: { 'Content-Type': 'application/json' } } 

            );

            //setResponseData(response.data);
        } catch (error) {
            console.error("Erro:", error);
        }
    };

    const addFood = (food) => {
        setFoods([...foods, food]);
        setTotalCalories(prevTotal => prevTotal + food.calories);
    };

    return (
        <div>
            <h1>Informe as Calorias totais diárias</h1>
            <h3>Calorias Totais: {totalCalories.toFixed(2)} kcal</h3>

            <form onSubmit={handleSubmit}>
                <input
                    type="number"
                    placeholder="calorias (Kcal)"
                    value={calorias}
                    onChange={(e) => setCalorias(e.target.value)}
                />
                <button type="submit">Enviar Calorias</button>
            </form>

            <FoodForm addFood={addFood} />

            <div>
                <h3>Lista de Alimentos:</h3>
                <ul>
                    {foods.map((food, index) => (
                        <li key={index}>
                            <strong>{food.nome}</strong> - {food.calorias} kcal, {food.nutritivo}g Nutritivo
                        </li>
                    ))}
                </ul>
                <button onClick={sendFoodList}>Enviar Lista de Alimentos</button>
            </div>

            {responseData && (
                <div>
                    <h3>Resposta do Backend:</h3>
                    <ul>
                        {responseData.map((item, index) => (
                            <li key={index}>
                                <strong>{item.nome}</strong> - {item.calorias} calorias, Nutritivo: {item.nutritivo}/10
                            </li>
                        ))}
                    </ul>
                </div>
            )}

        </div>
    );
}

export default CalorieTracker;
