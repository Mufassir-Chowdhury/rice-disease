let imageBlob;
let prediction;

function handleFileInputChange(e) {
    const files = e.target.files;
    if (files.length > 0) {
        imageBlob = files[0];
        const reader = new FileReader();
        reader.onload = function(event) {
            const imageDataURL = event.target.result;
            const preview = document.getElementById('imagePreview');
            preview.src = imageDataURL;
            preview.style.display = 'block';
        };
        reader.readAsDataURL(files[0]);
    }
}

async function submitForm(event) {
    event.preventDefault();
    const formData = new FormData();
    formData.append('file', imageBlob);
    const response = await fetch('http://4.193.146.151:8000/predict', {
        method: 'POST',
        body: formData,
    });
    prediction = await response.json();
    displayPrediction(prediction);
}

function displayPrediction(prediction) {
    const predictionContainer = document.getElementById('predictionContainer');
    predictionContainer.innerHTML = `
        <div class="prediction-container">
            <p>Predictions:</p>
            <ul class="prediction-list">
                <li>Leaf Blight: ${prediction['blight']}</li>
                <li>Blast: ${prediction['blast']}</li>
                <li>Brown Spot: ${prediction['brownspot']}</li>
            </ul>
        </div>
    `;
}

const form = document.getElementById('uploadForm');
form.addEventListener('submit', submitForm);

const fileInput = document.getElementById('fileInput');
fileInput.addEventListener('change', handleFileInputChange);
