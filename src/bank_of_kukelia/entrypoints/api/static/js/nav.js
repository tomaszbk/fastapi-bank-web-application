
function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('username');
    window.location.href = '/';
}

let access_token = localStorage.getItem('access_token');
let username = localStorage.getItem('username');

let nav_options = document.getElementById('nav-options');
// check if user is null
console.log(username== null);
console.log(username);
if (username === null) {
    login_button = document.createElement('div');

    // Set the HTML content using template literals
    login_button.innerHTML = `<a href="/login"><button type="button" class="btn btn-primary">Log in</button></a>`;
    nav_options.appendChild(login_button);
}else{
    user_button = document.createElement('div');
    user_button.innerHTML = `<a href="user"><button type="button" class="btn btn-primary">User</button></a>`;
    dashboard_button = document.createElement('div');
    dashboard_button.innerHTML = `<a href="dashboard"><button type="button" class="btn btn-primary">Dashboard</button></a>`;
    logout_button = document.createElement('div');
    logout_button.innerHTML = `<button type="button" class="btn btn-primary">Log out</button>`;
    logout_button.addEventListener('click', logout);
    nav_options.appendChild(user_button);
    nav_options.appendChild(dashboard_button);
    nav_options.appendChild(logout_button);
}
