document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const file = document.getElementById('fileInput').files[0];
    if (file) {
        document.getElementById('fileInfo').innerText = `You uploaded: ${file.name}`;
        processFile(file);
    }
});

function processFile(file) {
    // Logic for detecting loop in video/audio
    // For now, this is a placeholder function
    console.log("Processing file", file);
}
