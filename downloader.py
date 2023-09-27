import requests
from youtube_dl import YoutubeDL


class Downloader:
    def __init__(self, link):
        self.link = link
        self.downloaded_path = None
    
    async def download_youtube(self):
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
    
    async def download_instagram(self):
        
        url = "https://download-ig-videos.vercel.app/"

        payload = f"[\"{self.link}\"]"
        headers = {
  'authority': 'download-ig-videos.vercel.app',
  'accept': 'text/x-component',
  'accept-language': 'en-US,en;q=0.6',
  'content-type': 'text/plain;charset=UTF-8',
  'next-action': '2627efa1b8fdc3a3fc06d1fa89c5e9072ee9e54c',
  'next-router-state-tree': '%5B%22%22%2C%7B%22children%22%3A%5B%22__PAGE__%22%2C%7B%7D%5D%7D%2Cnull%2Cnull%2Ctrue%5D',
  'next-url': '/',
  'origin': 'https://download-ig-videos.vercel.app',
  'referer': 'https://download-ig-videos.vercel.app/',
  'sec-ch-ua': '"Brave";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'sec-gpc': '1',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
}

        response = requests.request("POST", url, headers=headers, data=payload)
        response = response.text.split('https')[1].replace("}", '').replace('"', '')
        download_link = "https"+response
        save_path = 'downloaded_video.mp4'  # Replace with your desired file path and name
        self.downloaded_path = save_path
        response_vid = requests.get(download_link, stream=True)
        # Open a file in binary write mode to save the video
        with open(save_path, 'wb') as video_file:
            # Iterate over the content of the response and write it to the file in chunks
            for chunk in response_vid.iter_content(chunk_size=1024):
                if chunk:
                    video_file.write(chunk)
