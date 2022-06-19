const submitBtn = document.querySelector(".submitBtn");
const submitForm = document.querySelector(".submitForm");
submitBtn.addEventListener('click', () => {
    let ingredients = [];
    for (i of document.getElementsByName("ingr[]")) {
        ingredients.push(i.value);
    }

    let links = [];
    for (l of document.getElementsByName("link[]")) {
        links.push(l.value);
    }
    prep = Number(document.querySelector("#prep_t").value);
    cook = Number(document.querySelector("#cook_t").value);

    const recipe = {
        title : document.querySelector("#title").value,
        description : document.querySelector("#description").value,
        ingredients : ingredients.toString(),
        directions : document.querySelector("#directions").value,
        links : links.toString(),
        notes : document.querySelector("#notes").value,
        servings : Number(document.querySelector("#servings").value),
        prep_t : prep,
        cook_t : cook,
        total_t : prep + cook,
        category : document.querySelector("#category").value,
    };

    fetch('http://127.0.0.1:5000/recipes/create', {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(recipe)
    })
    .then(response => {
        console.log(`Response: ${response.status}`);
    
        if (response.status === 302) {
            window.location.replace(response.url);
        }
    })
    .catch(error => console.error("Error: ", error));
});
