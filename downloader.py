from youtube_dl import YoutubeDL

class Downloader:
    def __init__(self, link):
        self.link = link
        self.downloaded_path = None
    
    def download_video(self):
        ydl_opts = {
            'format': 'best',
            'outtmpl': '%(title)s.%(ext)s',  # Template for the output filename
        }
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(self.link, download=True)
            if 'entries' in info_dict:
                video_info = info_dict['entries'][0]
                print("Video Info", video_info)
            else:
                video_info = info_dict
            self.downloaded_path = ydl.prepare_filename(video_info)
            print("downloaded path", self.downloaded_path)
            return True
