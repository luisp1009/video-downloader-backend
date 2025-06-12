from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import yt_dlp
import uuid
import os

app = Flask(__name__)
CORS(app)  # Allow requests from other domains (like Netlify)

@app.route("/")
def home():
    return "Backend is running."

@app.route("/download", methods=["POST"])
def download():
    try:
        data = request.get_json()
        url = data.get("url")

        if not url:
            return jsonify({"error": "Missing video URL"}), 400

        filename = f"{uuid.uuid4()}.mp4"

        ydl_opts = {
            'outtmpl': filename,
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        response = send_file(filename, as_attachment=True, download_name="video.mp4")

        # Optional: clean up the file after download
        @response.call_on_close
        def cleanup():
            try:
                os.remove(filename)
            except Exception:
                pass

        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
