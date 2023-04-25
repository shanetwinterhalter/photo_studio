import { brushMask, segmentMask } from './canvas.js'

export function getMask() {
    if (brushMask.length != segmentMask.length) {
        throw "Mask sizes do not match";
    }

    const result = [];
    for (let i = 0; i < brushMask.length; i++) {
        result[i] = brushMask[i] || segmentMask[i];
    }

    return result
}