var updateBtns = document.getElementsByClassName('update-cart')
for (var i=0; i <  updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productID:', productId, 'Action:', action)

        console.log('User:', user)
        if (user==='AnonymousUser'){
            console.log('Usrr is not authenticated')
        }
        else {
            updateUserOrder(productId, action)
        }
    })
}

function updateUserOrder(productId, action){
    console.log('User is logged in, sending data...')

    var url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'aplication/json'
        },
        body:JSON.stringify({'productId':productId, 'action':action})
    })
    .then((response) =>{
        return response.json()
    })

    .then((data) =>{
        rconsole.log('data:', data)
    })
}