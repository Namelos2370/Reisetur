import React, {useEffect, useState} from 'react';
import { getMyCandidateList } from '../api';

export default function Dashboard(){
  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(()=>{
    async function load(){
      try {
        const data = await getMyCandidateList();
        setCandidates(data);
      } catch(err){
        setError('Impossible de charger les candidats. Vérifie ton token.');
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  return (
    <div>
      <h3>Dashboard - Staff</h3>
      {loading && <p className="small">Chargement...</p>}
      {error && <p className="small" style={{color:'red'}}>{error}</p>}
      {!loading && !error && (
        <table style={{width:'100%', borderCollapse:'collapse'}}>
          <thead><tr><th>Nom</th><th>Email</th><th>Objectif</th><th>Statut</th><th>Soumis le</th></tr></thead>
          <tbody>
            {candidates.map(c=>(
              <tr key={c.id} style={{borderTop:'1px solid #eef2ff'}}>
                <td>{c.first_name} {c.last_name}</td>
                <td>{c.email}</td>
                <td className="small">{c.objective}</td>
                <td>{c.status}</td>
                <td className="small">{c.created_at}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
