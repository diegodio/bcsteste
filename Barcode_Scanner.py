import cv2
import zbarlight
import streamlit as st

def barcode_scanner():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Find barcodes in the image
        codes = zbarlight.scan_codes(['qrcode'], gray)

        # Decode the barcode data
        if codes:
            for code in codes:
                barcode_data = code.data.decode('utf-8')
                st.write(f"Barcode Data: {barcode_data}")

        # Display the video frame
        st.image(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    barcode_scanner()