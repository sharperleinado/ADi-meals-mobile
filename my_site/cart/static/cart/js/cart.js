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
        document.getElementById("soup_addtocart").innerHTML = '<strong>Cart(</strong>' + data[2] + '<strong>)</strong>'
        
        if (btn_name === 'delete-item') {
            // If it's a delete operation, remove the HTML elements for the deleted item
            let itemContainer = document.getElementById(combinedId);

            if (itemContainer) {
                itemContainer.parentNode.removeChild(itemContainer);
        
            }
        } else {
            // If it's not a delete operation, update the quantity and unit price as usual
            let itemContainer = document.getElementById(combinedId);
            if (itemContainer) {

                let quantityElement = itemContainer.querySelector('.quantity');
                let quantityUnitPriceElement = itemContainer.querySelector('.quantity-unit-price');

                if (quantityElement && quantityUnitPriceElement) {
                    quantityElement.innerHTML = '<strong>Quantity: </strong>' + data[1];
                    quantityUnitPriceElement.innerHTML = '<strong>Quantity + Unit price: ₦</strong>' + data[0];
                }

                    // Check if the quantity is zero, and if so, remove the entire item block
                    if (parseInt(data[1]) === 0) {
                        itemContainer.parentNode.removeChild(itemContainer);
            }
        }
        }
        if (btn_name === 'add-item') {
            showNotification('Item added to the cart', '#4CAF50');
        } else if (btn_name === 'subtract-item') {
            showNotification('Item quantity updated', '#FF9800');
        } else if (btn_name === 'delete-item' && parseInt(data[1]) === 0) {
            showNotification('Item removed from the cart', '#F44336');
        }
        console.log(data)

    })
    .catch(error=>{
        console.log(error)
    })
}

function showNotification(message, color) {
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
}


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


