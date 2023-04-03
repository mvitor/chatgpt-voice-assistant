import streamlit as st

import tempfile, json, openai, config, subprocess, argparse, os

from st_custom_components import st_audiorec

openai.api_key = config.OPENAI_API_KEY

parser = argparse.ArgumentParser()
parser.add_argument(
    "role",
    help="Role name",
    nargs="?",
    default="Terapeuta",
    const="Terapeuta",
    type=str,
)
args = parser.parse_args()
print (args)
messages = ""
with open("roles.json", "r") as f:
    data = json.load(f)
for role in data:
    if role["name"].lower() == args.role.lower():
        messages = [role]

if not messages:
   print (f"Provided role {role['name']} did not match any entry in roles file") 
wav_audio_data = st_audiorec()

col_info, col_space = st.columns([0.57, 0.43])
# with col_info:
#     st.write("\n")
#     st.write("\n")
#     st.write("Welcome!")
if wav_audio_data is not None:
    # display audio data as received on the backend
    print("Got a new Audio!")


    st.audio(wav_audio_data, format="audio/wav")
    audio_filename = f"{next((tempfile._get_candidate_names()))}.wav"
    with open(audio_filename, "bx") as file:
        file.write(wav_audio_data)
    audio_file = open(audio_filename, "rb")

    print("Querying Transcribe API")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    os.remove(audio_filename)
    print(f"\nTranscribe API response: {transcript['text']}")
    
    messages.append({"role": "user", "content": transcript["text"]})



    st.write(f"Pergunta:\n{transcript['text']}")
    print("Querying ChatCompletion API")
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    system_message = response["choices"][0]["message"]
    messages.append(system_message)
    print (f"messages: {messages}")

    st.write(f"Resposta:\n{system_message['content']}")
    print(f"Chatcompletion Response: {system_message['content']}")

    # Using separate script because in macos runAndWait is blocking the thread even with Threads
    subprocess.call(["python3", "pytts.py", system_message["content"]])
