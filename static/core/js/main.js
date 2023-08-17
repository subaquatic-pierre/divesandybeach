document.addEventListener('DOMContentLoaded', () => {

    // Mobile Menu settings
    mobileMenu = document.querySelector('.mobile-menu')
    document.querySelector('#mobile-menu-btn').addEventListener('click', () => {
        document.querySelector('.mobile-next-to').classList.toggle('nav-show');
        mobileMenu.classList.toggle('menu-toggle');
        // Maybe no scroll body ?
        document.querySelector('body').classList.toggle('no-scroll');
        document.querySelector('.navbar').classList.toggle('fixed-top');
    })
    document.querySelector('.mobile-next-to').addEventListener('click', () => {
        document.querySelector('.mobile-next-to').classList.remove('show');
        mobileMenu.classList.remove('menu-toggle');
        document.querySelector('.navbar').classList.remove('fixed-top');
        document.querySelector('body').classList.remove('no-scroll');
    })


    // Booking form settings

    function addDiverInput() {
        extra_diver++
        // create input group div
        div = document.createElement('div')
        div.innerHTML =
            `    
        <div class="form-group">         
            <div class="input-group">
                <input type="text" class="form-control" name=extra_diver_${extra_diver} placeholder="Enter divers full name">
                <div class=""><i class="remove-extra-diver-btn trash-icon fas fa-trash px-auto"></i></div>
            </div>
        </div>
        `
        button = div.children[0].children[0].children[1].children[0]
        input = div.children[0].children[0].children[0]
        input.setAttribute('required', true)
        button.onclick = removeDiverInput
        $('#extra-divers').append(div)
        input.focus()
        console.log(input)
    }

    function removeDiverInput(e) {
        e.target.parentElement.parentElement.remove()
        console.log(extra_diver)

    }

})

const delay = ms => new Promise(res => setTimeout(res, ms));
