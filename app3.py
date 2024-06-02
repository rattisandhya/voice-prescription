import streamlit as st
import speech_recognition as sr
import re
from email.message import EmailMessage
import smtplib
from moviepy.editor import VideoFileClip
def convert_audio_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.RequestError as e:
            st.error(f"Error: {e}")
            return None

def prepare_prescription(text):
    medicine_pattern = r'tablet\s(\w+\s?\d+\s?\w*)\s(\d+)\s(day|days)?\s(after|before)\s(food|meal)?\s(morning|noon|afternoon|evening|night)'
    medicines = re.findall(medicine_pattern, text, re.IGNORECASE)
    prescription = "Prescription:\n"
    for medicine in medicines:
        name = medicine[0]
        timing = f"{medicine[1]} times a day"
        prescription += f"- {name}: {timing}\n"

    return prescription

def mp4_to_wav(ip,op):
    input_video_path = ip
    output_audio_path = op
    video_clip = VideoFileClip(input_video_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(output_audio_path)
    video_clip.close()
    audio_clip.close()
    return output_audio_path

def send_prescription_to_email(prescription, receiver_email):
    sender_email = "sandhyaratti03@gmail.com"  
    sender_password = "snnz ugym pmcb cvsj" 

    msg = EmailMessage()
    msg["Subject"] = "Your Prescription"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.set_content(prescription)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.send_message(msg)

    st.success("Prescription sent successfully!")

def main():
    st.title("Voice Prescription App")

    audio_file = st.file_uploader("Upload Audio File", type=["mp3", "wav"])
    video_file = st.file_uploader("Upload Video File", type=["mp4"])

    if audio_file:
        st.audio(audio_file, format="audio/wav")

        text = convert_audio_to_text(audio_file)


        st.subheader("Converted Text:")
        st.write(text)


        prescription = prepare_prescription(text)


        st.subheader("Prescription:")
        st.write(prescription)


        receiver_email = st.text_input("Enter Patient's Email")
        if st.button("Send Prescription"):
            if receiver_email:
                send_prescription_to_email(prescription, receiver_email)
                st.success("Prescription sent successfully!")
            else:
                st.error("Please enter the patient's email.")



if __name__ == "__main__":
    main()
