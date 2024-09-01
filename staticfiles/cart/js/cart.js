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
    let btn_name = e.target.name
    let btn_value = e.target.value
    let food_category = e.target.dataset.item
    let content_object = e.target.dataset.content

    let combinedId = btn_value + '-' + food_category;
    let combinedContentObject = content_object + '-' + food_category;
    
    console.log(btn_name)
    console.log(btn_value)
    /*console.log(food_category)
    console.log(content_object)*/
    

    let url = '/cart/cart-buttons/'
    
    let data = {'id':btn_value,'btn_name':btn_name,'form':food_category}
    
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
        document.getElementById("food_addtocart").innerHTML =  data[2]
        document.getElementById("subtotal").innerHTML =  '₦' + data[3]
        /*Delete thisif it is not working*/
        if (parseInt(data[4]) < 1) {
            window.location.href = '/';
            return;
        }
        
        if (btn_name === 'delete-item') {
            // If it's a delete operation, remove the HTML elements for the deleted item
            let itemContainer = document.getElementById(combinedId);

            if (itemContainer) {
                itemContainer.parentNode.removeChild(itemContainer);
        
            }
        } else {
            // If it's not a delete operation, update the quantity and unit price as usual
            let itemContainer = document.getElementById(combinedId);
            console.log(itemContainer)
            if (itemContainer) {

                let quantityElement = itemContainer.querySelector('.quantity');
                let quantityUnitPriceElement = itemContainer.querySelector('.quantity-unit-price');
                console.log(quantityElement)
                console.log(quantityUnitPriceElement)

                if (quantityElement && quantityUnitPriceElement) {
                    quantityElement.innerHTML = data[1];
                    quantityUnitPriceElement.innerHTML = '₦' + data[0].toLocaleString();
                }

                    // Check if the quantity is zero, and if so, remove the entire item block
                    if (parseInt(data[1]) < 1) {
                        itemContainer.parentNode.removeChild(itemContainer);
            
            }
        }
        }
        /*if (btn_name === 'add-item') {
            showNotification('Item added to the cart', '#4CAF50');
        } else if (btn_name === 'subtract-item') {
            showNotification('Item quantity updated', '#FF9800');
        } else if (btn_name === 'delete-item' && parseInt(data[1]) === 0) {
            showNotification('Item removed from the cart', '#F44336');
        }*/
        console.log(data)

    })
    .catch(error=>{
        console.log(error)
    })
}

/*function showNotification(message, color) {
    let notificationContainer = document.getElementById('notification-container');
    notificationContainer.innerHTML = message;
    notificationContainer.style.backgroundColor = color;
    notificationContainer.style.display = 'block';

    // Hide the notification after a few seconds (adjust as needed)
    setTimeout(() => {
        hideNotification();
    }, 3000);
}

function hideNotification() {
    let notificationContainer = document.getElementById('notification-container');
    notificationContainer.style.display = 'flex';
}*/


let clearAllButton = document.getElementById('clear_all');
let overlay = document.getElementById('overlay');
let okayButton = document.getElementById('okayButton');
let cancelButton = document.getElementById('cancelButton');
let container = document.getElementById('container');

clearAllButton.addEventListener("click", function() {
    overlay.style.display = 'flex';
});

okayButton.addEventListener('click', function() {
    // Add your delete logic here

    let okayValue = okayButton.value;
    console.log(okayValue)
    let url = '/cart/clear_all/';
    let data = {'okay_value': okayValue};
    
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
        console.log(data);
        window.location.href = '/';
        return;
    })
    .catch(error => {
        console.log(error);
    });

    alert('Delete confirmed!');
    overlay.style.display = 'none';
});

cancelButton.addEventListener('click', function() {
    overlay.style.display = 'none';
});



document.querySelectorAll('.proteinClass select[name="protein"]').forEach(ptein => {
    ptein.addEventListener("change", changeProtein);
});

function changeProtein(e) {
    let protein_value = e.target.value;
    let form = e.target.closest('form'); // Get the closest form element
    let subproteinSelect = form.querySelector('select[name="subprotein"]'); // Find subprotein select within this form
    let url = '/cart/change_cart_protein/';

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
    const changeProteinButtons = document.querySelectorAll('.btn-white');
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

