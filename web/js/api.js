//API URL
const API_URL = 'http://127.0.0.1:8000'

async function apiFetch(endpoint, options = {}){
    const token = getToken();


    const headers={
        'Content-Type': 'application/json',
        ...(token ? {'Authorization':'Bearer ' + token} : {}),
        ...(options.headers || {})
    };

    const response = await fetch(API_URL + endpoint, {
        ...options,
        headers
    });

    if(response.status === 401){
        logout();
        return null;
    }

    if(response.status === 404){
        throw new Error('Not Found (404)');
    }

    if(response.status === 500){
        throw new Error('Server Error (500), check API is running');
    }

    if(!response.ok){
        const err = await response.json().catch(() =>({}));
        throw new Error(err.detail || 'Something went wrong'); 
    }

    const text = await response.text();
    return text ? JSON.parse(text) : null;
}