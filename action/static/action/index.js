document.addEventListener("DOMContentLoaded", function() {
    var selectElement = document.querySelector('.search-criteria');
    var inputElement = document.querySelector('.search-bar');

    selectElement.addEventListener('change', function() {
        if (selectElement.value === 'date') {
            inputElement.type = 'datetime-local';
        } else {
            inputElement.type = 'text';
        }
    });
});
