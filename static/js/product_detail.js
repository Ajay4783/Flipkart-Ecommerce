    function toggleReviewForm() {
        var formBox = document.getElementById("review-form-box");
        if (formBox.style.display === "none") {
            formBox.style.display = "block";
        } else {
            formBox.style.display = "none";
        }
    }
    function nativeShare() {
    const pageTitle = document.title;
    const pageUrl = window.location.href;

    if (navigator.share) {
        navigator.share({
            title: pageTitle,
            text: 'Check this out on ShopKart!',
            url: pageUrl,
        })
        .catch((error) => console.log('Error sharing', error));
    } else {
        const whatsappUrl = `https://wa.me/?text=Check this out: ${pageTitle} - ${pageUrl}`;
        window.open(whatsappUrl, '_blank');
    }
}