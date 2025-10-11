import speech_recognition as sr
from flask import Flask, request, jsonify, send_from_directory
from textblob import TextBlob
from googletrans import Translator
from pydub import AudioSegment
from moviepy.editor import VideoFileClip
from werkzeug.utils import secure_filename
from io import BytesIO
import os


app = Flask(__name__)
app.config['UPLOAD_FILE_FOLDER'] = 'upload-files'
app.config['PORT'] = 8801

# Ensure the upload and output directories exist
os.makedirs(app.config['UPLOAD_FILE_FOLDER'], exist_ok=True)

def convert_to_wav(audio_file):
    if audio_file.endswith('.mp3'):
        audio = AudioSegment.from_file(audio_file, format='mp3')
        wav_filename = os.path.splitext(audio_file)[0] + '.wav'
        audio.export(wav_filename, format='wav')
        return wav_filename
    elif audio_file.filename.endswith('.wav'):
        return audio_file.filename
    else:
        raise ValueError('Unsupported file format')
def speech_to_text(audio_file):
    recognizer = sr.Recognizer()
    try:
        audio_file_path = convert_to_wav(audio_file)
        with sr.AudioFile(audio_file_path) as source:
            audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
        return text
    except Exception as e:
        print("Error:", e)
        return 'Cannot recognize audio file'

@app.route('/api/speech-to-text', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Convert the audio file to WAV format
        audio = AudioSegment.from_file(BytesIO(file.read()))
        audio = audio.set_frame_rate(16000)
        wav_io = BytesIO()
        audio.export(wav_io, format="wav")
        wav_io.seek(0)

        # Use SpeechRecognition to transcribe the audio
        recognizer = sr.Recognizer()
        audio_file = sr.AudioFile(wav_io)
        with audio_file as source:
            audio_data = recognizer.record(source)
        
        # Recognize the speech in the audio
        text = recognizer.recognize_google(audio_data)
        return jsonify({"transcription": text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/v1/speech-to-text', methods=['POST'])
def speech_to_text_api():
    try:
        audio_file = request.files['audio']
        filename = secure_filename(audio_file.filename)
        audio_file_path = os.path.join(app.config['UPLOAD_FILE_FOLDER'], filename)
        audio_file.save(audio_file_path)
        text = speech_to_text(audio_file_path)
        return jsonify({'text': text})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/aai', methods=['POST'])
def speech_to_text_aai():
    try:
        audio_url = request.form.get('audio_url')
        
        aai.settings.api_key = 'KEY_AAI'
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_url)
        text = transcript.text
        return jsonify({'text': text})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/keywords', methods=['POST'])
def main_keywords():
    try:
        paragraph = request.form.get('text')
            # Create a TextBlob object
        blob = TextBlob(paragraph)
    
    # Extract noun phrases (main keywords) from the paragraph
        noun_phrases = blob.noun_phrases

    # Use a set to automatically remove duplicates
        unique_keywords = list(set(noun_phrases))
    
        return jsonify({'keywords': unique_keywords})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/translation', methods=['POST'])
def translate():
    try:
        content = request.form.get('content')
        language_code = request.form.get('languageCode')
        result = None
        if content is not None:
            translator = Translator()
            translated_content = translator.translate(content, dest=language_code)
            result = translated_content.text
        return jsonify({'text': result})
    except Exception as e:
        return jsonify({'text': 'The language code is not supported with {language_code}'.format(language_code=language_code)})


@app.route('/api/convert-video-to-audio', methods=['POST'])
def convert_video_to_audio():
    file = request.files['videoFile']
    file_name = secure_filename(file.filename)
    video_path = os.path.join(app.config['UPLOAD_FILE_FOLDER'], file_name)
    file.save(video_path)

    audio_filename = f"{os.path.splitext(file_name)[0]}.mp3"
    audio_path = os.path.join(app.config['UPLOAD_FILE_FOLDER'], audio_filename)

    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)

    return jsonify({'audio_url': f"http://103.75.186.174:{app.config['PORT']}/files/uploads/{audio_filename}"})

@app.route('/files/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FILE_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=app.config['PORT'])
