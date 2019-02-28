document.addEventListener('DOMContentLoaded', () => {
    // Retrieve and compile Handlebars template

    const template = document.querySelector('#handlebar-ingredient-template');

    if(template) {
       const compiledTemplate = Handlebars.compile(template.innerHTML);
       // Add Listener to button to create a new ingrediento model to recipe
       document.querySelector('#new-ingredient').onclick = (e)  => {
           e.preventDefault();
           // Creating the html text from handlebars template
           const content = compiledTemplate();
           // Append the new recipe element to DOM.
           document.querySelector('#ingredients').innerHTML += content;
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

});

function removeRecipe() {
    event.preventDefault();
    event.target.parentElement.remove();
}
