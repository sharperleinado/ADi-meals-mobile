let btns = document.querySelectorAll('.addProduct button')


btns.forEach(btn=>{
    btn.addEventListener("click", addToCart)
    
})

function addToCart(e){
    let btn = e.target
    console.log(btn)
}



console.log("hello world!")


