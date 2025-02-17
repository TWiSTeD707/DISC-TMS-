import React from 'react';
import { Link } from 'react-router-dom';
import './HomePage.css';

const HomePage = () => {
  return (
    <div className="home-container">
      <header className="header">
        <h1 className="title">Work team</h1>
        <p className="subtitle">ИИ - платформа для формирования команд</p>
      </header>

      <div className="main-content">
        <h2>Создайте эффективную команду с помощью нейросети</h2>
        <p>Автоматическое распределение сотрудников по психотипам</p>

        <div className="buttons-container">
          <Link to="/register/company" className="btn btn-green">
            Войти как компания
          </Link>
          <Link to="/register/employee" className="btn btn-blue">
            Войти как сотрудник
          </Link>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
