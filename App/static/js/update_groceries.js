
const addBtn = document.querySelector('#add_to_groceries');
const go = document.querySelector('#go_to_groceries');
const ingredients = document.querySelectorAll(".ingredient");

let checked_count = 0;

// For each ingredient
for (let ingr of ingredients) {
    const input = ingr.querySelector('input'); 
    input.addEventListener('change', () => {
        // If the item was unchecked,
        // and it is the first checked item
        // then enable the "add" button
        if (input.getAttribute('name') === '') {
            if (checked_count === 0 && go.style.display === '') {
                addBtn.style.display = 'block';
            }
            input.setAttribute('name', 'grocery');
            checked_count++;
        }

        // If item was checked and it was the only checked
        // Then disable the "add" button
        else {
            if (checked_count === 1 && go.style.display === '') {
                addBtn.style.display = 'none';
            }
            input.setAttribute('name', '');
            checked_count--;
        }
    })
}

// Update the database with the items
function send_ingredients(ingr) {
    fetch('http://127.0.0.1:5000/groceries/append', {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(ingr)
    })
    .then(response => console.log("Response:" + response.toString()))
    .catch(error => console.error("Error: ", error));
}
// Append ingredients to be added
// Send them as a string
addBtn.addEventListener('click', () => {
    let values = [];
    for (let i of document.querySelectorAll('input')) {
        if (i.getAttribute('name') === 'grocery')
            values.push(i.value);
        i.disabled = true;
    }
    
    send_ingredients(values);
    addBtn.style.display = 'none';
    go.style.display = 'block';
});

