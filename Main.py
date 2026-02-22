import flet as ft
import subprocess
import threading
import os
import yt_dlp

def main(page: ft.Page):
    page.title = "S25 Pro Downloader Cloud"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    # יצירת תיקיית ההורדות של השרת
    downloads_dir = os.path.join(os.getcwd(), "assets", "downloads")
    os.makedirs(downloads_dir, exist_ok=True)

    title = ft.Text("Nerias Cloud Downloader ☁️", size=30, weight="bold", color="blue")
    status_label = ft.Text("Status: Ready", size=18, weight="w500", color="grey")
    
    url_input = ft.TextField(label="YouTube URL", width=350, border_color="blue")
    
    file_type = ft.RadioGroup(content=ft.Row([
        ft.Radio(value="mp3", label="MP3"),
        ft.Radio(value="mp4", label="MP4")
    ], alignment=ft.MainAxisAlignment.CENTER), value="mp3")
    
    trim_switch = ft.Switch(label="Enable Trim (FFmpeg)", value=False)
    start_time = ft.TextField(label="Start (00:00)", width=160, visible=False, value="00:00")
    end_time = ft.TextField(label="End (01:00)", width=160, visible=False, value="01:00")
    
    def toggle_trim(e):
        start_time.visible = trim_switch.value
        end_time.visible = trim_switch.value
        page.update()
    trim_switch.on_change = toggle_trim
    
    download_btn = ft.ElevatedButton("Start Server Download", width=250, height=50, bgcolor="blue")
    save_device_btn = ft.ElevatedButton("📥 שמור במכשיר", width=250, height=50, bgcolor="green", visible=False)

    def run_download_task():
        try:
            ydl_opts = {
                'outtmpl': f'{downloads_dir}/%(title)s.%(ext)s',
                'nocheckcertificate': True,
                'format': 'bestaudio/best' if file_type.value == 'mp3' else 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
            }
            
            if file_type.value == 'mp3':
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            else:
                ydl_opts['merge_output_format'] = 'mp4'

            if trim_switch.value:
                ydl_opts['external_downloader'] = 'ffmpeg'
                ydl_opts['external_downloader_args'] = {'ffmpeg_i': ['-ss', start_time.value, '-to', end_time.value]}

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url_input.value, download=True)
                filename = ydl.prepare_filename(info)
                
                # התאמת סיומת הקובץ
                if file_type.value == 'mp3':
                    filename = filename.rsplit('.', 1)[0] + '.mp3'
                elif file_type.value == 'mp4' and not trim_switch.value:
                    filename = filename.rsplit('.', 1)[0] + '.mp4'

            # חילוץ שם הקובץ הסופי
            base_filename = os.path.basename(filename)
            
            status_label.value = "Status: SUCCESS! 🎉"
            status_label.color = "green"
            
            # הצגת הכפתור הירוק להורדה לטלפון
            save_device_btn.data = f"/downloads/{base_filename}"
            save_device_btn.visible = True
            
        except Exception as e:
            status_label.value = f"Status: FAILED ❌\n{str(e)}"
            status_label.color = "red"
        finally:
            download_btn.disabled = False
            page.update()

    def download_clicked(e):
        if not url_input.value:
            status_label.value = "Status: Error - No URL"
            status_label.color = "red"
            page.update()
            return

        download_btn.disabled = True
        save_device_btn.visible = False
        status_label.value = "Status: DOWNLOADING TO SERVER... ⏳"
        status_label.color = "yellow"
        page.update()
        threading.Thread(target=run_download_task).start()

    def save_to_device(e):
        page.launch_url(save_device_btn.data)

    save_device_btn.on_click = save_to_device
    download_btn.on_click = download_clicked

    page.add(
        title, url_input, ft.Text("Select Format:", size=16, weight="bold"), file_type, 
        ft.Divider(), trim_switch, ft.Row([start_time, end_time], alignment=ft.MainAxisAlignment.CENTER),
        download_btn, status_label, save_device_btn
    )

# הפעלת האפליקציה תוך חשיפת תיקיית assets כתיקייה ציבורית להורדות
ft.app(target=main, assets_dir="assets", port=int(os.getenv("PORT", 8080)), view=ft.AppView.WEB_BROWSER)
