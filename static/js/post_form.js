let form = document.getElementsByTagName('form')[0];
form.addEventListener('submit', function(e) {
    e.preventDefault();
    submitForm();
});

function submitForm() {
    const formData = {};
    // Loop through the form's elements and populate the formData object
    for (const element of form.elements) {
        if (element.name && element.tagName === 'INPUT') {
            formData[element.name] = element.value;
        }
    }

    // window.location.href is the current page's URL
    fetch(window.location.href, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
    })
    .then(response => {
        window.alert(response.json());
        if (response.ok) {
            // Handle the redirect response
            window.location.href = '/login';
        } else {
            // Handle other responses (e.g., errors)
            console.alert(response.json());
            console.error('Error:', response.status);
            throw new Error('Request failed with status ' + response.status);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });

}