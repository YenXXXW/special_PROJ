document.addEventListener('DOMContentLoaded', (event) => {
    const form = document.getElementById('category-select-form');
    const productsContainer = document.querySelector('.row.col-lg-9.gx-5');

    form.addEventListener('change', (event) => {
        if (event.target.type === 'radio') {
            const selectedValue = event.target.value;
            sendPostRequest(selectedValue);
        }
    });

    function sendPostRequest(selectedValue) {
        fetch("/", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ category: selectedValue })
        })
        .then(response => response.json())
        .then(() => {
            window.location.reload(); // Reload the page
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
