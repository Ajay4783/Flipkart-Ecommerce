document.addEventListener("DOMContentLoaded", () => {
    
    let index = 0;
    const slides = document.querySelectorAll('.banner3');
    const banner = document.querySelector('.banner');
    const banner2 = document.querySelector('.banner2');

    if (banner && banner2 && slides.length > 0) {
        const totalSlides = slides.length;
        const actualSlides = totalSlides - 1;
        let autoSlideInterval;

        function showSlide(i) {
            index = i;
            if (index > totalSlides) {
                index = totalSlides;
            }
            banner2.style.transform = `translateX(-${index * 100}%)`;

            if (index >= actualSlides) {
                setTimeout(() => {
                    banner2.style.transition = 'none';
                    index = 0;
                    banner2.style.transform = `translateX(-${index * 100}%)`;
                    setTimeout(() => {
                        banner2.style.transition = 'transform 0.5s ease';
                    }, 50);
                }, 500);
            }
        }

        function startAutoSlide() {
            clearInterval(autoSlideInterval);
            autoSlideInterval = setInterval(() => {
                showSlide(index + 1);
            }, 3000);
        }

        startAutoSlide();

        banner.addEventListener('mouseover', () => { clearInterval(autoSlideInterval); });
        banner.addEventListener('mouseout', () => { startAutoSlide(); });

        const nextBtn = document.querySelector('.next');
        if (nextBtn) {
            nextBtn.onclick = () => {
                clearInterval(autoSlideInterval);
                showSlide(index + 1);
                startAutoSlide();
            };
        }

        const prevBtn = document.querySelector('.prev');
        if (prevBtn) {
            prevBtn.onclick = () => {
                clearInterval(autoSlideInterval);
                if (index === 0) {
                    banner2.style.transition = 'none';
                    showSlide(actualSlides);
                    setTimeout(() => {
                        banner2.style.transition = 'transform 0.5s ease';
                        showSlide(actualSlides - 1);
                    }, 50);
                } else {
                    showSlide(index - 1);
                }
                startAutoSlide();
            };
        }
    }

    const scrollContainer = document.querySelector('.top-deals-container');
    const scrollButtonRight = document.querySelector('.scroll-btn');
    const scrollButtonLeft = document.querySelector('.scroll-btn2');

    function checkScrollPosition() {
        if (!scrollContainer || !scrollButtonRight || !scrollButtonLeft) return;

        if (scrollContainer.scrollLeft <= 5) {
            scrollButtonLeft.style.display = 'none';
        } else {
            scrollButtonLeft.style.display = 'block';
        }

        const maxScroll = scrollContainer.scrollWidth - scrollContainer.clientWidth;
        if (scrollContainer.scrollLeft >= maxScroll - 5) {
            scrollButtonRight.style.display = 'none';
        } else {
            scrollButtonRight.style.display = 'block';
        }
    }

    if (scrollContainer) {
        scrollContainer.addEventListener('scroll', checkScrollPosition);
        if (scrollButtonRight) {
            scrollButtonRight.addEventListener('click', () => {
                scrollContainer.scrollBy({ left: 450, behavior: 'smooth' });
            });
        }
        if (scrollButtonLeft) {
            scrollButtonLeft.addEventListener('click', () => {
                scrollContainer.scrollBy({ left: -450, behavior: 'smooth' });
            });
        }
        checkScrollPosition();
    }

    let isLoading = false;
    const container = document.getElementById('infinite-container');
    const loader = document.getElementById('loading-spinner');

    if (container && loader) {
        const sensor = document.createElement('div');
        sensor.id = 'scroll-sensor';
        sensor.style.height = '10px';
        sensor.style.width = '100%';
        sensor.style.clear = 'both';
        
        loader.parentNode.insertBefore(sensor, loader);

        const observer = new IntersectionObserver((entries) => {
            if (entries[0].isIntersecting && !isLoading) {
                loadMoreSections();
            }
        }, {
            rootMargin: '100px'
        });

        observer.observe(sensor);

        function loadMoreSections() {
            if (isLoading) return;
            
            isLoading = true;
            loader.style.display = 'block';

            const url = container.getAttribute('data-url');
            if (!url) return;

            fetch(url)
                .then(response => response.json())
                .then(data => {
                    setTimeout(() => {
                        if (data.sections && data.sections.length > 0) {
                            data.sections.forEach(sectionData => {
                                const section = document.createElement('div');
                                section.className = 'loaded-section';

                                let productsHtml = '';
                                sectionData.products.forEach(item => {
                                    let imgUrl = item.image ? item.image : 'https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg';
                                    productsHtml += `
                                            <a href="${item.url}" style="text-decoration: none; color: inherit;">
                                                <div class="mobile-item">
                                                    <img src="${imgUrl}" alt="${item.name}">
                                                    <p class="mobile-name">${item.name}</p>
                                                    <h4 class="mobile-offer">₹${item.price}</h4>
                                                </div>
                                            </a>
                                    `;
                                });

                                section.innerHTML = `
                                        <h2>${sectionData.title}</h2>
                                        <div class="mobile-items">
                                            ${productsHtml}
                                        </div>
                                `;
                                container.appendChild(section);
                            });

                            isLoading = false;
                            loader.style.display = 'none';
                            
                        } else {
                            if (loader) {
                                loader.innerHTML = "<p style='color:#666;'>That's all folks! No more products.</p>";
                                setTimeout(() => { loader.style.display = 'none'; }, 2000);
                            }
                            observer.disconnect(); 
                            sensor.remove(); 
                        }
                    }, 1500);
                })
                .catch(err => {
                    console.error(err);
                    isLoading = false;
                    loader.style.display = 'none';
                });
        }
    }
});