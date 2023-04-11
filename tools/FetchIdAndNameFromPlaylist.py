import csv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Your API key here. Replace with your own Google API key.
API_KEY = 'YOUR_API_KEY'

def get_playlist_videos(playlist_id):
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    # Get the list of videos in the playlist
    videos = []
    next_page_token = None

    while True:
        try:
            response = youtube.playlistItems().list(
                part='snippet',
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token
            ).execute()

            for item in response['items']:
                video_id = item['snippet']['resourceId']['videoId']
                video_title = item['snippet']['title']
                videos.append((video_title, video_id))

            next_page_token = response.get('nextPageToken')
            if next_page_token is None:
                break
        except HttpError as e:
            print(f"An HTTP error {e.resp.status} occurred: {e.content}")
            break

    return videos

def save_to_csv(videos, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Title', 'Video ID'])
        writer.writerows(videos)

def main():
    playlist_id = 'YOUR_PLAYLIST_ID'  # Replace with the desired playlist ID
    output_file = 'playlist_videos.csv'

    videos = get_playlist_videos(playlist_id)
    save_to_csv(videos, output_file)
    print(f"Playlist video data saved to {output_file}")

if __name__ == '__main__':
    main()
