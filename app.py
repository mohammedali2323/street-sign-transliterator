import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image
from streamlit_webrtc import webrtc_streamer
import av
from gtts import gTTS
import tempfile

# Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

st.title("Street Sign Transliterator")

st.write("Detect traffic signs, translate them, and hear the output")

# ---------------------------------
# LANGUAGE SELECTION
# ---------------------------------

language = st.selectbox(
"Select Preferred Language",
["English","Kannada","Tamil","Telugu","Malayalam"]
)

# ---------------------------------
# TRAFFIC SIGN DATASET
# ---------------------------------

signs = {

"Stop":{
"English":"Stop",
"Kannada":"ನಿಲ್ಲಿ",
"Tamil":"நிறுத்து",
"Telugu":"ఆపు",
"Malayalam":"നിർത്തുക"
},

"No U Turn":{
"English":"No U Turn",
"Kannada":"ಯು ಟರ್ನ್ ನಿಷೇಧ",
"Tamil":"யூ டர்ன் இல்லை",
"Telugu":"యూ టర్న్ లేదు",
"Malayalam":"യു ടേൺ നിരോധനം"
},

"No Left Turn":{
"English":"No Left Turn",
"Kannada":"ಎಡ ತಿರುವು ಬೇಡ",
"Tamil":"இடது திருப்பு இல்லை",
"Telugu":"ఎడమ మలుపు లేదు",
"Malayalam":"ഇടത് തിരിവ് ഇല്ല"
},

"No Parking":{
"English":"No Parking",
"Kannada":"ಪಾರ್ಕಿಂಗ್ ಇಲ್ಲ",
"Tamil":"பார்க்கிங் இல்லை",
"Telugu":"పార్కಿಂಗ್ లేదు",
"Malayalam":"പാർക്കിംഗ് ഇല്ല"
},

"Speed Limit":{
"English":"Speed Limit",
"Kannada":"ವೇಗ ಮಿತಿ",
"Tamil":"வேக வரம்பு",
"Telugu":"వేగ పరిమితి",
"Malayalam":"വേഗ പരിധി"
},

"One Way":{
"English":"One Way",
"Kannada":"ಒಂದು ದಾರಿ",
"Tamil":"ஒரு வழி",
"Telugu":"ఒక ಮಾರ್ಗం",
"Malayalam":"ഒരു വഴി"
},

"No Horn":{
"English":"No Horn",
"Kannada":"ಹಾರ್ನ್ ಬೇಡ",
"Tamil":"ஹார்ன் இல்லை",
"Telugu":"హార్న్ వద్దు",
"Malayalam":"ഹോൺ ഇല്ല"
},

"Pedestrian Crossing":{
"English":"Pedestrian Crossing",
"Kannada":"ಪಾದಚಾರಿಗಳ ದಾಟು",
"Tamil":"பாதசாரி கடப்பு",
"Telugu":"పాదచారి దాటడం",
"Malayalam":"പാദചാരി കടവ്"
},

"School Ahead":{
"English":"School Ahead",
"Kannada":"ಮುಂದೆ ಶಾಲೆ",
"Tamil":"முன்னால் பள்ளி",
"Telugu":"ముందు పాఠశాల",
"Malayalam":"മുന്നിൽ സ്കൂൾ"
},

"Hospital Ahead":{
"English":"Hospital Ahead",
"Kannada":"ಮುಂದೆ ಆಸ್ಪತ್ರೆ",
"Tamil":"முன்னால் மருத்துவமனை",
"Telugu":"ముందు ఆసుపత్రి",
"Malayalam":"മുന്നിൽ ആശുപത്രಿ"
}

}

# ---------------------------------
# FUNCTION FOR VOICE OUTPUT
# ---------------------------------

def speak(text):

    tts = gTTS(text=text)

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")

    tts.save(tmp.name)

    st.audio(tmp.name)

# ---------------------------------
# IMAGE UPLOAD DETECTION
# ---------------------------------

st.header("Upload Traffic Sign")

uploaded = st.file_uploader("Upload Image")

if uploaded:

    img = Image.open(uploaded)

    st.image(img)

    image = np.array(img)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    text = pytesseract.image_to_string(gray)

    detected = "Unknown"

    for sign in signs:
        if sign.lower() in text.lower():
            detected = sign

    st.subheader("Detected Sign")

    st.write(detected)

    if detected != "Unknown":

        output = signs[detected][language]

        st.subheader("Translation")

        st.write(output)

        if st.button("🔊 Speak"):

            speak(output)

# ---------------------------------
# WEBCAM DETECTION
# ---------------------------------

st.header("Live Camera Detection")

class VideoProcessor:

    def recv(self, frame):

        img = frame.to_ndarray(format="bgr24")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        text = pytesseract.image_to_string(gray)

        detected = "Unknown"

        for sign in signs:
            if sign.lower() in text.lower():
                detected = sign

        if detected != "Unknown":

            display = signs[detected][language]

        else:

            display = "No Sign"

        cv2.putText(
            img,
            display,
            (30,50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,255,0),
            2
        )

        return av.VideoFrame.from_ndarray(img, format="bgr24")

webrtc_streamer(key="camera", video_processor_factory=VideoProcessor)