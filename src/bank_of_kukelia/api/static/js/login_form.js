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

    var formBody = [];
    for (var property in formData) {
    var encodedKey = encodeURIComponent(property);
    var encodedValue = encodeURIComponent(formData[property]);
    formBody.push(encodedKey + "=" + encodedValue);
    }
    formBody = formBody.join("&");
    console.log(formBody);
    // window.location.href is the current page's URL
    fetch(window.location.href, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        },
        body: formBody,
    }).then(response => {
        response.json().then(data => {
        
            if (response.ok) {

                // Handle the redirect response
                window.alert(data);
                // store received token in local storage
                localStorage.setItem('jwtToken', data.token);
                localStorage.setItem('username', formData["username"]);
                
                // redirect to home page
                window.location.href = '/';
            }else {
                // Incorrect credentials response
                window.alert(data.detail);
                console.log(response);
                console.error('Error:', response.status);
                throw new Error('Request failed with status ' + response.status);
            }
        })
    }).catch(error => {
        console.error('Error:', error);
        window.alert(error);
    });

}