import wave
import openai
# from docx import Document
from flask import Flask, request
import json
import os
audio_file_path = "test.wav"
# API_KEY =  "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"
API_KEY="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"
# OPENAI_ORG_NAME="org-RhrrHbjlD8YcWbT3FXb0ITwW"


app = Flask(__name__)
openai.api_key = API_KEY

@app.route('/health')
def health_check():
    # return json.loads({"status":200,"message": "success"})
    return "ok"

@app.route('/test')
def test_api():
    # return json.loads({"status":200,"message": "success"})
    return json.dumps({"status":"ok"})

@app.route('/processAudio',methods=["POST"])
def process_audio():
    print("audio process")
    response = {}
    print("request.form ", request.form)
    print("request.files ", request.files)
    try:
        request.files['file'].save('./temp.wav')
        response["statusCode"] = 200
        response["status"] = True
        response["message"] = "success"

        response["data"] = {}
        response["data"]["minutes"] = {
                "Summary_Meeting" : "Credit cards to be explained, bonus points are explained",
                "Action_Items" : "1. Send brochures\n2. Schedule meeting at 2 pm\n3.Webiste link to be shared",
                "Minutes_of_Meeting" : "Jade wants to apply for credit card on his salary and a card on his FD"
            }
    except Exception as e:
        response["statusCode"] = 500
        response["status"] = False
        response["message"] = str(e)
    finally:
        return json.dumps(response)

def get_minutes(): 
    transcription = transcribe_audio(audio_file_path)
    minutes = meeting_minutes(transcription)
    return json.dumps({"minutes":minutes})

def transcribe_audio(audio_file_path):
    with open(audio_file_path, 'rb') as audio_file:
        transcription = openai.Audio.transcribe("whisper-1", audio_file)
    return transcription['text']

def meeting_minutes(transcription):
    # abstract_summary = abstract_summary_extraction(transcription)
    # key_points = key_points_extraction(transcription)
    action_items = action_item_extraction(transcription)
    # sentiment = sentiment_analysis(transcription)
    return {
        # 'abstract_summary': abstract_summary,
        # 'key_points': key_points,
        'action_items': action_items,
        # 'sentiment': sentiment
    }

def abstract_summary_extraction(transcription):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "You are a highly skilled AI trained in language comprehension and summarization. I would like you to read the following text and summarize it into a concise abstract paragraph. Aim to retain the most important points, providing a coherent and readable summary that could help a person understand the main points of the discussion without needing to read the entire text. Please avoid unnecessary details or tangential points."
            },
            {
                "role": "user",
                "content": transcription
            }
        ]
    )
    return response['choices'][0]['message']['content']


def key_points_extraction(transcription):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "You are a proficient AI with a specialty in distilling information into key points. Based on the following text, identify and list the main points that were discussed or brought up. These should be the most important ideas, findings, or topics that are crucial to the essence of the discussion. Your goal is to provide a list that someone could read to quickly understand what was talked about."
            },
            {
                "role": "user",
                "content": transcription
            }
        ]
    )
    return response['choices'][0]['message']['content']


def action_item_extraction(transcription):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "You are an AI expert in analyzing conversations and extracting action items. Please review the text and identify any tasks, assignments, or actions that were agreed upon or mentioned as needing to be done. These could be tasks assigned to specific individuals, or general actions that the group has decided to take. Please list these action items clearly and concisely."
            },
            {
                "role": "user",
                "content": transcription
            }
        ]
    )
    return response['choices'][0]['message']['content']

def sentiment_analysis(transcription):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "As an AI with expertise in language and emotion analysis, your task is to analyze the sentiment of the following text. Please consider the overall tone of the discussion, the emotion conveyed by the language used, and the context in which words and phrases are used. Indicate whether the sentiment is generally positive, negative, or neutral, and provide brief explanations for your analysis where possible."
            },
            {
                "role": "user",
                "content": transcription
            }
        ]
    )
    return response['choices'][0]['message']['content']

# def save_as_docx(minutes, filename):
#     doc = Document()
#     for key, value in minutes.items():
#         # Replace underscores with spaces and capitalize each word for the heading
#         heading = ' '.join(word.capitalize() for word in key.split('_'))
#         doc.add_heading(heading, level=1)
#         doc.add_paragraph(value)
#         # Add a line break between sections
#         doc.add_paragraph()
#     doc.save(filename)


   
# transcription = transcribe_audio(audio_file_path)
# minutes = meeting_minutes(transcription)
# print(minutes)

# save_as_docx(minutes, 'meeting_minutes.docx')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001,debug=True)