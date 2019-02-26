document.addEventListener('DOMContentLoaded', () => {
    // Retrieve and compile Handlebars template
    const template = Handlebars.compile(document.querySelector('#handlebar-ingredient-template').innerHTML);

    // Add Listener to button to create a new ingrediento model to recipe
    document.querySelector('#new-ingredient').onclick = (e)  => {
        e.preventDefault();
        // Creating the html text from handlebars template
        const content = template();
        // Append the new recipe element to DOM.
        document.querySelector('#ingredients').innerHTML += content;
    };
});

function removeRecipe() {
    event.preventDefault();
    event.target.parentElement.remove();
}
