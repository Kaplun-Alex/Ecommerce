var updateBtns = document.getElementsByClassName('update-cart');

for (var i=0; i <  updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productID:', productId, 'Action:', action)

        console.log('User:', user)
        if (user == 'AnonymousUser'){
            console.log('Go to anonimouser process')
            updateAnonimouseUserOrder(productId, action)
        }
        else {
            updateUserOrder(productId, action)
        }
    })
}

// function addCookieItem(productId, action) {

//     if(action == 'add') {
//         console.log('Increace item...')
//         var url = '/update_item/'
        
//         fetch(url, {
//             method: 'POST',
//             headers:{
//                 'Content-Type':'aplication/json', 
//                 'X-CSRFToken':csrftoken,
//             },
//             body:JSON.stringify({'productId':productId, 'action':action})
//         })
//         .then((response) =>{
//             return response.json()
//         })
    
//         .then((data) =>{
//             console.log('data:', data)
//             location.reload()
//         })


//         if(cart[productId] == undefined){
//             cart[productId] = {'quantity':1}
//         }
//         else{
//             cart[productId]['quantity'] += 1
//         }
//     }
    
//     if(action =='remove'){
//         console.log('Decreace item...')
//         cart[productId]['quantity'] -= 1

//         if(cart[productId]['quantity'] <= 0){
//             delete cart[productId]
//             }
//     }

//     document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
//     console.log(cookie)

//     location.reload()
// }

function updateAnonimouseUserOrder(productId, action){
    console.log('No user, user name is CSRF')

    var url = '/update_item/'
    
    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'aplication/json', 
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productId':productId, 'action':action})
    })
    .then((response) =>{
        return response.json()
    })

    .then((data) =>{
        console.log('data:', data)
        location.reload()
    })
}

function updateUserOrder(productId, action){
    console.log('User is logged in, sending data...')

    var url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'aplication/json', 
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productId':productId, 'action':action})
    })
    .then((response) =>{
        return response.json()
    })

    .then((data) =>{
        console.log('data:', data)
        location.reload()
    })
}
