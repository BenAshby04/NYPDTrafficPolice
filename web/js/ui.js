function showLoading(buttonId){
    const btn = document.getElementById(buttonId);
    if (!btn) return;
    btn.disabled = true;
    btn.dataset.original = btn.textContent;
    btn.textContent = 'Loading...';
}

function hideLoading(buttonId){
    const btn = document.getElementById(buttonId);
    if (!btn) return;
    btn.disabled = false;
    btn.textContent = btn.dataset.original || 'Submit';
}

function showToast(message, type){
    type = type || 'success';

    const existing = document.querySelector('.toast');
    if(existing) existing.remove();

    const toast = document.createElement('div');
    toast.className = 'toast toast-' + type;
    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(function(){
        toast.style.opacity = '0';
        setTimeout(function(){toast.remove;}, 300);
    }, 3000);
}