// export function validate(input) {
//     let message = '';
//     state = input.validity;
//     if (input.value === '') 
//         message = 'Entry cannot be empty'
//     else if (state.tooLong)
//         message = 'Entry is too long';
//     else if (state.typeMismatch) 
//         message = 'Enter correct form';
//     return message;
// }

const to_validate = document.querySelectorAll('.toValidate');
for (let v of to_validate) {
    v.addEventListener('submit', (e) => {
        if (!v.checkValidity()) {
            e.preventDefault();
            // v.setCuso
            v.reportValidity();
        }

        // message = validate(v);
        // if (messege !== '') {
        //     e.preventDefault();
        //     v.setCustomValidity(message);
        //     v.reportValidity();
        // }
    });
}