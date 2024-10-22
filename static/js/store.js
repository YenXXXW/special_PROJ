let products = productsData
selectedShop = 'all'
document.addEventListener('DOMContentLoaded', function() {
    
    // get the products previoulsy filterd with category and shop
    const searchedShop = sessionStorage.getItem('selectedShop')
    if(searchedShop) {
        
        const form = document.getElementById('category-select-form');
        const formData = new FormData(form);
        formData.append('shop_id', searchedShop)

        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            // Handle the response data
            if (data.products) {
                products = data.products
                updateProducts(products)
                const searchedValue = sessionStorage.getItem('searchedValue')
                if(searchedValue) {
                    let searchedProducts
                    if (searchedValue === '')  searchedProducts = products
                    else{
                        searchedProducts = products.filter(product => product.name.includes(searchedValue))
                    }
                    updateProducts(searchedProducts)
                }
            } else {
                console.error('No products data received.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    // listening for the category change
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');

    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
        const searchProduct = document.getElementById("navSearchInput")
        searchProduct.value = ''
            if (this.checked) {
                // Uncheck all other checkboxes
                checkboxes.forEach(otherCheckbox => {
                    if (otherCheckbox !== this) {
                        otherCheckbox.checked = false;
                    }
                });
                updateDateRequest()
            }
        });
    });

    function attachEventListeners() {
        var updateBtns = document.getElementsByClassName('update-cart');
        for (var i = 0; i < updateBtns.length; i++) {
            updateBtns[i].addEventListener('click', function() {
                var productID = this.dataset.product;
                var action = this.dataset.action;
                
                if (user === 'AnonymousUser') {
                    addCookieItem(productID, action);
                } else {
                    updateUserOrder(productID, action);
                }
            });
        }
    }

    function updateDateRequest() {
        const form = document.getElementById('category-select-form');
        const formData = new FormData(form);
        formData.append('shop_id', selectedShop)

        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            // Handle the response data
            if (data.products) {
                products = data.products
                updateProducts(products)
                
            }
         })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    function updateProducts(products) {
        const productsContainer = document.getElementById('products-container');
        console.log(products)
        productsContainer.innerHTML = ''; // Clear existing products
        productsContainer.classList.add('col-lg-9')
        productsContainer.id = "products-container"
        
        const rowElement = document.createElement('div');
        rowElement.classList.add('row', 'gy-5');
        
        products.forEach(product => {
            const productElement = document.createElement('div');
            
            productElement.classList.add('col-md-4', 'col-contianer')
            productElement.innerHTML = `
                <div class="product">
                    <div class="product-img-container">
                        <img src="${ product.image_url }" alt="${product.name}" class="product-img">
                    </div>
                    <h3 id="product-price">${product.name}</h3>
                        <p>${product.price} Ks</p>
                        <p><small>Quantity: ${product.quantity}</small></p>
                    <div>
                        
                        <a href="product/${product.id}"><button class="view_button">View</button></a>
                        <button data-product="${product.id}" data-action="add" class="add-to-cart update-cart ">Add to Cart</button>
                    </div>
                    
                </div>
            `;
            rowElement.appendChild(productElement);
        });
        
        productsContainer.appendChild(rowElement);

        attachEventListeners();
    }
    

    document.getElementById('shopSelect').addEventListener('change', function() {
        selectedShop = this.value;
        sessionStorage.setItem('selectedShop', selectedShop)
        const searchProduct = document.getElementById("navSearchInput")
        searchProduct.value = ''
        updateDateRequest()
    });

    const searchProduct = document.getElementById("navSearchInput")
    searchProduct.addEventListener('input', handleSearch)
    function handleSearch(){
        sessionStorage.setItem('searchedValue', searchProduct.value)
        let searchedProducts
        if(searchProduct.value === ''){
            searchedProducts = products
        } else {
            console.log("pr", products)
            searchedProducts = products.filter(product => product.name.includes(searchProduct.value))
        }
        console.log("se",searchedProducts)
        updateProducts(searchedProducts)
    }

});

