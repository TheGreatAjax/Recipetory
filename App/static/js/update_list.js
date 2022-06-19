// import { validate } from './validate.js';

const addBtns = document.querySelectorAll('.add_button');

function update(input, list, name) {

    const item = input.value;
    input.value = "";
        
    // The data to be sent to the server
    const listInput = document.createElement('input');
        listInput.setAttribute("type", "hidden");
        listInput.setAttribute("name", name + "[]");
        listInput.setAttribute("value", item);

    // The span which contains the input and the text
    const listText = document.createElement('span');
          listText.textContent = item;
          listText.setAttribute('conenteditable', 'true');
          listText.appendChild(listInput);
          
    
    // Delete button to remove an item from the list
    const listBtn = document.createElement('button');
          listBtn.textContent = 'Remove';
          listBtn.setAttribute('class', 'remove_button');
          listBtn.setAttribute('type', 'button');
          listBtn.addEventListener('click', () => {
            list.removeChild(listBtn.parentNode);
        });
    
    // The list item holding all this
    const listItem = document.createElement('li');
          listItem.setAttribute('class', name);
          listItem.appendChild(listText);
          listItem.appendChild(listBtn);


    list.appendChild(listItem);

}

const listBtn = document.getElementsByClassName("remove_button");
for (const btn of listBtn) {
    btn.addEventListener('click', () => {
        btn.parentElement.remove();
    });
}

for (let btn of addBtns) {
    btn.addEventListener('click', () => {
        
        // First, validate the constrains
        const input = document.querySelector(btn.getAttribute('data-input'));
        let message = '';
        state = input.validity;
        if (input.value === '') 
            message = 'Entry cannot be empty'
        else if (state.tooLong)
            message = 'Entry is too long';
        else if (state.typeMismatch) 
            message = 'Enter correct form';

        input.setCustomValidity(message);
        if (message !== '') {
            input.reportValidity();
        }
        else {
            const list = document.querySelector(btn.getAttribute('data-list'));
            const name = btn.getAttribute('data-item_name');
            update(input, list, name);
        }
    })
}

// input.addEventListener('keydown', key => {
//     if (key.code == 13) {
//         update();
//     }
// })
