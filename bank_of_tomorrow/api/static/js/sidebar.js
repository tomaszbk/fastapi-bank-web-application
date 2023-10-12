const apiUrl = '/dashboard';
const bearerToken = localStorage.getItem('access_token');

home = document.getElementById("home_sidebar_button")
home.addEventListener("click", function() {
    window.location.href = `${apiUrl}?token=${bearerToken}`;
})

transaction = document.getElementById("transaction_sidebar_button")
transaction.addEventListener("click", function() {
    window.location.href = `${apiUrl}/transaction?token=${bearerToken}`;
})

profile = document.getElementById("profile_sidebar_button")
profile.addEventListener("click", function() {
    window.location.href = `${apiUrl}/profile?token=${bearerToken}`;
})