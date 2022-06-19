/*
    Removing a recipe from the planning calendar.
    User clicks 'remove' button next to a recipe in the
    planner -> The entry gets visually removed and 
    data is sent to the server to update the database.
*/

// Remove buttons next to planned recipes
let removeBtns = document.getElementsByName('remove_recipe');

for (let btn of removeBtns) {
    btn.addEventListener('click', () => {
        const week = {
            '1': 'Monday',
            '2': 'Tuesday',
            '3': 'Wednsday',
            '4': 'Thursday',
            '5': 'Friday',
            '6': 'Saturday',
            '7': 'Sunday' };

        // [week, day, course, id]
        const remove_info = btn.getAttribute('value').split(',');
        const send_data = {
            week_n: remove_info[0],
            day: week[remove_info[1]],
            course: remove_info[2],
            recipe_id: remove_info[3]
        };

        // Send POST request to update the database
        fetch('http://127.0.0.1:5000/planning/remove_recipe', {
            method: "POST",
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(send_data)
        })
        .then(response => console.log("Response:" + response))
        .catch(error => console.error("Error: ", error));

        // Remove the entry from DOM
        btn.parentElement.remove();
    });
}