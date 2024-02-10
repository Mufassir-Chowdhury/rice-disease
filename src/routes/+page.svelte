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
    <input type="file" on:change={e => imageBlob = e.target.files[0]} class="py-2" />
    <button type="submit" class="px-4 py-2 bg-green-500 text-white rounded">Submit</button>
</form>
<p class="mt-4 text-lg font-bold">{JSON.stringify(prediction, null, 2)}</p>