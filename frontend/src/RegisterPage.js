import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './RegisterPage.css';

const RegisterPage = ({ match }) => {
  const [role, setRole] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const history = useNavigate();

  const handleSubmit = () => {
    console.log(`Role: ${role}, Username: ${username}, Password: ${password}`);
    history.push(`/profile/${role}`);
  };

  return (
    <div className="register-container">
      <header className="header">
        <h1 className="title">Регистрация</h1>
        <p className="subtitle">Пожалуйста, выберите вашу роль</p>
      </header>

      <div className="form-container">
        <div className="role-selection">
          <button
            className={role === 'company' ? 'active' : ''}
            onClick={() => setRole('company')}
          >
            Компания
          </button>
          <button
            className={role === 'employee' ? 'active' : ''}
            onClick={() => setRole('employee')}
          >
            Сотрудник
          </button>
        </div>

        <input
          type="text"
          placeholder="Имя пользователя"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Пароль"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button className="btn-submit" onClick={handleSubmit}>
          Зарегистрироваться
        </button>
      </div>
    </div>
  );
};

export default RegisterPage;
