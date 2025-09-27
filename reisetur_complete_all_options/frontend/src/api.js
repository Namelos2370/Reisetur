import axios from 'axios';
const API_BASE = process.env.REACT_APP_API_BASE || '';

function getAuthHeaders() {
  const token = localStorage.getItem('access');
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function login(username, password){
  const res = await axios.post(`${API_BASE}/api/token/`, { username, password });
  localStorage.setItem('access', res.data.access);
  localStorage.setItem('refresh', res.data.refresh);
  return res.data;
}

export function logout(){
  localStorage.removeItem('access');
  localStorage.removeItem('refresh');
}

export async function getCandidate(id){
  const res = await axios.get(`${API_BASE}/api/admin/candidates/${id}/`, { headers: getAuthHeaders() });
  return res.data;
}

export async function getMyCandidateList(){
  // staff-only endpoint; for demo we fetch admin list if token present
  const res = await axios.get(`${API_BASE}/api/admin/candidates/`, { headers: getAuthHeaders() });
  return res.data;
}

export async function createCandidate(formData, onUploadProgress){
  // use XMLHttpRequest for better upload progress control
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.open('POST', `${API_BASE}/api/candidates/`);
    xhr.onload = () => {
      try {
        const json = JSON.parse(xhr.responseText);
        resolve({ status: xhr.status, data: json });
      } catch(e){
        resolve({ status: xhr.status, data: xhr.responseText });
      }
    };
    xhr.onerror = () => reject(new Error('Network error'));
    if(onUploadProgress){
      xhr.upload.onprogress = (ev) => {
        if(ev.lengthComputable){
          onUploadProgress(Math.round((ev.loaded / ev.total) * 100));
        }
      };
    }
    xhr.send(formData);
  });
}
