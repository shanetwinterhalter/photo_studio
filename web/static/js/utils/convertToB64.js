export function getMaskBase64(mask) {
    const uint8Array = new Uint8Array(mask.map(x => x ? 1 : 0));

    const chunkSize = 8192;
    const binaryChunks = [];

    for (let i = 0; i < uint8Array.length; i += chunkSize) {
        const chunk = uint8Array.slice(i, i + chunkSize);
        const binaryString = String.fromCharCode.apply(null, chunk);
        binaryChunks.push(binaryString);
    }

    const encoder = new TextEncoder();
    const concatenatedChunks = binaryChunks.reduce((acc, binaryString) => acc + binaryString, '');
    const uint8ArrayEncoded = encoder.encode(concatenatedChunks);

    const base64Encoded = window.btoa(String.fromCharCode.apply(null, uint8ArrayEncoded));
    return base64Encoded;
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
