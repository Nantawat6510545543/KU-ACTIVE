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

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById('fileInput').addEventListener('change', function () {
        var input = document.getElementById('fileInput');
        var backgroundSlide = document.getElementById('backgroundSlide');
        backgroundSlide.innerHTML = '';
        // Loop through selected files and create image elements
        for (var i = 0; i < input.files.length; i++) {
            var reader = new FileReader();

            reader.onload = function (e) {
                var img = document.createElement('img');
                img.className = 'image-Slides';
                img.src = e.target.result;
                img.alt = "Activity Picture";
                img.width = 400;
                img.height = 240;

                // Append the image to the background slide div
                backgroundSlide.appendChild(img);
            };

            // Read the selected file as a data URL
            reader.readAsDataURL(input.files[i]);
        }
    });
});
