import pandas as pd
import requests

def get_video_details(video_id, API_KEY):

    # collecting view, like, comment counts, duration of the video and the video definition
    
    # making the API call by the video id 
    url_video_stats = "https://www.googleapis.com/youtube/v3/videos?id=" + video_id + "&part=statistics,contentDetails&key=" + API_KEY
    response_video_stats = requests.get(url_video_stats).json() 

    view_count = response_video_stats['items'][0]['statistics']['viewCount']
    like_count = response_video_stats['items'][0]['statistics']['likeCount']
    comment_count = response_video_stats['items'][0]['statistics']['commentCount']
    duration_video = response_video_stats['items'][0]['contentDetails']['duration'] 
    video_definition = response_video_stats['items'][0]['contentDetails']['definition']
    
    return view_count, like_count, comment_count, duration_video, video_definition


def get_youtube_videos(df, API_KEY, CHANNEL_ID):
    
    pageToken = ""
    while True:
    
        # Making the API call        
        url = "https://www.googleapis.com/youtube/v3/search?key=" + API_KEY + "&channelId=" + CHANNEL_ID + "&part=snippet,id&order=date&maxResults=10000&" + pageToken
        response = requests.get(url).json()
        
        # collecting video id, title and upload date
        for i, video in enumerate(response['items']):
            
            if video['id']['kind'] == "youtube#video":
                
                video_id = video['id']['videoId']
                video_title = video['snippet']['title']
                video_title = str(video_title).replace("&amp;","")
                upload_date = video['snippet']['publishedAt']
                upload_date = str(upload_date).split("T")[0]
                view_count, like_count, comment_count, duration_count, video_definition = get_video_details(video_id, API_KEY)
                
                # making a row to the youtube DataFrame
                df.loc[i] = [
                    video_id,
                    video_title,
                    upload_date,
                    view_count,
                    like_count,
                    comment_count,
                    duration_count,
                    video_definition
                ]
                
        try:
            # To scroll through all possible pages of videos uploaded by the channel
            if response['nextPageToken'] != None:
                pageToken = "pageToken=" + response['nextPageToken']

        except:
            break

    return df

