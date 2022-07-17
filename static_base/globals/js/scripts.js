(() => {
    const forms = document.querySelectorAll('.delete-form')
    for (const form of forms) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            const confirmed = confirm('Are you sure?')
            if (confirmed) {
                form.submit()
            }
        })
    }
})();

(() => {
    const buttonOpenMenu = document.querySelector('.menu-open-button')
    const buttonCloseMenu = document.querySelector('.menu-close-button')
    const menuContainer = document.querySelector('.menu-container')

    const menuHiddenClass = 'menu-hidden'
    const buttonOpenMenuHiddenClass = 'menu-open-button-hidden'

    const closeMenu = () => {
        menuContainer.classList.add(menuHiddenClass)
        buttonOpenMenu.classList.remove(buttonOpenMenuHiddenClass)
    }

    const showMenu = () => {
        menuContainer.classList.remove(menuHiddenClass)
        buttonOpenMenu.classList.add(buttonOpenMenuHiddenClass)
    }

    if (buttonCloseMenu) {
        buttonCloseMenu.removeEventListener('click', closeMenu)
        buttonCloseMenu.addEventListener('click', closeMenu)
    }
    if (buttonOpenMenu) {
        buttonOpenMenu.removeEventListener('click', showMenu)
        buttonOpenMenu.addEventListener('click', showMenu)
    }

    closeMenu()

})();

(() => {
    const logoutLinks = document.querySelectorAll('.logout-link')
    const logoutForm = document.querySelector('.logout-form')

    const logout = (e) => {
        e.preventDefault()
        logoutForm.submit()
    }

    for (const link of logoutLinks) {
        link.removeEventListener('click', logout)
        link.addEventListener('click', logout)
    }
})();