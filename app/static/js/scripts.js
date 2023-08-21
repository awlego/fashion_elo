function selectImage(imageId) {
    // Deselect previously selected images
    const images = document.querySelectorAll('.image-container img');
    images.forEach(img => {
        img.classList.remove('selected');
    });

    // Select the clicked image
    const selectedImage = document.getElementById(imageId);
    selectedImage.classList.add('selected');

    // Make an AJAX call to the backend to get two new random images
    fetch(`/select_image/${imageId}`)
    .then(response => response.json())
    .then(data => {
        updateDisplayedImages(data);
    });
}

function updateDisplayedImages(imageData) {
    const images = document.querySelectorAll('.image-container img');
    images[0].src = imageData[0].path;
    images[0].id = imageData[0].id;
    
    images[1].src = imageData[1].path;
    images[1].id = imageData[1].id;
}
