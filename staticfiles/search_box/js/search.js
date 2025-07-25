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
    
    let url = '/search/add_to_cart/'
    
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

