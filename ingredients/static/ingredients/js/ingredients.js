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
        // Get form
        let form = document.getElementById("form-ingredient");

        // Get form children elements
        let form_childrens = document.getElementById("form-ingredient").children;

        // Loop through all the children elements
        for (i=0; i<form_childrens.length; i++) {
          // Check if the element is an input element
          let isInput = form_childrens[i] instanceof HTMLInputElement;
          if (isInput) {
            let inputElement = form_childrens[i];
            // Check if the input element is valid
            if (!inputElement.checkValidity()) {
              // If input element is not valid, write a error message in the screen to the user.
              document.querySelector('.error-message').innerHTML = inputElement.dataset.name +": "+ inputElement.validationMessage;
              inputElement.focus();
              return false;
            }

            if (inputElement.type === "number"){
              // Get numbers and format to two decimal places
              let number = parseFloat(inputElement.value)
              inputElement.value = number.toFixed(2);
            }
          }

          // Check if the element is an select element
          let isSelect = form_childrens[i] instanceof HTMLSelectElement;
          if(isSelect) {
            // Check if the value from the select is valid
            let selectElement = form_childrens[i];
            if (selectElement.value === "") {
              // If select element is not valid, write a error message in the screen to the user.
              document.querySelector('.error-message').innerHTML = "Select a unit please";
              selectElement.focus();
              return false;
            }
          }
        }

        form.submit();
    };

});
