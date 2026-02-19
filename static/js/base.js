function toggleChat() {
    var chatBox = document.getElementById("chatBox");
    chatBox.style.display = (chatBox.style.display === "none" || chatBox.style.display === "") ? "flex" : "none";
}

function handleEnter(event) {
    if (event.key === 'Enter') sendMessage();
}

function sendMessage() {
    var input = document.getElementById("userMsg");
    var msg = input.value.trim();
    if (msg === "") return;

    var chatBody = document.getElementById("chatBody");
    var userDiv = document.createElement("div");
    userDiv.className = "message user-msg";
    userDiv.innerText = msg;
    chatBody.appendChild(userDiv);
    input.value = "";
    chatBody.scrollTop = chatBody.scrollHeight;

    fetch(`/blog/chatbot/?msg=${msg}`)
    .then(response => response.json())
    .then(data => {
        var botDiv = document.createElement("div");
        botDiv.className = "message bot-msg";
        botDiv.innerHTML = data.response; 
        chatBody.appendChild(botDiv);
        chatBody.scrollTop = chatBody.scrollHeight;
    })
    .catch(error => console.error('Error:', error));
}

document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.add-cart-btn');

    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const btn = this;
            const originalText = btn.innerHTML;

            let imgUrl = ''; 
            
            const parentCard = btn.closest('.card, .product-item, .box-element, .product-box, .col-md-3, .col-md-4');
            if (parentCard) {
                const imgTag = parentCard.querySelector('img');
                if (imgTag) imgUrl = imgTag.src;
            }

            if (!imgUrl) {
                const mainImg = document.querySelector('.product-detail-img') || 
                                document.querySelector('.carousel-item.active img') || 
                                document.querySelector('#main-image') || 
                                document.querySelector('.zoom-img') ||
                                document.querySelector('.product-main-image img'); 
                if (mainImg) imgUrl = mainImg.src;
            }

            if (!imgUrl) {
                const allImgs = document.querySelectorAll('img');
                for (let img of allImgs) {
                    if (img.width > 100 && img.height > 100 && !img.src.includes('logo') && !img.src.includes('icon')) {
                        imgUrl = img.src;
                        break; 
                    }
                }
            }

            if (!imgUrl) {
                imgUrl = 'https://via.placeholder.com/100?text=No+Img';
            }

            const prodId = btn.getAttribute('data-id');
            const type = btn.getAttribute('data-type');
            
            btn.innerHTML = '<i class="fa fa-circle-o-notch fa-spin"></i> Adding...';
            btn.disabled = true;

            fetch(`/add-to-cart-ajax/?prod_id=${prodId}&type=${type}`)
            .then(response => response.json())
            .then(data => {
                btn.innerHTML = originalText;
                btn.disabled = false;

                if(data.status === 'Added'){
                    const badge = document.getElementById('cart-badge');
                    if(badge) {
                        badge.innerText = data.cart_count;
                        badge.style.display = 'flex';
                    }

                    const popup = document.getElementById('mini-cart-notification');
                    const popupImg = document.getElementById('popup-img');
                    const popupTick = document.getElementById('popup-tick');

                    popupImg.src = imgUrl;

                    popup.classList.remove('show');
                    popupImg.classList.remove('spin-animation');
                    popupTick.classList.remove('show-tick');

                    setTimeout(() => {
                        popup.classList.add('show');       
                        popupImg.classList.add('spin-animation'); 
                        
                        setTimeout(() => {
                            popupTick.classList.add('show-tick');
                        }, 600); 

                    }, 50);

                    setTimeout(() => {
                        popup.classList.remove('show');
                    }, 7000);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                btn.innerHTML = originalText;
                btn.disabled = false;
            });
        });
    });
});