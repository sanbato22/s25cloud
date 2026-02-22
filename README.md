# 🎵 S25 Pro Downloader

YouTube to MP3/MP4 converter with Trim support!

## ✨ Features
- Download YouTube videos as MP4
- Extract audio as MP3
- Trim videos (select start/end time)
- Clean, modern web interface
- **Works on any device!**

## 🚀 Deploy to Render (Free!)

### Method 1: Automatic (Easiest!)

1. **Fork this repo** to your GitHub
2. Go to [Render.com](https://render.com) and sign in with GitHub
3. Click **"New +"** → **"Web Service"**
4. Select your forked repo
5. Render will detect `render.yaml` automatically!
6. Click **"Apply"** → **"Create Web Service"**
7. Wait 3-5 minutes ⏳

**Done!** You'll get a URL like: `https://s25-downloader.onrender.com`

### Method 2: Manual

If automatic doesn't work:

1. **New Web Service** on Render
2. Connect your repo
3. Settings:
   - **Build Command**: 
     ```bash
     apt-get update && apt-get install -y ffmpeg && pip install -r requirements.txt
     ```
   - **Start Command**: `python main.py`
   - **Instance Type**: Free

## 💻 Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Install ffmpeg (if not installed)
# Windows: choco install ffmpeg
# Mac: brew install ffmpeg
# Linux: apt-get install ffmpeg

# Run
python main.py
```

Open: http://localhost:8080

## 📝 How to Use

1. Paste a YouTube URL
2. Choose format (MP3 or MP4)
3. (Optional) Enable Trim and set times
4. Click "Start Download"
5. Wait for processing
6. Click "Download File" when ready!

## ⚠️ Important Notes

- Files are temporarily stored on the server
- Free Render instances sleep after 15 min of inactivity
- First request after sleep takes ~30 seconds
- Maximum file size depends on Render's limits

## 🛠️ Tech Stack

- **Flet** - Python web framework
- **yt-dlp** - YouTube downloader
- **FFmpeg** - Video processing (for trim)

## 📜 License

MIT - Do whatever you want!

---

Made with ❤️ for easy YouTube downloads
