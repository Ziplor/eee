// This part captures the file from the form
document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const file = document.getElementById('fileInput').files[0];
    if (file) {
        document.getElementById('fileInfo').innerText = `You uploaded: ${file.name}`;
        processFile(file); // Sends the file to the backend
    }
});

// This part sends the file to the backend (Flask API)
function processFile(file) {
    const formData = new FormData();
    formData.append('file', file);

    fetch('http://localhost:5000/process', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.is_looped) {
            alert(data.message); // Show a message if a loop is detected
        }
    })
    .catch(error => {
        console.error('Error:', error); // If there's an error, log it
    });
}
