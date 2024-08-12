import av
import cv2
import zbarlight
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase

def process_frame(frame):
    image = frame.to_ndarray(format="bgr24")

    # Barcode detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    codes = zbarlight.scan_codes(['qrcode'], gray)

    if codes:
        for code in codes:
            barcode_data = code.data.decode('utf-8')
            st.write(f"Barcode Data: {barcode_data}")

    return av.VideoFrame.from_ndarray(image, format="bgr24")

webrtc_streamer(
    key="barcode-detection",
    video_processor_factory=process_frame,
)