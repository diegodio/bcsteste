import streamlit as st
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, WebRtcMode

class BarcodeProcessor(VideoProcessorBase):
    def __init__(self):
        self.barcode_data = None

    def BarcodeReader(self, image):
        detected_barcodes = decode(image)
        for barcode in detected_barcodes:
            (x, y, w, h) = barcode.rect
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            self.barcode_data = barcode.data.decode('utf-8')
        return image

    def recv(self, frame):
        image = frame.to_ndarray(format="bgr24")
        annotated_image = self.BarcodeReader(image)
        return av.VideoFrame.from_ndarray(annotated_image, format="bgr24")

def main():
    st.title("Real-Time Barcode Scanner")
    webrtc_ctx = webrtc_streamer(
        key="barcode-scanner",
        mode=WebRtcMode.SENDRECV,
        video_processor_factory=BarcodeProcessor,
        media_stream_constraints={"video": True, "audio": False},
    )

    if webrtc_ctx.video_processor:
        barcode_data = webrtc_ctx.video_processor.barcode_data
        if barcode_data:
            st.write(f"Detected Barcode: {barcode_data}")

if __name__ == "__main__":
    main()
