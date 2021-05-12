const signUpForm = document.getElementById('signup-form');
document.getElementById("signupbtn").addEventListener("click", function() {
    const email = document.getElementById("Semail").value;
    const firstName = document.getElementById("fname").value;
    const lastName = document.getElementById("lname").value;
    const password = document.getElementById("Spassword").value;
    const conpassword = document.getElementById("Spassword_confirmation").value;
    const phone = document.getElementById("Scell").value;

    if(password != conpassword){
        window.alert("Passwords do not match");
        return;
    }



    auth.createUserWithEmailAndPassword(email, password).then(cred => {
        return db.collection('users').doc(cred.user.uid).set({
            fname:firstName,
            lname: lastName,
            email:email,
            password:password,
            phone:phone
        });
    }).then(() => {
        $('#loginModal').modal('hide');
    })
    .catch(function(error) {
        console.log("Login Failed!", error);
        window.alert("User already exists", error);
    });
});

const loginForm = document.getElementById('login-form');
document.getElementById("loginbtn").addEventListener("click", function() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    auth.signInWithEmailAndPassword(email, password).then(cred => {
        console.log(cred.user);
        $('#loginModal').modal('hide');
        loginForm.reset();
    })
    .catch(error => {
        switch (error.code) {
           case 'auth/email-already-in-use':
             console.log(`Email address ${this.state.email} already in use.`);
             window.alert("Email address ${this.state.email} already in use.", error);
             break;
           case 'auth/invalid-email':
             console.log(`Email address ${this.state.email} is invalid.`);
             window.alert("Email address ${this.state.email} is invalid.", error);
             
             break;
           case 'auth/operation-not-allowed':
             console.log(`Error during sign up.`);
             break;
           case 'auth/weak-password':
             console.log('Password is not strong enough. Add additional characters including special characters and numbers.');
             window.alert("Password is not strong enough. Add additional characters including special characters and numbers.", error);
             break;
           default:
             console.log(error.message);
             break;
         }
        });
});


$(function () {
    $('#signupbtn').attr('disabled', true);
    $('#Spassword_confirmation').change(function () {
        if ($('#fname').val() != '' && $('#lnanme').val() != '' && $('#Semail').val() != '' && $('#Scell').val() != '' && $('#Spassword').val() != '' && $('#Spassword_confirmation').val() != '') {
            $('#signupbtn').attr('disabled', false);
        } else {
            $('#signupbtn').attr('disabled', true);
        }
    });
 });
