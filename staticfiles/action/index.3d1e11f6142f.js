function setupSearchFunction() {
    var selectElement = document.querySelector('.search-criteria');
    var inputElement = document.querySelector('.search-bar');
    var dropdownElement = document.querySelector('.tag-search');

    function updateSearchUI() {
        if (selectElement.value === 'date') {
            inputElement.type = 'datetime-local';
            inputElement.style.display = 'inline-block';
            inputElement.disabled = false;
            dropdownElement.disabled = true;
            dropdownElement.style.display = 'none';
        } else if (selectElement.value === 'categories') {
            inputElement.style.display = 'none';
            dropdownElement.style.display = 'inline-block';
            inputElement.disabled = true;
            dropdownElement.disabled = false;
        } else {
            inputElement.type = 'text';
            inputElement.style.display = 'inline-block';
            inputElement.disabled = false;
            dropdownElement.disabled = true;
            dropdownElement.style.display = 'none';
        }
    }

    // setup
    updateSearchUI();
    selectElement.addEventListener('change', updateSearchUI);
}

// Call the Function on initial page load
document.addEventListener("DOMContentLoaded", setupSearchFunction);

// Call the Function when the page is refreshed
window.addEventListener('load', setupSearchFunction);

function AdvanceFunction() {
  var advance = document.getElementById("advance-search");
  if (advance.style.display === "block") {
    advance.style.display = "none";
  } else if (advance.style.display = "none"){
    advance.style.display = "block";
  }
}