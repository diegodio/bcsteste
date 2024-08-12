import av
import cv2
import streamlit as st 
from pyzbar.pyzbar import decode
from streamlit_webrtc import (webrtc_streamer, VideoProcessorBase,WebRtcMode)

def live_detection(play_state):

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
            return av.VideoFrame.from_ndarray(image, format="bgr24")

         else:

            self.barcode_val = result[0]
            play_state = False
            return av.VideoFrame.from_ndarray(annotated_image, format="bgr24")

   stream = webrtc_streamer(
         key="barcode-detection",
         mode=WebRtcMode.SENDRECV,
         desired_playing_state=play_state,
         video_processor_factory=BarcodeProcessor,
         media_stream_constraints={"video": True, "audio": False},
         async_processing=True,
      )

play_state = True
detected_barcode = live_detection(play_state)
