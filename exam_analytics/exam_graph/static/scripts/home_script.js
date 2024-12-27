// const uploadContainer = document.getElementById('upload-container');
// const fileInput = document.getElementById('file-input');

// // Add drag-over effect
// uploadContainer.addEventListener('dragover', (event) => {
//     event.preventDefault();
//     uploadContainer.classList.add('drag-over');
// });

// uploadContainer.addEventListener('dragleave', () => {
//     uploadContainer.classList.remove('drag-over');
// });

// // Handle file drop
// uploadContainer.addEventListener('drop', (event) => {
//     event.preventDefault();
//     uploadContainer.classList.remove('drag-over');
//     const files = event.dataTransfer.files;
//     console.log(`ASDFASDF: ${JSON.stringify(files)}`)
//     handleFiles(files);
// });

// // Handle file selection from the browse button
// fileInput.addEventListener('change', (event) => {
//     const files = event.target.files;
//     console.log(`ASDFASDF: ${event.target.files}`)
//     handleFiles(files);
// });

// function getCsrfToken() {
//     return document.querySelector('[name=csrfmiddlewaretoken]').value;
// }

// // Function to handle the files
// function handleFiles(files) {
//     alert(`something's wrong :( \n ${JSON.stringify(files)}`);

//     document.getElementById('file-input').addEventListener('change', function () {
//         const file = this.files[0];
//         const formData = new FormData();
//         formData.append('csv_file', file);

//         fetch('/result/', {  // Replace with your Django URL route
//             method: 'POST',
//             body: formData,
//             headers: {
//                 'X-CSRFToken': getCsrfToken() // Ensure CSRF protection
//             }
//         })
//             .then(response => response.json())
//             .then(data => {
//                 console.log('File uploaded successfully:', data);
//                 alert(`File uploaded: dfsgsdgsdfgg${files[0].name}\n${data}`);
//             })
//             .catch(error => {
//                 alert(`something's wrong :( \n ${error}`);
//                 console.error('Error uploading file:', error);
//             });
//     });

// }

document.addEventListener('DOMContentLoaded', function () {
    const uploadContainer = document.getElementById('upload-container');
    const fileInput = document.getElementById('file-input');
    const uploadForm = document.getElementById('upload-form');

    // Trigger file input click when the button is clicked
    fileInput.addEventListener('change', function () {
        if (fileInput.files) {
            uploadForm.submit(); // Submit form when a file is selected
        }
    });

    // Handle drag-and-drop functionality
    uploadContainer.addEventListener('dragover', function (e) {
        e.preventDefault();
        uploadContainer.classList.add('drag-over');
    });

    uploadContainer.addEventListener('dragleave', function () {
        uploadContainer.classList.remove('drag-over');
    });

    uploadContainer.addEventListener('drop', function (e) {
        e.preventDefault();
        uploadContainer.classList.remove('drag-over');

        if (e.dataTransfer.files) {
            fileInput.files = e.dataTransfer.files; // Assign dropped file to input
            uploadForm.submit(); // Automatically submit the form
        }
    });
});


