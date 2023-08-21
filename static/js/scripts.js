function selectImage(imageId) {
    // Deselect previously selected images
    const images = document.querySelectorAll('.image-container img');
    images.forEach(img => {
        img.classList.remove('selected');
    });

    // Select the clicked image
    const selectedImage = document.getElementById(imageId);
    selectedImage.classList.add('selected');

    // Make an AJAX call to the backend to record the selection
    fetch('/record', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ selected_image: imageId })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);  // Log the server's response
    });
}
