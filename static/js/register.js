document.querySelectorAll('.form-group input').forEach(input => {
    if (input.name === 'username') input.placeholder = 'Choose a Username';
    if (input.name === 'email') input.placeholder = 'Enter Email Address';
    if (input.name === 'password1') input.placeholder = 'Enter Password';
    if (input.name === 'password2') input.placeholder = 'Confirm Password';
});