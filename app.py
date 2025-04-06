from flask import Flask, request, jsonify
from flask_cors import CORS
import moviepy.editor as mp
from pydub import AudioSegment
import numpy as np

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from your frontend

@app.route('/process', methods=['POST'])
def process_file():
    file = request.files['file']
    file_path = 'temp_file'  # Save the uploaded file temporarily
    file.save(file_path)
    
    # Check if it's a video or audio file and process accordingly
    if file_path.endswith(('.mp4', '.mov', '.avi')):
        result = detect_video_loop(file_path)
    elif file_path.endswith(('.mp3', '.wav', '.flac')):
        result = detect_audio_loop(file_path)
    else:
        result = {'is_looped': False, 'message': 'Unsupported file type.'}
    
    return jsonify(result)

def detect_video_loop(file_path):
    # Load the video
    video = mp.VideoFileClip(file_path)
    
    # We will do a simple check by comparing the first 2 seconds with the last 2 seconds
    first_frame = video.subclip(0, 2).get_frame(0)
    last_frame = video.subclip(-2, 0).get_frame(0)
    
    # Compare frames for similarity
    if np.array_equal(first_frame, last_frame):
        return {'is_looped': True, 'message': 'Video has a loop.'}
    else:
        return {'is_looped': False, 'message': 'No loop detected in video.'}

def detect_audio_loop(file_path):
    # Load the audio file
    audio = AudioSegment.from_file(file_path)
    
    # Check if the first few seconds match the last few seconds
    first_chunk = audio[:5000]  # First 5 seconds
    last_chunk = audio[-5000:]  # Last 5 seconds
    
    # Compare audio chunks (this is a very simple comparison, you can make it more complex)
    if first_chunk == last_chunk:
        return {'is_looped': True, 'message': 'Audio has a loop.'}
    else:
        return {'is_looped': False, 'message': 'No loop detected in audio.'}

if __name__ == '__main__':
    app.run(debug=True)
