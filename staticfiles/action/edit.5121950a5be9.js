function displayImage() {
    const input = document.getElementById('imageInput');
    const image = document.getElementById('uploadedImage');

    if (input.files && input.files[0]) {
        const reader = new FileReader();

        reader.onload = function(e) {
            image.src = e.target.result;
            image.style.display = 'block';
        };

        reader.readAsDataURL(input.files[0]);
    }
}