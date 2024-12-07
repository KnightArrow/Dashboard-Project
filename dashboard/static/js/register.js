const usernameField=document.getElementById('usernameField');
const feedBackArea=document.querySelector('.invalid-feedback');
usernameField.addEventListener('keyup',(e)=>{
    console.log("7777");
    const usernameVal=e.target.value;
    usernameField.classList.remove("is-invalid");  //Remove the is-invalid we the error is removed
    feedBackArea.style.display="none";
    if(usernameVal.length>0){
        fetch('/authentication/validate-username',{
            body:JSON.stringify({username:usernameVal}),
            method:"POST",
        }).then(
            response=>response.json()
        ).then(
            data=>{                 //Processing the data converted to json
                console.log("data",data);
                if(data.username_error){
                    usernameField.classList.add("is-invalid");
                    feedBackArea.textContent=data.username_error;
                    feedBackArea.style.display="block";
                }
            }
        );
    }
});
const emailField=document.getElementById('emailField');
emailField.addEventListener('keyup',(e)=>{
    console.log("Working on Email");
    const emailVal=e.target.value;
    emailField.classList.remove("is-invalid");
    feedBackArea.style.display="none";
    if(emailVal.length>0){
        fetch('/authentication/validate-email',{
            body:JSON.stringify({email:emailVal}),
            method:"POST",
        }).then(response=>response.json()).then(
            data=>{
                console.log("Email data",data);
                if(emailField.email_error){
                    emailField.classList.add("is-invalid");
                    feedBackArea.textContent=data.email_error;
                    feedBackArea.style.display="block";
                }
            }
        );
    }
});
console.log("register working")
function togglePasswordVisibility() {
    const passwordField = document.getElementById('passwordField');
    const smallText = document.querySelector('.form-group small');
    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        smallText.textContent = 'Hide';
    } else {
        passwordField.type = 'password';
        smallText.textContent = 'Show';
    }
}