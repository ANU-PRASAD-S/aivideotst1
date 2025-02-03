import streamlit as st
import os
from moviepy.editor import VideoClip, TextClip, CompositeVideoClip
import random
import requests
from io import BytesIO

# Placeholder for AI video generation logic (replace with actual AI model integration)
def generate_ai_video(text, video_path):
    """Overlays text on a provided video clip."""

    try:
        clip = VideoClip(video_path)  # Use the downloaded video

        # ... (rest of the text overlay code is the same as before)
        import matplotlib.font_manager as fm
        available_fonts = [f.name for f in fm.fontManager.ttflist]
        random_font = random.choice(available_fonts) if available_fonts else "Arial"

        txt_clip = TextClip(text, fontsize=40, color="white", font=random_font).set_position("center")
        txt_clip = txt_clip.set_opacity(0.7)
        final_clip = CompositeVideoClip([clip, txt_clip.set_pos('center')])

        output_path = "generated_video.mp4"
        final_clip.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")

        return output_path

    except Exception as e:
        st.error(f"Error generating video: {e}")
        return None


def download_video(url, filename):
    """Downloads a video from a URL."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return filename

    except requests.exceptions.RequestException as e:
        st.error(f"Error downloading video: {e}")
        return None

# Streamlit app
st.title("AI Video Generator (Simulated)")

text_input = st.text_area("Enter text for the video:", "Your video text here")

# Video URL input
video_url = st.text_input("Enter the URL of a free video clip:", "")  # Or use a file uploader

if text_input and video_url:  # Check if both text and URL are provided
    if st.button("Generate Video"):
        video_filename = "downloaded_video.mp4"  # Temporary filename
        downloaded_path = download_video(video_url, video_filename)

        if downloaded_path:
            video_path = generate_ai_video(text_input, downloaded_path)

            if video_path:
                st.video(video_path)
                with open(video_path, "rb") as f:
                    st.download_button("Download Video", f, file_name="generated_video.mp4", mime="video/mp4")

            # Clean up the downloaded video (optional, but good practice)
            os.remove(downloaded_path)  # Handle potential errors

elif not text_input:
    st.warning("Please enter text for the video.")

elif not video_url:
    st.warning("Please enter a video URL.")
