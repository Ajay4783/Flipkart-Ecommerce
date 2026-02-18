
function startVoiceSearch() {

    const micIcon = document.getElementById('micIcon');
    const searchInput = document.getElementById('searchInput');
    const searchForm = document.getElementById('searchForm');

    if (!micIcon || !searchInput || !searchForm) {
        console.warn("Voice search elements not found on this page.");
        return;
    }

    if ('webkitSpeechRecognition' in window) {
        var recognition = new webkitSpeechRecognition();
        recognition.lang = 'en-US';

        recognition.onstart = function () {
            micIcon.classList.add('voice-active');
            searchInput.placeholder = "Listening...";
        };

        recognition.onresult = function (event) {
            var voiceText = event.results[0][0].transcript;
            searchInput.value = voiceText;
            setTimeout(() => {
                searchForm.submit();
            }, 500);
        };

        recognition.onend = function () {
            micIcon.classList.remove('voice-active');
            searchInput.placeholder = "Search for products, brands and more";
        };

        recognition.start();
    } else {
        alert("Voice Search not supported in this browser.");
    }
}


document.addEventListener("DOMContentLoaded", function () {

    const searchInput = document.getElementById('searchInput');
    const suggestionBox = document.getElementById('suggestion-box');


    if (searchInput && suggestionBox) {

        searchInput.addEventListener('keyup', function () {
            const query = this.value.trim();

            if (query.length > 1) {
                fetch(`/blog/search-suggestions/?term=${query}`)
                    .then(response => response.json())
                    .then(data => {
                        suggestionBox.innerHTML = '';
                        if (data.length > 0) {
                            suggestionBox.style.display = 'block';
                            data.forEach(item => {
                                const div = document.createElement('a');
                                div.href = item.url;
                                div.className = 'suggestion-item';
                                div.innerHTML = `
                                    <img src="${item.image}" class="s-img" alt="img">
                                    <span class="s-name">${item.label}</span>
                                `;
                                suggestionBox.appendChild(div);
                            });
                        } else {
                            suggestionBox.style.display = 'none';
                        }
                    })
                    .catch(err => console.error("Search Error:", err));
            } else {
                suggestionBox.style.display = 'none';
            }
        });


        document.addEventListener('click', function (e) {
            if (searchInput && suggestionBox) {
                if (!searchInput.contains(e.target) && !suggestionBox.contains(e.target)) {
                    suggestionBox.style.display = 'none';
                }
            }
        });

    } else {
        console.log("Search bar not present on this page (Normal behavior).");
    }
});