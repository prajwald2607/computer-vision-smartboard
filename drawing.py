import streamlit as st
import cv2
import numpy as np
from collections import deque

# Default called trackbar function
def set_values(x):
    print("")

# Creating the trackbars needed for adjusting the marker colour
st.sidebar.title("Color Detectors")
upper_hue = st.sidebar.slider("Upper Hue", 0, 180, 153, step=1, key="uh")
upper_saturation = st.sidebar.slider("Upper Saturation", 0, 255, 255, step=1, key="us")
upper_value = st.sidebar.slider("Upper Value", 0, 255, 255, step=1, key="uv")
lower_hue = st.sidebar.slider("Lower Hue", 0, 180, 64, step=1, key="lh")
lower_saturation = st.sidebar.slider("Lower Saturation", 0, 255, 72, step=1, key="ls")
lower_value = st.sidebar.slider("Lower Value", 0, 255, 49, step=1, key="lv")

# Giving different arrays to handle colour points of different colour
bpoints = [deque(maxlen=1024)]
gpoints = [deque(maxlen=1024)]
rpoints = [deque(maxlen=1024)]
ypoints = [deque(maxlen=1024)]

# These indexes will be used to mark the points in particular arrays of specific colour
blue_index = 0
green_index = 0
red_index = 0
yellow_index = 0

# The kernel to be used for dilation purpose
kernel = np.ones((5, 5), np.uint8)

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
color_index = 0

# Here is code for Canvas setup
paint_window = np.zeros((471, 636, 3)) + 255
paint_window = cv2.rectangle(paint_window, (40, 1), (140, 65), (0, 0, 0), 2)
paint_window = cv2.rectangle(paint_window, (160, 1), (255, 65), colors[0], -1)
paint_window = cv2.rectangle(paint_window, (275, 1), (370, 65), colors[1], -1)
paint_window = cv2.rectangle(paint_window, (390, 1), (485, 65), colors[2], -1)
paint_window = cv2.rectangle(paint_window, (505, 1), (600, 65), colors[3], -1)

cv2.putText(paint_window, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
cv2.putText(paint_window, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paint_window, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paint_window, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paint_window, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 2, cv2.LINE_AA)
st.sidebar.image(paint_window, channels="BGR", use_column_width=True)

# Creating the main Streamlit app layout
st.title("Streamlit Drawing App")

# Loading the default webcam of PC
cap = cv2.VideoCapture(0)

# Function to get the current frame
def get_frame():
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    return frame

# Function to get the drawing window
def get_drawing_window():
    drawing_window = np.copy(paint_window)
    return drawing_window

# Keep looping
while True:
    frame = get_frame()
    drawing_window = get_drawing_window()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Your existing color tracking logic...

    # Display the frame and drawing window
    st.image(frame, channels="BGR", use_column_width=True, caption="Original Frame")
    st.image(drawing_window, channels="BGR", use_column_width=True, caption="Drawing Window")

    # If the 'q' key is pressed, stop the application
    if st.button("Quit"):
        break

# Release the camera and all resources
cap.release()
cv2.destroyAllWindows()
