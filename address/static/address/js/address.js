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



const stateSelect = document.querySelector('.addressClass select[name="state"]');
const divisionSelect = document.querySelector('.addressClass select[name="division"]');
const lgaSelect = document.querySelector('.addressClass select[name="lga"]');
const lcdaSelect = document.querySelector('.addressClass select[name="lcda"]');

stateSelect.addEventListener("change", function(e) {
    const state = e.target.value;
    fetchData('/address/change_address/', {'division_id': state}, divisionSelect);
});

divisionSelect.addEventListener("change", function(e) {
    const division = e.target.value;
    fetchData('/address/change_address_division/', {'lga_id': division,'state':stateSelect.value}, lgaSelect);
});

lgaSelect.addEventListener("change", function(e) {
    const lga = e.target.value;
    fetchData('/address/change_address_lga/', {'lcda_id': lga,'state':stateSelect.value,'division':divisionSelect.value,'lga':lgaSelect.value}, lcdaSelect);
});

function fetchData(url, data, targetSelect) {
    fetch(url, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(data),
    })
    .then(res => res.json())
    .then(data => {
        console.log(data)
        /*targetSelect.innerHTML = '<option selected=""></option>';*/
        data.forEach(item => {
            /*targetSelect.innerHTML += `<option value="${item}">${item[0].toUpperCase() + item.slice(1)}</option>`;*/
            targetSelect.innerHTML = '<option selected=""></option>';

            // Check if it's LCDA level (i.e. values are arrays like ['Ajegunle', 800])
            if (Array.isArray(data[0])) {
                data.forEach(item => {
                    const [name, id] = item;
                    targetSelect.innerHTML += `<option value="${name}">${name}</option>`;
                });
            } else {
                data.forEach(item => {
                    targetSelect.innerHTML += `<option value="${item}">${item[0].toUpperCase() + item.slice(1)}</option>`;
                });
            }
        });
    })
    .catch(error => {
        console.log(error);
    });
}


