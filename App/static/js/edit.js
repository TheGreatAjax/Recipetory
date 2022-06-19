const editBtn = document.querySelector("#edit_button");

// Update hidden inputs
// Which will send updated editable fields to the server
function update_inputs() {
    for (let input_id of ['#title_input', '#description_input', '#directions_input', '#notes_input']) {
        const field = document.querySelector(input_id);
        field.setAttribute('value', field.parentElement.textContent);
    }

    ingredients = document.getElementsByName('ingredient[]');
    for (i of ingredients) {
        i.setAttribute('value', i.parentElement.textContent);
    }

    links = document.getElementsByName('link[]');
    for (l of links) {
        l.setAttribute('value', l.parentElement.textContent);
    }
}

editBtn.addEventListener('click', update_inputs);