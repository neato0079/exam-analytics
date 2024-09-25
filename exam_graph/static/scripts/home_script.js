const uploadContainer = document.getElementById('upload-container');
const fileInput = document.getElementById('file-input');

// Add drag-over effect
uploadContainer.addEventListener('dragover', (event) => {
    event.preventDefault();
    uploadContainer.classList.add('drag-over');
});

uploadContainer.addEventListener('dragleave', () => {
    uploadContainer.classList.remove('drag-over');
});

// Handle file drop
uploadContainer.addEventListener('drop', (event) => {
    event.preventDefault();
    uploadContainer.classList.remove('drag-over');
    const files = event.dataTransfer.files;
    handleFiles(files);
});

// Handle file selection from the browse button
fileInput.addEventListener('change', (event) => {
    const files = event.target.files;
    handleFiles(files);
});

// Placeholder function to handle the files
function handleFiles(files) {
    if (files.length > 0) {
        alert(`File uploaded: ${files[0].name}`);
    }
}