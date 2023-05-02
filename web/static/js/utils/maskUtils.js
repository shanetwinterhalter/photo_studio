export const eventBus = document.createElement("div");

export function updateSegmentMask(mask) {
    eventBus.dispatchEvent(new CustomEvent("masksDataReceived", { detail: mask }));
}
