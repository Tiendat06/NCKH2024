function collapsedSideBar(){
    document.getElementById('toggleButton').addEventListener('click', function() {
        const specificSidebar = document.getElementById('header-sidebar');
        const sidebar = document.getElementById('sidebar');
        const content = document.querySelector('.content');
        const header_content = document.getElementById('header-content');
        const sidebar_para = document.querySelectorAll('.main-sidebar__para');
        const sidebar_item = document.querySelectorAll('.main-sidebar__item');
        const header_title = document.querySelector('#header-navbar__title');
      
        for(let i = 0; i < sidebar_para.length; i++){
            if(sidebar_para[i].classList.contains('d-none') && sidebar_item[i].classList.contains('justify-content-center')){
                sidebar_para[i].classList.remove('d-none');
                sidebar_item[i].classList.remove('justify-content-center');

            }else{
                sidebar_para[i].classList.add('d-none');
                sidebar_item[i].classList.add('justify-content-center');
            }
        }

        console.log(header_title);

        // if(header_title.classList.contains('d-none')){
        //     header_title.classList.remove('d-none');
        // }else{
        //     header_title.classList.add('d-none');
        // }

        sidebar.classList.toggle('collapsed');
        header_content.classList.toggle('collapsed');
        specificSidebar.classList.toggle('collapsed');
        content.classList.toggle('collapsed');
    });
      
}

function fullScreen(){
    const fullscreenButton = document.getElementById('navbar-bottom__icon--fullscreen');
    const content = document.querySelector('#body');

    fullscreenButton.addEventListener('click', () => {
    if (document.fullscreenElement) {
        exitFullscreen();
    } else {
        requestFullscreen();
    }
    });

    function requestFullscreen() {
        if (content.requestFullscreen) {
            content.requestFullscreen();
        } else if (content.mozRequestFullScreen) { /* Firefox */
            content.mozRequestFullScreen();
        } else if (content.webkitRequestFullscreen) { /* Chrome, Safari and Opera */
            content.webkitRequestFullscreen();
        } else if (content.msRequestFullscreen) { /* IE/Edge */
            content.msRequestFullscreen();
        }
    }

    function exitFullscreen() {
        if (document.exitFullscreen) {
            document.exitFullscreen();
        } else if (document.mozCancelFullScreen) { /* Firefox */
            document.mozCancelFullScreen();
        } else if (document.webkitExitFullscreen) { /* Chrome, Safari and Opera */
            document.webkitExitFullscreen();
        } else if (document.msExitFullscreen) { /* IE/Edge */
            document.msExitFullscreen();
        }
    }

}