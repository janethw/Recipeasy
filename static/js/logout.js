// js to support logout functionality
document.addEventListener('DOMContentLoaded', (event) => {
    console.log('Logout page loaded');

         // redirect to login page after 5 seconds
     setTimeout(() => {
         window.location.href = '/login';
     }, 5000);

});