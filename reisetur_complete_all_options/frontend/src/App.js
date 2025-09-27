import React, {useState, useEffect} from 'react';

function App(){
  const [mode, setMode] = useState('form'); // form | dashboard
  const [firstName,setFirstName] = useState('');
  const [lastName,setLastName] = useState('');
  const [email,setEmail] = useState('');
  const [objective,setObjective] = useState('');
  const [message,setMessage] = useState('');
  const [token,setToken] = useState(localStorage.getItem('reisetur_token') || '');
  const [candidate,setCandidate] = useState(null);
  const [uploadProgress,setUploadProgress] = useState(0);

  useEffect(()=>{
    if(token){
      fetch(`/api/self/${token}/`).then(r=>{
        if(r.ok) return r.json();
        throw new Error('Not found');
      }).then(data=>{
        setCandidate(data);
        setMode('dashboard');
      }).catch(()=>{ localStorage.removeItem('reisetur_token'); setToken(''); });
    }
  },[]);

  const submit = async (e) => {
    e.preventDefault();
    // client-side validation
    if(!firstName || !lastName || !email) { setMessage('Veuillez remplir les champs obligatoires'); return; }
    const form = new FormData();
    form.append('first_name', firstName);
    form.append('last_name', lastName);
    form.append('email', email);
    form.append('objective', objective);
    // use XHR for progress
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/candidates/');
    xhr.onload = function(){
      if(xhr.status === 201){
        const resp = JSON.parse(xhr.responseText);
        setMessage('Candidature envoyée. Conservez votre code d\'accès pour suivre le dossier.');
        const t = resp.access_token || resp.accessToken || null;
        if(t){
          localStorage.setItem('reisetur_token', t);
          setToken(t);
          setCandidate(resp);
          setMode('dashboard');
        }
      } else {
        setMessage('Erreur lors de l\'envoi.');
      }
    };
    xhr.upload.onprogress = function(e){
      if(e.lengthComputable){
        const pct = Math.round((e.loaded / e.total) * 100);
        setUploadProgress(pct);
      }
    };
    xhr.send(form);
  };

  const fetchCandidate = async () => {
    if(!token) return;
    const res = await fetch(`/api/self/${token}/`);
    if(res.ok){
      const data = await res.json();
      setCandidate(data);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('reisetur_token');
    setToken('');
    setCandidate(null);
    setMode('form');
  };

  if(mode === 'dashboard' && candidate){
    return (
      <div style={{maxWidth:800, margin:'40px auto', fontFamily:'Arial, sans-serif'}}>
        <h2>Suivi de candidature</h2>
        <p>Bonjour {candidate.first_name} {candidate.last_name}</p>
        <p><strong>Statut:</strong> {candidate.status}</p>
        <p><strong>Objectif:</strong> {candidate.objective}</p>
        <p><strong>Dernière mise à jour:</strong> {candidate.created_at}</p>
        <button onClick={fetchCandidate}>Rafraîchir</button>
        <button onClick={handleLogout} style={{marginLeft:10}}>Se déconnecter</button>
      </div>
    );
  }

  return (
    <div style={{maxWidth:800, margin:'40px auto', fontFamily:'Arial, sans-serif'}}>
      <h2>Déposer ma candidature - Reisetür</h2>
      <form onSubmit={submit}>
        <div><input placeholder="Prénom" value={firstName} onChange={e=>setFirstName(e.target.value)} required/></div>
        <div><input placeholder="Nom" value={lastName} onChange={e=>setLastName(e.target.value)} required/></div>
        <div><input placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} required/></div>
        <div><input placeholder="Objectif (ex: études)" value={objective} onChange={e=>setObjective(e.target.value)} /></div>
        <div style={{marginTop:10}}>
          <button type="submit">Envoyer</button>
        </div>
      </form>
      {uploadProgress>0 && <p>Upload: {uploadProgress}%</p>}
      {message && <p>{message}</p>}
      {token && <p>Vous êtes connecté. <button onClick={()=>setMode('dashboard')}>Aller au tableau de bord</button></p>}
    </div>
  );
}

export default App;
