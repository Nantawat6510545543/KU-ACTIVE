function show_hide() {
   var click = document.getElementById("Dropdown");
   if (click.style.display === "none") {
      click.style.display = "block";
   } else {
      click.style.display = "none";
   }
}

function check_size() {
   var click = document.getElementById("Dropdown");
   var size = document.documentElement.clientWidth || window.innerWidth;
   if (size > 1170){
      click.style.display = "none";
   }
}

window.addEventListener('resize', check_size)

function closeMsg() {
    var alertMsg = document.getElementById('alert-msg');

    // Check if the alertMsg element exists
    if (alertMsg) {
        // Set opacity to 0 and transition to make it smooth
        alertMsg.style.opacity = '0';

        // After the transition is complete, set display to 'none'
        setTimeout(function () {
            alertMsg.style.display = 'none';
        }, 1000); //(1 seconds) transition time in CSS
    }
}