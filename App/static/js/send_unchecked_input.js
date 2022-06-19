const f = document.querySelector("#main_form");

function sendInfo() {
    // Get recipes which were included in the category
    const recipes = document.getElementsByName("included_recipes[]");

    for (recipe of recipes) {
        // If a recipe got unchecked, then create and send 
        // Hidden input to the server
        if (recipe.checked === false) {
            const listInfo = document.createElement('input');
            listInfo.setAttribute("type", "hidden");
            listInfo.setAttribute("name", "excluded_recipes[]");
            listInfo.setAttribute("value", recipe.value);
            
            recipe.parentNode.appendChild(listInfo);
            recipe.remove();
        }
    }
}

// Do the action when the first form is submitted
f.addEventListener('submit', sendInfo);
