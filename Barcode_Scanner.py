import av
import cv2
import time
import streamlit as st 
from pyzbar.pyzbar import decode
from streamlit_webrtc import (webrtc_streamer, VideoProcessorBase,WebRtcMode)

st.set_page_config(layout="wide")

def live_detection(play_state):

   c1, c2 = st.columns(2)
   class BarcodeProcessor(VideoProcessorBase):

      def __init__(self) -> None:
         self.barcode_val = False
      
      def BarcodeReader(self, image):
         detectedBarcodes = decode(image)
         if not detectedBarcodes:
            print("\n No barcode! \n")
            return image, False

         else:
            for barcode in detectedBarcodes: 
               (x, y, w, h) = barcode.rect
               cv2.rectangle(image, (x-10, y-10),
                              (x + w+10, y + h+10),
                              (0, 255, 0), 2)

            if detectedBarcodes[0] != "":
               return image, detectedBarcodes[0]


      def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
         image = frame.to_ndarray(format="bgr24")

         annotated_image, result = self.BarcodeReader(image)

         if result == False:
            return av.VideoFrame.from_ndarray(annotated_image, format="bgr24")
         else:
            self.barcode_val = result[0]
            return av.VideoFrame.from_ndarray(annotated_image, format="bgr24")

   stream = webrtc_streamer(
         key="barcode-detection",
         mode=WebRtcMode.SENDRECV,
         desired_playing_state=play_state,
         video_processor_factory=BarcodeProcessor,
         media_stream_constraints={"video": True, "audio": False},
         async_processing=True,
      )

   while True:
      if stream.video_processor.barcode_val != False:
         barcode = stream.video_processor.barcode_val
         print("FOUND")
         c1.subheader(barcode)
         del stream

play_state = True

possible_barcode = live_detection(play_state)
