document.addEventListener('DOMContentLoaded', () => {


    // Add Listener to clear button to reset the informations of the form
    document.querySelector('#reset-form').onclick = (e)  => {
        e.preventDefault();
        // Get form and reset informations
        document.getElementById("form-ingredient").reset();
    };

    // Add Listener to submit button to submit the form
    document.querySelector('#submit-form').onclick = (e)  => {
        e.preventDefault();
        // Get form and submit 
        document.getElementById("form-ingredient").submit();
    };
});
