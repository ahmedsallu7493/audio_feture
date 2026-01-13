from flask import Flask, request, Response, jsonify
import yt_dlp
import time

app = Flask(__name__)

RATE_LIMIT = 15
WINDOW = 3600  # 1 hour
ip_requests = {}

def check_rate_limit(ip):
    now = time.time()
    requests = ip_requests.get(ip, [])
    requests = [t for t in requests if now - t < WINDOW]

    if len(requests) >= RATE_LIMIT:
        return False

    requests.append(now)
    ip_requests[ip] = requests
    return True


@app.route("/download", methods=["POST"])
def download():
    ip = request.remote_addr

    if not check_rate_limit(ip):
        return jsonify({"error": "Rate limit exceeded (15/hour)"}), 429

    url = request.json.get("url")
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "noplaylist": True,
        "outtmpl": "-",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

    def stream():
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    return Response(stream(), mimetype="audio/mpeg")


@app.route("/")
def home():
    return render_template("index.html")
