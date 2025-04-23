import requests


API_KEY = "AIzaSyDJgPiL-a4n5XJzYp-Ps8pvroup3nl49gI"
CHANNEL_ID = "UC0WP5P-ufpRfjbNrmOWwLBQ"  

channel_stats_url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={CHANNEL_ID}&key={API_KEY}"
channel_stats = requests.get(channel_stats_url).json()
subscribers = channel_stats["items"][0]["statistics"].get("subscriberCount", "Hidden")
print(f"\n👥 Subscribers: {subscribers}")


details_url = f"https://www.googleapis.com/youtube/v3/channels?part=contentDetails&id={CHANNEL_ID}&key={API_KEY}"
details_response = requests.get(details_url).json()
uploads_playlist_id = details_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]


video_ids = []
next_page_token = None

while True:
    playlist_url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults=50&playlistId={uploads_playlist_id}&key={API_KEY}"
    if next_page_token:
        playlist_url += f"&pageToken={next_page_token}"
    
    playlist_response = requests.get(playlist_url).json()
    for item in playlist_response["items"]:
        video_ids.append(item["contentDetails"]["videoId"])
    
    next_page_token = playlist_response.get("nextPageToken")
    if not next_page_token:
        break


videos_data = []

for i in range(0, len(video_ids), 50):  
    batch_ids = ",".join(video_ids[i:i+50])
    stats_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id={batch_ids}&key={API_KEY}"
    stats_response = requests.get(stats_url).json()
    
    for video in stats_response["items"]:
        stats = video["statistics"]
        snippet = video["snippet"]
        videos_data.append({
            "title": snippet["title"],
            "videoId": video["id"],
            "views": int(stats.get("viewCount", 0)),
            "likes": int(stats.get("likeCount", 0)),
        })


most_viewed = max(videos_data, key=lambda x: x["views"])
most_liked = max(videos_data, key=lambda x: x["likes"])


print("\n🔥 Most Viewed Video:")
print(f"Title: {most_viewed['title']}")
print(f"Views: {most_viewed['views']}")
print(f"Link: https://www.youtube.com/watch?v={most_viewed['videoId']}")

print("\n❤ Most Liked Video:")
print(f"Title: {most_liked['title']}")
print(f"Likes: {most_liked['likes']}")
print(f"Link: https://www.youtube.com/watch?v={most_liked['videoId']}")
