// Template for adding a new ingredient for one recipe

document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('#newIngredient').onclick = (e)  => {
        e.preventDefault();
        const template = Handlebars.compile(document.querySelector('#handlebarIngredientTemplate').innerHTML);
        // Create new recipe element to DOM.

        const content = template();
        document.querySelector('#ingredients').innerHTML += content;
    };

});

function removeRecipe() {
    event.preventDefault();
    event.target.parentElement.remove();
}
