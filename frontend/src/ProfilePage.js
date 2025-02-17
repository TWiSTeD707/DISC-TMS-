import React, { useEffect, useState } from 'react';
import './ProfilePage.css';

const ProfilePage = ({ match }) => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Здесь нужно сделать запрос к API для получения данных пользователя
    setUser({
      username: 'Employee1',
      email: 'employee@example.com',
    });
  }, []);

  if (!user) return <div>Загрузка...</div>;

  return (
    <div className="profile-container">
      <header className="header">
        <h1 className="title">Профиль сотрудника</h1>
      </header>

      <div className="profile-details">
        <p><strong>Имя пользователя:</strong> {user.username}</p>
        <p><strong>Email:</strong> {user.email}</p>
      </div>
    </div>
  );
};

export default ProfilePage;
