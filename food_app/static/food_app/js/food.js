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


let btns = document.querySelectorAll('.productContainer button')

btns.forEach(btn=>{
    btn.addEventListener("click", addToCart)
})

function addToCart(e){
    let product_id = e.target.value
    
    let url = '/food_app/add_to_cart/'
    
    let data = {'id':product_id}
    console.log(product_id)
    
    
    fetch(url, {
        method: "POST",
        headers: {
        'Content-Type':'application/json',
         'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(data),
    })
    .then(res=>res.json())
    .then(data=>{
        document.getElementById("food_addtocart").innerHTML = '<strong>' + data[0] + '</strong>'
        document.getElementById("mobile_food_addtocart").innerHTML = '<strong>' + data[0] + '</strong>'
        console.log(data)
        document.querySelectorAll(`button[value="${product_id}"]`).forEach(btn => {
            if (parseInt(data[1]) >= 10) {
                btn.disabled = true;
                if (parseInt(data[1]) === 10) {
                    alert("Item quantity cannot be more than 10");
                }
            } else {
                btn.disabled = false;
            }
        });
    })
    .catch(error=>{
        console.log(error)
    })
}


document.querySelectorAll('.proteinClass select[name="protein"]').forEach(ptein => {
    ptein.addEventListener("change", changeProtein);
});

function changeProtein(e) {
    let protein_value = e.target.value;
    let form = e.target.closest('form'); // Get the closest form element
    let subproteinSelect = form.querySelector('select[name="subprotein"]'); // Find subprotein select within this form
    let url = '/food_app/change_protein/';

    fetch(url, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'id': protein_value}),
    })
    .then(res => res.json())
    .then(data => {
        subproteinSelect.innerHTML = '<option selected=""></option>';
        data.forEach(item => {
            subproteinSelect.innerHTML += `<option value="${item}">${item[0].toUpperCase() + item.slice(1)}</option>`;
        });
    })
    .catch(error => {
        console.log(error);
    });
}


document.addEventListener('DOMContentLoaded', (event) => {
    const changeProteinButtons = document.querySelectorAll('.btn-warning');
    const formContainers = document.querySelectorAll('.hidden-form');

    changeProteinButtons.forEach((button, index) => {
        const formContainer = formContainers[index];
        const formOverlay = document.createElement('div');
        
        formOverlay.classList.add('protein-background');
        document.body.appendChild(formOverlay);
        formOverlay.style.display = 'none';

        button.addEventListener('click', () => {
            formContainer.classList.remove('hidden-form');
            formOverlay.style.display = 'block';
        });

        formOverlay.addEventListener('click', () => {
            formContainer.classList.add('hidden-form');
            formOverlay.style.display = 'none';
        });
    });
});

