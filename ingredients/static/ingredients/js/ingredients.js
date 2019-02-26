document.addEventListener('DOMContentLoaded', () => {
    // Get template of showing an ingredient to the user to use in the filter call
    const template = Handlebars.compile(document.querySelector('#handlebar-ingredient-show-template').innerHTML);

    let btnReset = document.querySelector('#reset-form')
    if (btnReset) {
      // Add Listener to clear button to reset the informations of the form
      btnReset.onclick = (e)  => {
          e.preventDefault();
          // Get form and reset informations
          document.getElementById("form-ingredient").reset();
      };
    }

    let btnSubmit = document.querySelector('#submit-form');
    if (btnSubmit) {
      btnSubmit// Add Listener to submit button to submit the form
      .onclick = (e)  => {
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
    }

    let btnSearch = document.querySelector('.button-search');
    if (btnSearch) {
      // Add Listener to search button to filter the list of ingredients
      btnSearch.onclick = (e)  => {
          e.preventDefault();
          // Make ajax request
          let filter = document.querySelector('#filter').value;
          $.ajax({
  					url: 'filter',
  					data:{
  						filter: filter,
  					},
  					success: function(data) {
              // Query for list of result
              debugger
              var result = JSON.parse(data)
              var list = document.querySelector(".list-items");
              list.innerHTML = "";
              debugger
              for(var i = 0; i < result.length; i++) {
                debugger
                let ingredient = result[i]['fields'];
                debugger
                let context = {
                  "name": ingredient['name'],
                  "articleNumber": ingredient['article_number'],
                  "baseAmount": ingredient['base_amount'],
                  "unit": ingredient['unit'],
                  "basePrice": ingredient['base_price'],
                }
                let content = template(context);
                list.innerHTML += content;

              }
  					},
  					failure: function(data) {
  						debugger
  					}
  				});
      };
    }

});
