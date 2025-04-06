from flask import Flask, request, jsonify
from flask_cors import CORS
import moviepy.editor as mp
from pydub import AudioSegment
import numpy as np
from sklearn.preprocessing import MinMaxScaler

app = Flask(__name__)
CORS(app)

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
    
    # For video, let’s do a simple comparison of frames at the start and end of the video
    first_frame = video.subclip(0, 2).get_frame(0)  # Get the first frame (2 seconds)
    last_frame = video.subclip(-2, 0).get_frame(0)  # Get the last frame (2 seconds)

    # Convert frames to grayscale and compare their histograms (for better comparison)
    first_frame_gray = np.mean(first_frame, axis=2)  # Convert to grayscale
    last_frame_gray = np.mean(last_frame, axis=2)  # Convert to grayscale

    if np.array_equal(first_frame_gray, last_frame_gray):
        return {'is_looped': True, 'message': 'Video has a loop.'}
    else:
        return {'is_looped': False, 'message': 'No loop detected in video.'}

def detect_audio_loop(file_path):
    # Load the audio file
    audio = AudioSegment.from_file(file_path)
    
    # Take first 10 seconds and last 10 seconds for comparison
    first_chunk = audio[:10000]  # First 10 seconds
    last_chunk = audio[-10000:]  # Last 10 seconds
    
    # Extract raw data for better comparison
    first_chunk_raw = np.array(first_chunk.get_array_of_samples())
    last_chunk_raw = np.array(last_chunk.get_array_of_samples())
    
    # Use MinMaxScaler to normalize the values before comparing (this helps with small differences)
    scaler = MinMaxScaler()
    first_chunk_scaled = scaler.fit_transform(first_chunk_raw.reshape(-1, 1))
    last_chunk_scaled = scaler.transform(last_chunk_raw.reshape(-1, 1))

    # Compare the scaled chunks
    if np.array_equal(first_chunk_scaled, last_chunk_scaled):
        return {'is_looped': True, 'message': 'Audio has a loop.'}
    else:
        return {'is_looped': False, 'message': 'No loop detected in audio.'}

if __name__ == '__main__':
    app.run(debug=True)
