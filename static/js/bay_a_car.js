
function theme() {
  const iconTheme = document.querySelector('.icon')

  iconTheme.addEventListener('click', () => {

    let el = document.documentElement
    if(el.hasAttribute('data-theme')) {
      el.removeAttribute('data-theme')
    }else {
        el.setAttribute('data-theme','light')
      }
  })
}

theme()


function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
    document.getElementById("main").style.marginLeft = "250px";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
}