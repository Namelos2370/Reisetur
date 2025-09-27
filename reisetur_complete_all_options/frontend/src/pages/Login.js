import React, {useState} from 'react';
import { login } from '../api';
import { useNavigate } from 'react-router-dom';

export default function Login(){
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const nav = useNavigate();

  const submit = async (e) => {
    e.preventDefault();
    try {
      await login(username, password);
      nav('/dashboard');
    } catch(err){
      setError('Identifiants invalides');
    }
  };

  return (
    <div>
      <h3>Connexion - Staff</h3>
      <form onSubmit={submit}>
        <div className="form-row"><input placeholder="Email" value={username} onChange={e=>setUsername(e.target.value)} required/></div>
        <div className="form-row"><input type="password" placeholder="Mot de passe" value={password} onChange={e=>setPassword(e.target.value)} required/></div>
        <button>Se connecter</button>
        {error && <p className="small" style={{color:'red'}}>{error}</p>}
      </form>
    </div>
  );
}
