const UNIT_CHOICES = {
  'G': 'Grams',
  'KG': 'Kilograms',
  'CL': 'Centiliters',
  'LT': 'Liters',
  'ML': 'Milliliters',
  'U': 'Unit',
}
document.addEventListener('DOMContentLoaded', () => {
    // Retrieve and compile Handlebars template

    const template = document.querySelector('#handlebar-ingredient-template');
    const handlebarTemplate = document.querySelector('#handlebar-recipe-show-template');



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

    let btnDelete = document.querySelector('#delete-form');
    if (btnDelete) {
      // Add Listener to clear button to reset the informations of the form
      btnDelete.onclick = (e)  => {
          e.preventDefault();
          // Get form and reset informations
          document.getElementById("form-recipe").submit();
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
                      if (inputElement.name == "articleNumber") {
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
  					url: '/recipes/filter',
  					data:{
  						filter: filter,
  					},
  					success: function(data) {

              // Query for list of result
              var list = document.querySelector(".list-items");
              list.innerHTML = "";
              let showMoreButton = document.querySelector('#show-more-button');
              let showMoremessage = document.querySelector('#show-more-message');
              let filter = document.querySelector('#filter').value;
              showMoreButton.dataset.page = 1;


              // Check if number of results is less than 2, disable load more
              if (Object.keys(data).length < 5) {
                showMoreButton.style.display = "none";
                showMoremessage.style.display = "block"
              }
              else {
                showMoreButton.style.display = "block";
                showMoremessage.style.display = "none"

              }

              for(var i = 0; i < Object.keys(data).length; i++) {

                let recipe_cost = data[i][1];

                let recipe = JSON.parse(data[i][0]);
                let id = recipe[0].pk;

                let context = {
                  "id": id,
                  "name": recipe[0]['fields']['name'],
                  "description": recipe[0]['fields']['description'],
                  "cost": recipe_cost,
                }
                let content = template(context);
                list.innerHTML += content;

              }

              // hide loader
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
              const template = Handlebars.compile(handlebarTemplate.innerHTML);
              e.preventDefault();
              let loader = document.querySelector('.loader');
              // show loader
              loader.style.display = "block";
              // Make ajax request
              let inicio = parseInt(event.target.dataset.inicio);
              let final = parseInt(event.target.dataset.final);
              $.ajax({
      					url: '/recipes/show_more',
      					data:{
      						inicio: inicio,
      						final: final,
      					},
      					success: function(data) {

                  // Query for list of result
                  var list = document.querySelector(".list-items");
                  let showMoreButton = document.querySelector('#show-more-button');
                  let showMoremessage = document.querySelector('#show-more-message');
                  // Set the dataset attribute to 5, because it is the first time that the query was executed
                  showMoreButton.dataset.inicio = inicio+5;
                  showMoreButton.dataset.final = final+5;
                  debugger

                  // Check if number of results is less than 5, disable load more
                  if (Object.keys(data).length < 5) {
                    showMoreButton.style.display = "none";
                    showMoremessage.style.display = "block"
                  }
                  else {
                    showMoreButton.style.display = "block";
                    showMoremessage.style.display = "none"

                  }

                  for(var i = 0; i < Object.keys(data).length; i++) {

                    let recipe_cost = data[i][1];

                    let recipe = JSON.parse(data[i][0]);
                    let id = recipe[0].pk;

                    let context = {
                      "id": id,
                      "name": recipe[0]['fields']['name'],
                      "description": recipe[0]['fields']['description'],
                      "cost": recipe_cost,
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

function removeRecipe() {
    event.preventDefault();
    event.target.parentElement.remove();
}


var INGREDIENT_PARENT;
function getIngredient() {
   let articleNumber = event.target.value;
   INGREDIENT_PARENT = event.target.parentElement.children;
   if(articleNumber !== ""){
     $.ajax({
       url: '/ingredients/get/'+articleNumber,
       success: function(data) {
         // Checks if a ingredient was found
         if(data.result){

           var result = JSON.parse(data.object);
           let obj = result[0]['fields']
           INGREDIENT_PARENT[2].value = obj.name;
           let number = 1
           INGREDIENT_PARENT[3].value = number.toFixed(2);

           INGREDIENT_PARENT[4].value = UNIT_CHOICES[obj.unit];

         }
       },
       failure: function(data) {

       }
     });
   }
}


// Trigger filter event via key enter press in the input
function search() {
    //See notes about 'which' and 'key'
    if (event.keyCode == 13) {
        document.querySelector(".button-search").click();
    }
}
