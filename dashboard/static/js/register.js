const usernameField=document.getElementById('usernameField');
const feedBackArea=document.querySelector('.invalid_feedback');
const emailField=document.getElementById('emailField');
const emailFeedBackArea=document.querySelector('.emailFeedbackArea');
const submitBtn=document.querySelector(".submit-btn");
//username validation
usernameField.addEventListener('keyup',(e)=>{              //Can also use function over here
    const usernameVal=e.target.value;
    usernameField.classList.remove("is-invalid");  //Remove the is-invalid when the error is removed
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
                    submitBtn.disabled=true;
                    usernameField.classList.add("is-invalid");
                    feedBackArea.textContent=data.username_error;
                    feedBackArea.style.display="block";
                }
                else{
                    submitBtn.disabled=false;
                }
            }
        );
    }
});

//email validation
emailField.addEventListener('keyup',(e)=>{                  //Can also use function over here
    console.log("Working on Email");
    const emailVal=e.target.value;
    emailField.classList.remove("is-invalid");
    emailFeedBackArea.style.display="none";
    if(emailVal.length>0){
        fetch('/authentication/validate-email',{
            body:JSON.stringify({email:emailVal}),
            method:"POST",
        }).then(response=>response.json()).then(
            data=>{
                console.log("Email data",data);
                if(data.email_error){
                    submitBtn.disabled=true;
                    emailField.classList.add("is-invalid");
                    emailFeedBackArea.textContent=data.email_error;
                    emailFeedBackArea.style.display="block";
                }
                else{
                    submitBtn.disabled=false;
                }
            }
        );
    }
});
console.log("register working")

//password validation
function togglePasswordVisibility() {                  //Can also use eventListener here
    const passwordField = document.getElementById('passwordField');
    const smallText = document.querySelector('.form-group small');
    if (passwordField.type === 'password') {
        passwordField.type = 'text';         //Can also use setAttribute("type","text");
        smallText.textContent = 'Hide';
    } else {
        passwordField.type = 'password';
        smallText.textContent = 'Show';
    }
}