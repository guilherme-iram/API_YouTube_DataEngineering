import pandas as pd
import requests
import re 


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


def get_youtube_videos(df, API_KEY, CHANNEL_ID, num_videos=10):
    
    pageToken = ""
    while True:
    
        # Making the API call        
        url = "https://www.googleapis.com/youtube/v3/search?key=" + API_KEY + "&channelId=" + CHANNEL_ID + f"&part=snippet,id&order=date&maxResults={num_videos}&" + pageToken
        response = requests.get(url).json()
        
        print(response)

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


from urllib.parse import urlparse, parse_qs

def get_channel_id_from_video_link(video_link, API_KEY):
    # Extrair o ID do vídeo do link
    parsed_url = urlparse(video_link)
    video_id = parse_qs(parsed_url.query).get('v')

    if video_id:
        video_id = video_id[0]
        # Fazer a chamada à API do YouTube para obter os detalhes do vídeo
        url_video_stats = "https://www.googleapis.com/youtube/v3/videos?id=" + video_id + "&part=snippet&key=" + API_KEY
        response_video_stats = requests.get(url_video_stats).json()

        if 'items' in response_video_stats:
            channel_id = response_video_stats['items'][0]['snippet']['channelId']
            return channel_id
        else:
            print("Não foi possível obter os detalhes do vídeo.")
    else:
        print("Link de vídeo inválido.")


def main():
    API_KEY = ""

    with open('API_key.txt') as api:
        API_KEY = api.readlines()[0]
    link_video = "https://www.youtube.com/watch?v=ssXEl6RNhrE&t=1s"
    channel_id = get_channel_id_from_video_link(link_video, API_KEY)

    print(channel_id)

if __name__ == "__main__":
    main()

