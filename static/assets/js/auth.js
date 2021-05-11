const logout = document.getElementById("logout");
logout.addEventListener('click', (e) => {
    e.preventDefault();
    auth.signOut().then(() => {
        console.log("user signed out");
        location.replace("../login_html/index.html");
    })
})