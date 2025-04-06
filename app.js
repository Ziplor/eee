document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const file = document.getElementById('fileInput').files[0];
    if (file) {
        document.getElementById('fileInfo').innerText = `You uploaded: ${file.name}`;
        document.getElementById('scanLoopBtn').style.display = 'inline'; // Show the "Scan for Loop" button
        currentFile = file; // Store the file for later use
    }
});

// Handle the Scan for Loop button click
document.getElementById('scanLoopBtn').addEventListener('click', function() {
    processFile(currentFile);
});

// Function to send the file to the backend for loop detection
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
            document.getElementById('loopResult').innerText = `Loop Detected! Message: ${data.message}`;
        } else {
            document.getElementById('loopResult').innerText = 'No loop detected in the file.';
        }
    })
    .catch(error => {
        console.error('Error:', error); 
    });
}
