from youtube_dl import YoutubeDL

class Downloader:
    def __init__(self, link):
        self.link = link
    
    def download_video(self):
        ydl_opts = {
    'format': 'best'
}
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.link])  