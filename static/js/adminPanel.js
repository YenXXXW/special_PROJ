const viewProducts = document.getElementById("view-products")
const addProdcut = document.getElementById("add-product")
viewProducts.addEventListener("click", ViewProducts )

addProdcut.addEventListener("click", AddProduct)

function ViewProducts() {
    let produts
    fetch('/shop_admin_data', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        }
   })
    .then(response => {
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json(); // assuming the response is JSON
    })
    .then(data => {
        const content = document.getElementById('content')
        content.innerHTML=""
        console.log(data)
        const productsContainer = document.createElement('div')
        productsContainer.classList.add("productsContainerAdminPage")
        data.products.map(product => {
            
            const productDiv = document.createElement('div')
            productDiv.classList.add('productAdminPage')
            const editButton = document.createElement('button')
            editButton.textContent = "Edt"
            editButton.dataset.productId = product.id
            editButton.addEventListener("click", () => productEdit(product.id))
            productDiv.innerHTML= `
                <img src="${product.image_url}" width="100"/>
                <p>${product.name}</p>
                <p>${product.price} </p>
            `
            productDiv.appendChild(editButton)
            console.log("helo")
            productsContainer.appendChild(productDiv)
        })
        console.log(productsContainer)
        content.appendChild(productsContainer)
        
    })
    .catch(error => {
        console.error('Error:', error);
    });

    
}

function getCSRFToken() {
    let cookieValue = null;
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith('csrftoken=')) {
            cookieValue = cookie.substring('csrftoken='.length, cookie.length);
            break;
        }
    }
    return cookieValue;
}

function productEdit(id) {
    const body = JSON.stringify({
        productId: id
    })
    console.log(id)
    console.log("the button clicked")
    fetch('/get_product_by_Id', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: body 
   })
    .then(response => {
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json(); // assuming the response is JSON
    })
    .then(data => {
        const content = document.getElementById('content')
        const UpdateButton = document.createElement('button')
        UpdateButton.innerHTML = "Update"
        UpdateButton.setAttribute("type", "submit")
        content.innerHTML=""
        
// Create form fields as separate elements
    const productContainerForm = document.createElement('form')
    const NameLabel = document.createElement('label')
    NameLabel.innerHTML = 'product name'
    NameLabel.setAttribute('for', 'name')
    const productNameInput = document.createElement('input')
    productNameInput.id = 'name'
    productNameInput.name = 'name'
    productNameInput.value = data.product.name
    const nameDiv = document.createElement('div')
    nameDiv.appendChild( NameLabel)
    nameDiv.appendChild(productNameInput)

    const productPriceInput = document.createElement('input')
    productPriceInput.name = 'price'
    productPriceInput.type = 'number'
    productPriceInput.id = 'price'
    productPriceInput.value = data.product.price
    const priceDiv = document.createElement('div')
    const PriceLabel = document.createElement('label')
    PriceLabel.htmlFor = 'price'
    PriceLabel.innerHTML = 'prcie'
    priceDiv.appendChild(PriceLabel)
    priceDiv.appendChild(productPriceInput)

    const productDescriptionInput = document.createElement('input')
    productDescriptionInput.name = 'description'
    productDescriptionInput.id = "description"
    productDescriptionInput.value = data.product.description
    const DescDiv = document.createElement('div')
    const DescLabel = document.createElement('label')
    DescLabel.innerHTML = 'description'
    DescLabel.htmlFor = 'description'
    DescDiv.appendChild(DescLabel)
    DescDiv.appendChild(productDescriptionInput)
    const productImage = document.createElement('img')
    productImage.setAttribute('src', data.product.image_url)
    productImage.setAttribute('width', 200)
    
    const ImageUpload = document.createElement('input')
    ImageUpload.type = "file"
    ImageUpload.name = "image"
    ImageUpload.accept = "image/jpeg, image/png, image/webp"
    // Append form fields to the form element
    const childElements = [ nameDiv, priceDiv,DescDiv, productImage, ImageUpload, UpdateButton]
    childElements.forEach(child => productContainerForm.appendChild(child))

    content.appendChild(productContainerForm)

    ImageUpload.addEventListener("change", (e) => {
        const uploadedImage = e.target.files[0]
        if (uploadedImage) {
            const reader = new FileReader()

            reader.onload = (e) => {
                productImage.src = e.target.result
            }

            reader.readAsDataURL(uploadedImage)
        }
    })
    UpdateButton.addEventListener("click", (e) => {
        e.preventDefault()

        const formData = new FormData(productContainerForm)
        formData.append("id", data.product.id)
        var url='/shop_admin_panel_edit_product'
        fetch(url, {
            method: "POST",
            headers: {
                'X-CSRFToken':csrftoken,
            }, body:formData
        }).then(res => res.json())
        .then(data => console.log(data))
    })
    })
    .catch(error => {
        console.error('Error:', error);
    });

}

function AddProduct() {
    
}