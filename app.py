import streamlit as st
import cv2
import numpy as np
from PIL import Image
from ultralytics import YOLO
from translator import signs
from gtts import gTTS
import tempfile

st.title("🚦 AI Traffic Sign Detector")

language = st.selectbox(
"Select Language",
["English","Kannada","Tamil","Telugu","Malayalam"]
)

model = YOLO("yolov8n.pt", task="detect")

def speak(text):
    tts = gTTS(text=text)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(tmp.name)
    st.audio(tmp.name)

def detect(image):

    results = model(image)

    for r in results:
        for box in r.boxes:

            cls = int(box.cls[0])

            label = model.names[cls]

            return label

    return "unknown"

st.header("Upload Image")

uploaded = st.file_uploader("Upload Traffic Sign")

if uploaded:

    img = Image.open(uploaded)

    st.image(img)

    image = np.array(img)

    sign = detect(image)

    if sign in signs:
        output = signs[sign][language]
    else:
        output = sign

    st.subheader("Detected Sign")

    st.write(output)

    if st.button("🔊 Speak"):
        speak(output)

st.header("Live Camera")

camera = st.camera_input("Capture Traffic Sign")

if camera:

    img = Image.open(camera)

    st.image(img)

    image = np.array(img)

    sign = detect(image)

    if sign in signs:
        output = signs[sign][language]
    else:
        output = sign

    st.subheader("Detected Sign")

    st.write(output)

    if st.button("🔊 Speak Camera"):
        speak(output)
