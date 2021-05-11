auth.onAuthStateChanged(user => {
    if(user){
        console.log('user logged in: ', user);
    }else{
        console.log('user logged out');
    }
})

const loginForm = document.querySelector('#login-form');
loginForm.addEventListener('submit', (e) => {
    e.preventDefault();

    const email = loginForm['login-email'].value;
    const password = loginForm['login-password'].value;
    console.log(email);
    console.log(password);

    auth.signInWithEmailAndPassword(email, password).then(cred => {
        console.log(cred.user)
        location.replace("../templates/acvlanding.html")

    })
})