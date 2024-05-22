function validate(){
    let a = document.forms['form']['username'].value;
    let b = document.forms['form']['password'].value;
    let c = document.forms['form']['password1'].value;
    if(b!=c){
        document.getElementById('error').innerHTML = 'password does not match.';
        document.getElementById('error1').innerHTML = '';
        return false;
    }
    else{
        if(b.length<=8){
            document.getElementById('error').innerHTML = 'password must be greater than 8 digits.';
            return false;
        }
        return true;
    }
}