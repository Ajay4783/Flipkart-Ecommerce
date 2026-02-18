    function swapValues() {
        
        let fromBox = document.getElementById("fromInput");
        let toBox = document.getElementById("toInput");

        
        let temp = fromBox.value;
        fromBox.value = toBox.value;
        toBox.value = temp;

        
        let btn = document.querySelector('.swap-btn');
        btn.style.transform = "translate(-50%, -50%) rotate(180deg)";
        
        
        setTimeout(() => {
            btn.style.transform = "translate(-50%, -50%) rotate(0deg)";
        }, 300);
    }