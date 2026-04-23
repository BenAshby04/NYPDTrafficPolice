// show a red error message underneath a field
function showError(fieldId, message){
    const field = document.getElementById(fieldId);
    if(!field) return;

    clearError(fieldId);

    const err = document.createElement('span');
    err.className = 'field-error';
    err.textContent = message;

    field.parentElement.appendChild(err);
    field.classList.add('input-error');
}

function clearError(fieldId){
    const field = document.getElementById(fieldId);
    if(!field) return;

    const err = field.parentElement.querySelector('.field-error');
    if(err) err.remove();
    field.classList.remove('input-error');
}

function validateEmail(email){
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function validatePassword(password){
    return /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/.test(password);
}

function validateRequired(value){
    return value !== null && value !== undefined && value.toString().trim() !== '';
}

function validateNumber(value){
    return !isNaN(value) && parseFloat(value) > 0;
}

function validatePastDate(dataStr){
    return new Date(dateStr) <= new Date();
}