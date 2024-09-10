import time
import pandas as pd
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
import isodate
import string
import requests
from nltk.sentiment import SentimentIntensityAnalyzer
import numpy as np

def get_transcript_info(channel_name, api_key):
    """
    Retrieves video details and transcript analysis for a given YouTube channel.

    Args:
        channel_name (str): The name of the YouTube channel.
        api_key (str): YouTube API key.

    Returns:
        pd.DataFrame: DataFrame containing video stats, transcript details, and sentiment analysis.
    """

    # Create a resource object for interacting with the YouTube API
    youtube = build('youtube', 'v3', developerKey=api_key) # creating YouTube API object

    # Get channel details
    search_response = youtube.search().list(
        q=channel_name,
        part='snippet',
        type='channel',
        maxResults=1
    ).execute()

    # If the channel name is not valid
    if not search_response['items']:
        print("Channel not found.")
        return None

    # Get playlist ID of the channel's uploaded videos
    channel_id = search_response['items'][0]['id']['channelId']
    channels_response = youtube.channels().list(
        id=channel_id,
        part='contentDetails'
    ).execute()

    uploads_playlist_id = channels_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    # Get video IDs from the uploads playlist
    video_ids = []
    next_page_token = None
    while True:
        playlist_response = youtube.playlistItems().list(
            playlistId=uploads_playlist_id,
            part='contentDetails',
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        video_ids.extend([item['contentDetails']['videoId'] for item in playlist_response['items']])

        next_page_token = playlist_response.get('nextPageToken')
        if not next_page_token:
            break

    # Get video details
    video_details = []
    for i in range(0, len(video_ids), 50):

        video_response = youtube.videos().list(
            id=','.join(video_ids[i:i + 50]),
            part='snippet,contentDetails,statistics'
        ).execute()

        for item in video_response['items']:

            try:
                # retrieves the transcript of each video as a dictionary where "text" is the key that
                # gives the actual transcript text

                video_id = item['id']
                transcript = YouTubeTranscriptApi.get_transcript(video_id)

                #removing punctuation
                transcript_text = ''.join(
                    ch for ch in ' '.join([t['text'] for t in transcript]) if ch not in string.punctuation
                ).replace('\n', '')

                words = transcript_text.split(" ")
                num_words = len(words)

                swear_words = ["fuck", "shit",'bitch',"pussy","ass","bitch", "fucker","asshole","bullshit","cock",
                               "dammit", "damn", "damned", "dick", "dickhead", "dumbass", "fucking","goddamn","motherfucker",
                               "slut", "whore", "twat", "[\xa0__\xa0]", "[ __ ]"]

                # find the longest word
                longest_word = max(words, key=len, default="N/A")

                # find # swear words
                num_swear_words = sum(1 for word in words if word.lower() in swear_words)

                # initialize sentiment analyzer object and generates a sentiment score which is a dictionary
                # of scores. The value we are interested in is the compound score, which is an overall score
                # between -1 & 1 with -1 being the most negative and 1 being the most positive.

                sentiment_analyzer = SentimentIntensityAnalyzer()
                sentiment_score = sentiment_analyzer.polarity_scores(transcript_text)
                sentiment_score = sentiment_score["compound"]

            except Exception as e:

                transcript_text, num_words, longest_word, num_swear_words, sentiment_score = (
                    'Transcript not available', 0, "N/A", np.nan, np.nan)

            # converting duration from iso8 format into number of minutes for calculating words per minute
            duration_iso = item['contentDetails']['duration']
            duration_minutes = isodate.parse_duration(duration_iso).total_seconds() / 60

            # Adds entries (as a dictionary) to a list that will become dataframe
            video_details.append({
                'title': item['snippet']['title'],
                'date_published': item['snippet']['publishedAt'],
                'duration_minutes': duration_minutes,
                'views': item['statistics'].get('viewCount', 0),
                'likes': item['statistics'].get('likeCount', 0),
                'transcript': transcript_text,
                'words_per_min': num_words/duration_minutes if duration_minutes != 0 else 0,
                'longest_word': longest_word,
                'number_swear_words': num_swear_words,
                'sentiment_score': round(sentiment_score, 1),
                'video_id' : item['id'],
                'link' : "https://www.youtube.com/watch?v=" + str(item['id'])
            })
    return pd.DataFrame(video_details)


# get_transcript_info("aj4ty7vn", 'AIzaSyAcEwPGcKSEnCOCCb86knYAQjGIpIqjJGg').to_csv("lorenzo_transcript")





