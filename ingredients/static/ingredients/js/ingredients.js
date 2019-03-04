document.addEventListener('DOMContentLoaded', () => {
    // Get template of showing an ingredient to the user to use in the filter call
    let handlebarTemplate = document.querySelector('#handlebar-ingredient-show-template');

    const UNIT_CHOICES = {
      'G': 'Grams',
      'KG': 'Kilograms',
      'CL': 'Centiliters',
      'LT': 'Liters',
  }




    let btnReset = document.querySelector('#reset-form');
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
      // Add Listener to submit button to submit the form
      btnSubmit.onclick = (e)  => {

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
      // Compile Handlebars template
      const template = Handlebars.compile(handlebarTemplate.innerHTML);
      // Add Listener to search button to filter the list of ingredients
      btnSearch.onclick = (e)  => {
          e.preventDefault();

          let loader = document.querySelector('.loader');
          // show loader
          loader.style.display = "block";
          // Make ajax request
          let filter = document.querySelector('#filter').value;


          $.ajax({
  					url: '/ingredients/filter',
  					data:{
  						filter: filter,
  					},
  					success: function(data) {

              // Query for list of result
              var result = JSON.parse(data)
              var list = document.querySelector(".list-items");
              list.innerHTML = "";
              let showMoreButton = document.querySelector('#show-more-button');
              let showMoremessage = document.querySelector('#show-more-message');
              showMoreButton.dataset.page = 1;


              // Check if number of results is less than 2, disable load more
              if (result.length < 5) {
                showMoreButton.style.display = "none";
                showMoremessage.style.display = "block"
              }
              else {
                showMoreButton.style.display = "block";
                showMoremessage.style.display = "none"

              }

              for(var i = 0; i < result.length; i++) {
                let ingredient = result[i]['fields'];
                let obj = result[i]

                let context = {
                  "id": obj.pk,
                  "name": ingredient['name'],
                  "articleNumber": ingredient['article_number'],
                  "baseAmount": ingredient['base_amount'],
                  "unit": UNIT_CHOICES[ingredient['unit']],
                  "basePrice": ingredient['base_price'],
                }
                let content = template(context);
                list.innerHTML += content;

              }
              loader.style.display = "none";
  					},
  					failure: function(data) {

  					}
  				});
      };
    }


    let btnShowMore = document.querySelector('#show-more-button');
    if (btnShowMore) {
      // Add Listener to search button to filter the list of ingredients
      btnShowMore.onclick = (e)  => {
          e.preventDefault();
          const template = Handlebars.compile(handlebarTemplate.innerHTML);
          let loader = document.querySelector('.loader');
          // show loader
          loader.style.display = "block";

          // Make ajax request
          let page = parseInt(event.target.dataset.page);
          $.ajax({
  					url: '/ingredients/show_more',
  					data:{
  						page: page,
  					},
  					success: function(data) {
              debugger
              // Query for list of result
              var result = JSON.parse(data)
              var list = document.querySelector(".list-items");
              let showMoreButton = document.querySelector('#show-more-button');
              let showMoremessage = document.querySelector('#show-more-message');
              // Set the dataset attribute to 5, because it is the first time that the query was executed
              showMoreButton.dataset.page = page+5;

              // Check if number of results is less than 5, disable load more
              if (result.length < 5) {
                showMoreButton.style.display = "none";
                showMoremessage.style.display = "block"
              }
              else {
                showMoreButton.style.display = "block";
                showMoremessage.style.display = "none"

              }

              for(var i = 0; i < result.length; i++) {
                let ingredient = result[i]['fields'];

                let context = {
                  "name": ingredient['name'],
                  "articleNumber": ingredient['article_number'],
                  "baseAmount": ingredient['base_amount'],
                  "unit": UNIT_CHOICES[ingredient['unit']],
                  "basePrice": ingredient['base_price'],
                }
                let content = template(context);
                list.innerHTML += content;
              }

              loader.style.display = "none";
  					},
  					failure: function(data) {

  					}
  				});
      };
    }

});

// Trigger filter event via key enter press in the input
function search() {
    //See notes about 'which' and 'key'
    if (event.keyCode == 13) {
        document.querySelector(".button-search").click();
    }
}
