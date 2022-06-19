/*
    Picking a recipe to be included into a menu.
    
    User clicks 'add' button ->
        1. The recipe is removed from the 'all_recipes' list
        2. The recipe is added to 'included_recipes list'
*/

const pickBtns = document.querySelectorAll('.pick_button');
const removeBtns = document.querySelectorAll('.remove_button'); 
const all_recipes = document.querySelector('#all_recipes');
const selected_recipes = document.querySelector('#selected_recipes')
const select_course = document.querySelectorAll('.select_course');

function update_course(event) {
    const recipe = event.target.parentElement;
    const input = recipe.querySelector('input');
    let value = input.value;
    value = event.target.value + value.slice(1, value.length);
    
    input.setAttribute('value', value);
}

function pick(event) {

    const recipe = event.target.parentElement;
    const input = recipe.querySelector('input');

        input.setAttribute('name', 'selected_recipe');
        let value = input.getAttribute('value');
        value = '0' + value.slice(1, value.length);
        input.setAttribute('value', value);

    
    let select = document.createElement('select');
        select.setAttribute('class', 'select_course');
        select.addEventListener('change', update_course);
    const course = ['-', 'Breakfast', 'Lunch', 'Dinner', 'Snack']
    for (let i in course) {
        let opt = document.createElement('option');
        opt.setAttribute('value', i.toString());
            opt.textContent = course[i];
            select.appendChild(opt);
    }

    let removeBtn = document.createElement('button');
        removeBtn.setAttribute('type', 'button');
        removeBtn.setAttribute('class', 'remove_button');
        removeBtn.textContent = 'Remove';
        removeBtn.addEventListener('click', remove);
        
     // Remove the 'add' button
    recipe.removeChild(recipe.querySelector('button'));
    recipe.append(select, removeBtn);
    selected_recipes.appendChild(recipe);
}

function remove(event) {
    const recipe = event.target.parentElement;
        recipe.querySelector('input').removeAttribute('name');
    
    let addBtn = document.createElement('button');
        addBtn.setAttribute('class', 'action_button pick_button');
        addBtn.setAttribute('type', 'button');
        addBtn.textContent = 'Add';
        addBtn.addEventListener('click', pick);
    
    recipe.removeChild(recipe.querySelector('button'));
    recipe.removeChild(recipe.querySelector('select'));
    recipe.append(addBtn);
    all_recipes.appendChild(recipe);
}

for (let btn of pickBtns) {
    btn.addEventListener('click', pick);
}

for (let btn of removeBtns) {
    btn.addEventListener('click', remove);
}

for (let select of select_course) {
    select.addEventListener('change', update_course);
}