import React from 'react';

export default function App() {
  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>Solitario - Proyecto Python</h1>
      <p>Este proyecto es un juego de Solitario desarrollado en Python con Flask.</p>
      <h2>Para ejecutar el juego:</h2>
      <ol>
        <li>Instalar dependencias: <code>pip install -r requirements.txt</code></li>
        <li>Ejecutar servidor: <code>python -m backend.main</code></li>
        <li>Abrir: <code>http://localhost:5000</code></li>
      </ol>
      <p>Ver README.md para más información.</p>
    </div>
  );
}
