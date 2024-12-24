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