// Save the token after someone logs in
function saveToken(token){
    sessionStorage.setItem('jwt', token);
}

// Get the saved token for api calls
function getToken(){
    return sessionStorage.getItem('jwt');
}

// Check if user is logged in
function isLoggedIn(){
    return getToken() !== null;
}

// Get the user's role
function getUserRole(){
    return sessionStorage.getItem('userRole');
}
// Log the user out and return to homepage
function logout(){
    sessionStorage.clear();
    window.location.href = '../index.html';
}

// If the user is not logged in send them to the login page
function requireLogin(loginPage){
    if(!isLoggedIn()){
        window.location.href = loginPage;
    }
}

// If the user has the wrong role kick them out
function requireRole(role){
    if(getUserRole() !== role){
        alert("Acess denied you dont have permission for this page!");
        logout();
    }
}