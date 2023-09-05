// to get current year
// function getYear() {
//     var currentDate = new Date();
//     var currentYear = currentDate.getFullYear();
//     document.querySelector("#displayYear").innerHTML = currentYear;
// }

// getYear();


// Script for navigation bar
const bar= document.getElementById('bar')
const close= document.getElementById('close')
const nav= document.getElementById('navbar')
if(bar){
    bar.addEventListener('click', () => {
        nav.classList.add('active')
    })
}
if(close){
    close.addEventListener('click', () => {
        nav.classList.remove('active')
    })
}


