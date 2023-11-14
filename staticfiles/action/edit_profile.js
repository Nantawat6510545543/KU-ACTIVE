function display_profile() {
    const input = document.getElementById('Input_profile');
    const image = document.getElementById('uploaded_profile');

    if (input.files && input.files[0]) {
        const reader = new FileReader();

        reader.onload = function(e) {
            image.src = e.target.result;
            image.style.display = 'inline-block';
        };

        reader.readAsDataURL(input.files[0]);
    }
}

function display_Background() {
    const input = document.getElementById('Input_background');
    const image = document.getElementById('uploaded_background');

    if (input.files && input.files[0]) {
        const reader = new FileReader();

        reader.onload = function(e) {
            image.src = e.target.result;
            image.style.display = 'block';
        };

        reader.readAsDataURL(input.files[0]);
    }
}