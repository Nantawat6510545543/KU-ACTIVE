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