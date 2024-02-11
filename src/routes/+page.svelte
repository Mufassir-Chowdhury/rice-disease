<script>
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
        const formData = new FormData();
        formData.append('file', imageBlob);
        const response = await fetch('http://localhost:8000/predict', {
            method: 'POST',
            body: formData,
        });
        prediction = await response.json();
        console.log(prediction);

    }
</script>

<form on:submit|preventDefault={submitForm} class="flex flex-col items-center space-y-4">
    <div class="upload-container">
        <input type="file" id="fileInput" on:change={handleFileInputChange} class="file-input" />
        <label for="fileInput" class="file-input-label">
            <span>Choose a file</span>
        </label>
        <!-- Display the uploaded image -->
        <img id="imagePreview" alt="Uploaded Image" class="my-4 image-preview" />
    </div>
    <button type="submit" class="upload-button">Submit</button>
</form>
{#if prediction}
    <div class="prediction-container">
        <p>Predictions:</p>
        <ul class="prediction-list">
            <li>Leaf Blight: {prediction['blight']}</li>
            <li>Blast: {prediction['blast']}</li>
            <li>Brown Spot: {prediction['brownspot']}</li>
        </ul>
    </div>
{/if}
<style>

    .upload-container {
        margin-top: 20px;
        width: 400px;
        height: 300px;
        border: 2px dashed #ccc;
        border-radius: 8px;
        display: flex;
        justify-content: center;
        align-items: center;
        cursor: pointer;
        position: relative;
    }

    .file-input {
        display: none;
    }

    .file-input-label {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        text-align: center;
        cursor: pointer;
    }

    .file-input-label span {
        font-size: 16px;
        color: #666;
    }

    .file-input-label:hover {
        background-color: #f0f0f0;
    }

    .image-preview {
        width: 100%;
        height: 100%;
        object-fit: cover;
        display: none;
    }

    .upload-button {
        padding: 10px 20px;
        background-color: #4caf50;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.3s;
    }

    .upload-button:hover {
        background-color: #45a049;
    }

    .prediction-container {
        margin-top: 20px;
        text-align: center;
    }

    .prediction-list {
        list-style-type: none;
        padding: 0;
    }

    .prediction-list li {
        margin-top: 10px;
        font-weight: bold;
    }

</style>