export const eventBus = document.createElement("div");

export function updateSegmentMask(mask) {
    eventBus.dispatchEvent(new CustomEvent("masksDataReceived", { detail: mask }));
}

export function loadMasksFromUrls(urls) {
    const maskPromises = urls.map(url => {
        return new Promise((resolve, reject) => {
            const maskImg = new Image();
            maskImg.src = url;

            // When the image is loaded, create a canvas and draw the image on it
            maskImg.onload = () => {
                const canvas = document.createElement('canvas');
                canvas.width = maskImg.width;
                canvas.height = maskImg.height;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(maskImg, 0, 0, canvas.width, canvas.height);

                // Convert canvas to only show mask areas
                const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
                const data = imageData.data;
                for (let i = 0; i < data.length; i += 4) {
                    if (data[i] < 128 && data[i + 1] < 128 && data[i + 2] < 128) {
                        data[i + 3] = 0;
                    }
                }
                ctx.putImageData(imageData, 0, 0);

                // Resolve the Promise with the created canvas
                resolve(canvas);
            };

            maskImg.onerror = () => {
                reject(new Error(`Failed to load mask image: ${url}`));
            };
        });
    });

    return Promise.all(maskPromises);
}

