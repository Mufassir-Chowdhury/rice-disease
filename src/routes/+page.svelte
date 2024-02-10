<script>
    let video;
    let canvas;
    let ctx;
    let imageBlob;
    let prediction;

    async function startCamera() {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
    }

    function captureImage() {
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        canvas.toBlob(blob => {
            imageBlob = blob;
        });
    }
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


    function handleDragOver(e) {
        e.preventDefault();
        e.stopPropagation();
        e.target.closest('.upload-container').classList.add('drag-over');
    }

    function handleDragLeave(e) {
        e.preventDefault();
        e.stopPropagation();
        e.target.closest('.upload-container').classList.remove('drag-over');
    }

    function handleDrop(e) {
        e.preventDefault();
        e.stopPropagation();
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            imageBlob = files[0];
        }
        e.target.closest('.upload-container').classList.remove('drag-over');
    }

    async function submitForm(event) {
        const formData = new FormData();
        formData.append('file', imageBlob);
        const response = await fetch('http://20.204.128.43:8000/predict', {
            method: 'POST',
            body: formData,
        });
        prediction = await response.json();
        console.log(prediction);

    }
</script>

<!-- <svelte:window on:load={startCamera} /> -->
<form on:submit|preventDefault={submitForm} class="flex flex-col items-center space-y-4">
    <!-- <video bind:this={video} autoplay></video>
    <canvas bind:this={canvas} width="640" height="480"></canvas> -->
    <!-- <button type="button" on:click={captureImage} class="px-4 py-2 bg-blue-500 text-white rounded">Capture</button> -->
    <div class="upload-container"
         on:dragover={handleDragOver}
         on:dragleave={handleDragLeave}
         on:drop={handleDrop}>
        <input type="file" id="fileInput" on:change={handleFileInputChange} class="file-input" />
        <label for="fileInput" class="file-input-label">
            <span>Choose a file or drag it here</span>
        </label>
        <!-- Display the uploaded image -->
        <img id="imagePreview" alt="Uploaded Image" class="my-4 w-64 h-64 object-cover hidden" />
    </div>
    <button type="submit" class="px-4 py-2 bg-green-500 text-white rounded">Upload</button>
</form>
{#if prediction}
    <div class="mt-4 text-lg font-bold px-28">
        <p>Predictions:</p>
        <ul class="list-disc pl-8 flex flex-col">
            <div>
                Leaf Blight: {prediction['blight']}
            </div>
            <div>
                Blast: {prediction['blast']}
            </div>
            <div>
                Brown Spot: {prediction['brownspot']}
            </div>
        </ul>
    </div>
{/if}
<style>
    .upload-container {
        @apply relative mt-8 w-96 h-72 border-2 border-dashed border-gray-300 rounded-lg flex justify-center items-center cursor-pointer;
    }

    .file-input {
        @apply hidden;
    }

    .file-input-label {
        @apply absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-center;
    }

    .file-input-label span {
        @apply text-base text-gray-600;
    }

    .file-input-label:hover {
        @apply bg-gray-100;
    }

    .file-input-label.drag-over {
        @apply bg-gray-200;
    }
</style>