const UNIT_CHOICES = {
  'G': 'Grams',
  'KG': 'Kilograms',
  'CL': 'Centiliters',
  'LT': 'Liters',
}
document.addEventListener('DOMContentLoaded', () => {
    // Retrieve and compile Handlebars template

    const template = document.querySelector('#handlebar-ingredient-template');



    if(template) {
       const compiledTemplate = Handlebars.compile(template.innerHTML);
       // Add Listener to button to create a new ingrediento model to recipe
       document.querySelector('#new-ingredient').onclick = (e)  => {
           e.preventDefault();
           // Creating the html text from handlebars template
           let content = compiledTemplate();
           // Append the new recipe element to DOM.
           let li = document.createElement('li');
           li.innerHTML = content.trim();
           document.querySelector('#ingredients').appendChild(li);
       };
    }


    let btnReset = document.querySelector('#reset-form');
    if (btnReset) {
      // Add Listener to clear button to reset the informations of the form
      btnReset.onclick = (e)  => {
          e.preventDefault();
          // Get form and reset informations
          document.getElementById("form-recipe").reset();
      };
    }

    let btnSubmit = document.querySelector('#submit-form');
    if(btnSubmit) {
      // Add Listener to submit button to submit the form
      btnSubmit.onclick = (e)  => {
          e.preventDefault();
          // Get form
          let form = document.getElementById("form-recipe");

          // Get form children elements
          let form_childrens = document.getElementById("form-recipe").children[1].children;
          let INGREDIENTS = []
          // Loop through all the children elements
          for (i=0; i<form_childrens.length; i++) {
            // Check if the element is an input element
            let isInput = form_childrens[i] instanceof HTMLInputElement || form_childrens[i] instanceof HTMLTextAreaElement;
            if (isInput) {

              let inputElement = form_childrens[i];
              // Check if the input element is valid
              if (!inputElement.checkValidity()) {
                // If input element is not valid, write a error message in the screen to the user.
                document.querySelector('.error-message').innerHTML = inputElement.dataset.name +": "+ inputElement.validationMessage;
                inputElement.focus();
                return false;
              }
            }

            let isIngredient = form_childrens[i] instanceof HTMLDivElement
            if(isIngredient) {
              // Get list of ingredients
              let list_ingredients = form_childrens[i].children[1].children;

              // Check if ingredients inputs are correct
              for(j=0; j<list_ingredients.length; j++){
                // Get all the ingredients inputs from each ingredient in the list
                let ingredientFields = list_ingredients[j].children
                // Loop through all the input elements from ingredient
                for(k=0; k<ingredientFields.length; k++){
                  isInput = ingredientFields[k] instanceof HTMLInputElement;
                  if(isInput) {
                    inputElement = ingredientFields[k];
                    if (!inputElement.checkValidity()) {
                      // If input element is not valid, write a error message in the screen to the user.
                      document.querySelector('.error-message').innerHTML = inputElement.dataset.name +": "+ inputElement.validationMessage;
                      inputElement.focus();
                      return false;
                    }
                    else {
                      // Check for duplicated ingredients
                      if (inputElement.value !== "") {
                        if(INGREDIENTS.includes(inputElement.value)){
                          document.querySelector('.error-message').innerHTML = "The ingredient with article number ("+inputElement.value+") is duplicated.";
                          inputElement.focus();
                          return false;
                        }
                        else {
                          INGREDIENTS.push(inputElement.value)
                        }
                      }
                    }

                    // Format quantity to two decimal places
                    if (inputElement.type === "number"){
                      // Get numbers and format to two decimal places
                      let number = parseFloat(inputElement.value)
                      inputElement.value = number.toFixed(2);
                    }
                  }
                }
              }
            }
          }
          // Submit the form
          form.submit();
      };
    }

});

function removeRecipe() {
    event.preventDefault();
    event.target.parentElement.remove();
}


var INGREDIENT_PARENT;
function getIngredient() {
   let articleNumber = event.target.value;
   INGREDIENT_PARENT = event.target.parentElement.children;
   $.ajax({
     url: 'ingredients/get/'+articleNumber,
     success: function(data) {
       // Checks if a ingredient was found
       if(data.result){

         var result = JSON.parse(data.object);
         let obj = result[0]['fields']
         INGREDIENT_PARENT[2].value = obj.name;
         let number = 1
         INGREDIENT_PARENT[3].value = number.toFixed(2);
         debugger
         INGREDIENT_PARENT[4].value = UNIT_CHOICES[obj.unit];
         debugger
       }
     },
     failure: function(data) {

     }
   });
}
