export function getCanvasBase64() {
    // Create a new canvas with the native dimensions of the image
    const canvas = $("#canvas")[0];
    const img = $("#resultImage")[0];
    const nativeCanvas = document.createElement('canvas');
    nativeCanvas.width = img.naturalWidth;
    nativeCanvas.height = img.naturalHeight;
    const nativeCtx = nativeCanvas.getContext('2d');

    // Draw the scaled content from the original canvas onto the new canvas
    nativeCtx.drawImage(canvas, 0, 0, canvas.width, canvas.height, 0, 0, nativeCanvas.width, nativeCanvas.height);

    // Get the image data from the new canvas
    const imageData = nativeCtx.getImageData(0, 0, nativeCanvas.width, nativeCanvas.height).data;

    // Create a binary mask array from the image data
    const binaryMask = [];
    for (let i = 0; i < imageData.length; i += 4) {
        // Here, we consider a pixel colored if its red channel value is greater than 128
        binaryMask.push(imageData[i] > 128 ? 1 : 0);
    }

    // Convert the binary mask array to a Uint8Array
    const uint8Array = new Uint8Array(binaryMask);

    // Split the Uint8Array into smaller chunks and convert each chunk to a string
    const chunkSize = 8192;
    const binaryChunks = [];
    for (let i = 0; i < uint8Array.length; i += chunkSize) {
        const chunk = uint8Array.slice(i, i + chunkSize);
        const binaryString = String.fromCharCode.apply(null, chunk);
        binaryChunks.push(binaryString);
    }

    // Concatenate the binary chunks into a single string
    const concatenatedChunks = binaryChunks.join('');

    // Convert the concatenated string to a Base64 encoded string
    const base64DataUrl = btoa(concatenatedChunks);

    return base64DataUrl;
}

export function getImageBase64() {
    return new Promise((resolve, reject) => {
        const fileInput = document.getElementById("fileUpload");
        const file = fileInput.files[0];

        // Check user has uploaded file
        if (!file) {
            alert("Please select a file to upload");
            return;
        }

        // Check file is image file
        if (!/^image\/(jpe?g|png|gif)$/i.test(file.type)) {
            reject("Please select an image file (JPEG, PNG, or GIF)");
            return;
        }

        const reader = new FileReader();
        reader.onloadend = function () {
            const base64data = reader.result;
            resolve(base64data);
        }
        reader.onerror = function () {
            reject("Error reading file");
        }
        reader.readAsDataURL(file);
    });
}
