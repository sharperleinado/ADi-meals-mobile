function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');



state = document.getElementById('state');
state.addEventListener("change", changeAddress);

function changeAddress(e) {
    console.log(e.target)
}


/*document.querySelectorAll('.addressClass select[name="state"]').forEach(state => {
    state.addEventListener("change", changeAddress);
});

function changeAddress(e) {
    division = e.target.value
    console.log(division)

    let form = e.target.closest('form'); // Get the closest form element
    let lgaSelect = form.querySelector('select[name="divison"]'); // Find subprotein select within this form
    let url = '/authentication/change_address/';

    fetch(url, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'id': division}),
    })
    .then(res => res.json())
    .then(data => {
        console.log(data)
        /*lgaSelect.innerHTML = '<option selected=""></option>';
        data.forEach(item => {
            lgaSelect.innerHTML += `<option value="${item}">${item}</option>`;
        });
    })
    .catch(error => {
        console.log(error);
    });
}*/



