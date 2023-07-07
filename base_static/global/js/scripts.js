function my_scope() {
    const forms = document.querySelectorAll('.form-delete')
    for (const form of forms) {
        form.addEventListener('submit', function(e){
            e.preventDefault();
            
            const confirmed = confirm('Are you sure?')
    
            if (confirmed) {
                form.submit()
            }
           }) 
    }

    (
        () => {
           const btnCloseMenu = document.querySelector('.btn-close-menu');
           const btnShowMenu = document.querySelector('.btn-show-menu');
           const menuContainer = document.querySelector('.menu-container');
           const btnShowMenuVisible = 'btn-show-menu-visible';
           const menuHiddenClass = 'menu-hidden';
           const closeMenu = () => {

            btnShowMenu.classList.add(btnShowMenuVisible);
            menuContainer.classList.add(menuHiddenClass);
            };
           const showMenu = () => {
                btnShowMenu.classList.remove(btnShowMenuVisible);
                menuContainer.classList.remove(menuHiddenClass);
           };
           

           if(btnCloseMenu) {
            btnCloseMenu.removeEventListener('click', closeMenu);
            btnCloseMenu.addEventListener('click', closeMenu);
           }

           if(btnShowMenu) {
            btnShowMenu.removeEventListener('click', showMenu);
            btnShowMenu.addEventListener('click', showMenu);
           }
        }
    )();

    (() => {
        const authorLogoutLinks = document.querySelectorAll('.authors-logout-link');
        const formLogout = document.querySelector('.form-logout');
    
        for(const link of authorLogoutLinks) {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                formLogout.submit();
            });
        }
    }
    )();
}
my_scope()

