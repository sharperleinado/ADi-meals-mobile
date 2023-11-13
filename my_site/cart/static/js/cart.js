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
    
    console.log(btn_name)
    console.log(btn_value)
    console.log(food_category)
    

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
        console.log(document.getElementById("quantity"))/*.innerHTML = data
        console.log(data)*/
        
        /*let quantityElement = document.getElementById("quantity_${btn_value}")
        console.log(quantityElement)
        if (quantityElement) {
            quantityElement.innerHTML = '<strong>Quantity: </strong>${data}'
        }
        console.log(data)*/

    })
    .catch(error=>{
        console.log(error)
    })
}

