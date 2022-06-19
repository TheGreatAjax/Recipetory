/*
    Making cells in the planner calendar clickable.

    User clicks a cell -> 
        1. Corresponding information is set in the recipe selector
        2. The cell gets highlighted
*/

const cells = document.querySelectorAll(".clickable_cell");
const week_select = document.querySelector('#week_n');
const day_select = document.querySelector('#day');
let clicked = null;

for (let cell of cells) {
    cell.addEventListener('click', () => {

        // let state = cell.getAttribute('class');
        // if (state === 'clickable_cell highlighted') {
        //     cell.setAttribute('class', 'clickable_cell');
        // }
        if (cell === clicked) {
            cell.setAttribute('class', 'clickable_cell');
            clicked = null;
        }
        else {
            const w = Number(cell.getAttribute('data-week'));
            const d = Number(cell.getAttribute('data-day'));

            week_select.selectedIndex = w;
            day_select.selectedIndex = d;
            cell.setAttribute('class', 'clickable_cell highlighted');

            if (clicked !== null) {
                clicked.setAttribute('class', 'clickable_cell');
            }
            clicked = cell;
        }
    })
}