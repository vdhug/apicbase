document.addEventListener('DOMContentLoaded', () => {


    document.querySelector('#reset-form').onclick = (e)  => {
        e.preventDefault();

        document.getElementById("form-login").reset();
    };

    document.querySelector('#submit-form').onclick = (e)  => {
        e.preventDefault();
        document.getElementById("form-login").submit();
    };

});
