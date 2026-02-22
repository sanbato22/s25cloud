import flet as ft
import os
import threading
import time
import tempfile
import uuid

def main(page: ft.Page):
    page.title = "S25 Pro Downloader"
    page.theme_mode = "dark"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.padding = 20
    
    # משתנה לשמירת קובץ אחרון
    download_file = {"path": None, "name": None}
    
    status_text = ft.Text("Status: Ready", color="green", weight="bold", size=14)
    progress_text = ft.Text("", color="cyan", size=13, weight="bold")
    
    url_input = ft.TextField(
        label="YouTube URL", 
        width=350,
        height=55,
        border_color="blue",
        hint_text="Paste YouTube link here"
    )
    
    file_type = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="mp3", label="MP3 (Audio)"),
            ft.Radio(value="mp4", label="MP4 (Video)")
        ], alignment="center"), 
        value="mp3"
    )
    
    # Trim settings
    trim_switch = ft.Switch(label="Enable Trim", value=False)
    
    start_min = ft.TextField(label="Start (min)", width=70, keyboard_type=ft.KeyboardType.NUMBER, value="0", visible=False)
    start_sec = ft.TextField(label="Start (sec)", width=70, keyboard_type=ft.KeyboardType.NUMBER, value="0", visible=False)
    end_min = ft.TextField(label="End (min)", width=70, keyboard_type=ft.KeyboardType.NUMBER, value="1", visible=False)
    end_sec = ft.TextField(label="End (sec)", width=70, keyboard_type=ft.KeyboardType.NUMBER, value="0", visible=False)
    
    trim_inputs = ft.Row([
        start_min,
        ft.Text(":", size=14),
        start_sec,
        ft.Text("→", size=14),
        end_min,
        ft.Text(":", size=14),
        end_sec,
    ], alignment="center", visible=False)
    
    def toggle_trim(e):
        trim_inputs.visible = trim_switch.value
        start_min.visible = trim_switch.value
        start_sec.visible = trim_switch.value
        end_min.visible = trim_switch.value
        end_sec.visible = trim_switch.value
        page.update()
    
    trim_switch.on_change = toggle_trim

    download_btn = ft.ElevatedButton(
        "⬇️ Start Download", 
        width=250, 
        height=50,
        bgcolor="blue"
    )
    
    download_file_btn = ft.ElevatedButton(
        "💾 Download File",
        width=250,
        height=50,
        bgcolor="green",
        visible=False
    )

    def force_update():
        for _ in range(3):
            try:
                page.update()
                time.sleep(0.05)
            except:
                pass

    def run_download_task(url, format_type, do_trim, start_sec, end_sec):
        try:
            import yt_dlp
            
            # תיקייה זמנית
            temp_dir = tempfile.gettempdir()
            unique_id = str(uuid.uuid4())[:8]
            
            ydl_opts = {
                'outtmpl': f'{temp_dir}/{unique_id}_%(title)s.%(ext)s',
                'nocheckcertificate': True,
                'quiet': True,
                'no_warnings': True,
            }
            
            if format_type == "mp3":
                ydl_opts['format'] = 'bestaudio[ext=m4a]/bestaudio'
            else:
                ydl_opts['format'] = 'best[ext=mp4]/best'
            
            # Trim settings
            if do_trim:
                duration = end_sec - start_sec
                ydl_opts['postprocessor_args'] = {
                    'ffmpeg': ['-ss', str(start_sec), '-t', str(duration)]
                }

            status_text.value = "🚀 Downloading..."
            status_text.color = "orange"
            progress_text.value = "Please wait..."
            force_update()

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                
                if format_type == "mp3" and not filename.endswith('.m4a'):
                    filename = filename.rsplit('.', 1)[0] + '.m4a'
            
            # שמור נתיב הקובץ
            download_file["path"] = filename
            download_file["name"] = os.path.basename(filename)
            
            status_text.value = "✅ Ready to download!"
            status_text.color = "green"
            progress_text.value = f"File: {download_file['name']}"
            download_file_btn.visible = True
            
            force_update()
            
        except Exception as e:
            status_text.value = f"❌ Error!"
            status_text.color = "red"
            progress_text.value = str(e)[:100]
            force_update()
            
        finally:
            download_btn.disabled = False
            force_update()

    def on_download_click(e):
        if not url_input.value or not url_input.value.strip():
            status_text.value = "⚠️ Enter a URL!"
            status_text.color = "yellow"
            page.update()
            return
        
        url_to_download = url_input.value.strip()
        format_to_use = file_type.value
        do_trim = trim_switch.value
        
        start_sec = 0
        end_sec = 0
        if do_trim:
            try:
                start_sec = int(start_min.value or 0) * 60 + int(start_sec.value or 0)
                end_sec = int(end_min.value or 0) * 60 + int(end_sec.value or 0)
                
                if end_sec <= start_sec:
                    status_text.value = "⚠️ Invalid trim times!"
                    status_text.color = "red"
                    page.update()
                    return
            except:
                status_text.value = "⚠️ Invalid numbers!"
                status_text.color = "red"
                page.update()
                return
        
        download_btn.disabled = True
        download_file_btn.visible = False
        status_text.value = "🔄 Preparing..."
        progress_text.value = ""
        url_input.value = ""
        force_update()
        
        threading.Thread(
            target=run_download_task, 
            args=(url_to_download, format_to_use, do_trim, start_sec, end_sec),
            daemon=True
        ).start()

    def on_download_file_click(e):
        if download_file["path"] and os.path.exists(download_file["path"]):
            # יצירת קישור הורדה
            page.launch_url(f"file://{download_file['path']}")
        else:
            status_text.value = "❌ File not found!"
            status_text.color = "red"
            page.update()

    download_btn.on_click = on_download_click
    download_file_btn.on_click = on_download_file_click

    page.add(
        ft.Container(height=30),
        ft.Text("🎵 S25 Pro Downloader 🎬", size=22, weight="bold", color="blue"),
        ft.Text("YouTube to MP3/MP4 Converter", size=12, color="grey"),
        ft.Container(height=25),
        url_input,
        ft.Container(height=20),
        ft.Text("Select Format:", size=14, weight="bold"),
        ft.Container(height=5),
        file_type,
        ft.Container(height=15),
        trim_switch,
        ft.Container(height=5),
        trim_inputs,
        ft.Divider(height=25, color="blue"),
        download_btn,
        ft.Container(height=10),
        download_file_btn,
        ft.Container(height=20),
        progress_text,
        ft.Container(height=15),
        status_text,
        ft.Container(height=30),
    )

if __name__ == "__main__":
    ft.app(target=main, port=int(os.environ.get("PORT", 8080)))
