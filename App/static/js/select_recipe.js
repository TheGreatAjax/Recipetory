const selectable_items = document.querySelectorAll(".recipe");
let selected = document.querySelector(".selected");
const selected_holder = document.querySelector('#selected');
const selected_input = document.querySelector('#selected_id');


for (let item of selectable_items) {
    item.addEventListener('click', () => {

        if (item.getAttribute('class') === 'recipe selected') {
            item.setAttribute('class', 'recipe');
            selected = null;
            selected_holder.textContent = "";
            selected_input.removeAttribute('value');
        }
        else {
            item.setAttribute('class', 'recipe selected');
            selected_holder.textContent = item.textContent;
            selected_input.setAttribute('value', item.getAttribute('data-id'));

            if (selected !== null) {
                selected.setAttribute('class', 'recipe');
            }
            selected = item;
        }
    });
}