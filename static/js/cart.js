var updateBtns = document.getElementsByClassName('update-cart')
for (var i=0;i<updateBtns.length;i++)
{
    updateBtns[i].addEventListener('click',function(){
        var productID = this.dataset.product
        var action = this.dataset.action
        console.log('productID:',productID,'action:',action)
        console.log('User:',user)
        if(user === 'AnonymousUser')
        {
            console.log('Not logged in')
        }
        else
        {
            updateUserOrder(productID,action) 
        }
    })
}

function updateUserOrder(productID,action)
{
    console.log('User is logged in, data is sending..')
    var url = '/update_item/'
    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productID':productID,'action':action})

        
    })
    .then((response) => {
        return response.json()
    })

    .then((data) => {
        location.reload();

    })

    
}