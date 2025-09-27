import React, {useState} from 'react';
import { createCandidate } from '../api';

export default function CandidateForm(){
  const [first, setFirst] = useState('');
  const [last, setLast] = useState('');
  const [email, setEmail] = useState('');
  const [whatsapp, setWhatsapp] = useState('');
  const [objective, setObjective] = useState('');
  const [diploma, setDiploma] = useState('');
  const [files, setFiles] = useState({});
  const [progress, setProgress] = useState(0);
  const [message, setMessage] = useState('');

  function validateEmail(e){ return /\S+@\S+\.\S+/.test(e); }

  const submit = async (e) => {
    e.preventDefault();
    if(!first || !last || !email || !validateEmail(email)){ setMessage('Vérifie les champs obligatoires et l\'email'); return; }
    const form = new FormData();
    form.append('first_name', first);
    form.append('last_name', last);
    form.append('email', email);
    form.append('whatsapp', whatsapp);
    form.append('objective', objective);
    form.append('diploma', diploma);
    if(files.id_card) form.append('id_card', files.id_card);
    if(files.passport) form.append('passport', files.passport);
    if(files.diploma_file) form.append('diploma_file', files.diploma_file);
    if(files.cv) form.append('cv', files.cv);

    setProgress(0);
    setMessage('Envoi en cours...');
    try {
      const res = await createCandidate(form, (p)=>setProgress(p));
      if(res.status === 201){
        setMessage('Candidature envoyée avec succès !');
        setFirst(''); setLast(''); setEmail(''); setWhatsapp(''); setObjective(''); setDiploma('');
        setFiles({});
      } else {
        setMessage('Erreur: ' + JSON.stringify(res.data));
      }
    } catch(err){
      setMessage('Erreur réseau');
    }
  };

  return (
    <div>
      <h3>Déposer une candidature</h3>
      <form onSubmit={submit}>
        <div className="form-row"><input placeholder="Prénom" value={first} onChange={e=>setFirst(e.target.value)} required/></div>
        <div className="form-row"><input placeholder="Nom" value={last} onChange={e=>setLast(e.target.value)} required/></div>
        <div className="form-row"><input placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} required/></div>
        <div className="form-row"><input placeholder="WhatsApp (ex: whatsapp:+2376...)" value={whatsapp} onChange={e=>setWhatsapp(e.target.value)}/></div>
        <div className="form-row"><input placeholder="Objectif (études, soins...)" value={objective} onChange={e=>setObjective(e.target.value)}/></div>
        <div className="form-row"><input placeholder="Dernier diplôme" value={diploma} onChange={e=>setDiploma(e.target.value)}/></div>

        <hr/>
        <div className="form-row"><label className="small">CNI</label><input type="file" onChange={e=>setFiles({...files, id_card: e.target.files[0]})}/></div>
        <div className="form-row"><label className="small">Passeport</label><input type="file" onChange={e=>setFiles({...files, passport: e.target.files[0]})}/></div>
        <div className="form-row"><label className="small">Diplôme</label><input type="file" onChange={e=>setFiles({...files, diploma_file: e.target.files[0]})}/></div>
        <div className="form-row"><label className="small">CV</label><input type="file" onChange={e=>setFiles({...files, cv: e.target.files[0]})}/></div>

        <div className="form-row"><div className="progress"><span style={{width: progress + '%'}}></span></div></div>
        <button>Envoyer</button>
      </form>
      {message && <p className="small">{message}</p>}
    </div>
  );
}
