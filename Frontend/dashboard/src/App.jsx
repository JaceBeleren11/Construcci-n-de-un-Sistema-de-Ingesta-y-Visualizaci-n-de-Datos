import React, { useEffect, useState } from 'react';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import { Line } from 'react-chartjs-2';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

function App() {
  const [datos, setDatos] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/datos');
        const data = await response.json();
        setDatos(Array.isArray(data) ? data : []);
      } catch (error) {
        console.error("Error al obtener los datos:", error);
      }
    };
    
    fetchData();
    const interval = setInterval(fetchData, 5000); // Actualiza cada 5 segundos
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial' }}>
      <h1>Dashboard - Data Warehouse Moderno</h1>
      <p>Vista de datos en tiempo real y transaccionales.</p>

      <h2>Últimos registros en la base de datos</h2>
      <table border="1" cellPadding="10" style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th>ID</th>
            <th>Origen</th>
            <th>Contenido</th>
            <th>Fecha</th>
          </tr>
        </thead>
        <tbody>
          {datos.slice(0, 10).map((item) => (
            <tr key={item.id}>
              <td>{item.id}</td>
              <td>{item.origen}</td>
              <td>{item.contenido}</td>
              <td>{new Date(item.fecha).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;