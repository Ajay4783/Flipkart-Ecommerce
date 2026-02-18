function showMethod(methodId, element) {
    document.querySelectorAll('.payment-option').forEach(opt => opt.classList.remove('active'));
    element.classList.add('active');
    document.querySelectorAll('.method-content').forEach(content => content.classList.remove('active'));
    document.getElementById(methodId).classList.add('active');
}


function processPayment() {

    document.getElementById('loading-overlay').style.display = 'block';


    setTimeout(function () {

        window.location.href = "{% url 'place_order' %}";
    }, 2500);
}