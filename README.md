# Youtube Speech Analysis Dashboard
A dashboard allowing you to analyze the speech patterns of your favorite YouTubers!


## Purpose

### The idea for this dashboard first came to me after viewing Data Time's YouTube video called "I analyzed all words on the Mr Beast Channel" (https://www.youtube.com/watch?v=lXeNZeLSsgY). Essentially, Data Time got access to all the transcripts of Mr Beast's published videos and did a textual analysis of them. I had the idea to broaden the scope of the insights that Data Time gathered from Mr Beast's channel to all YouTube channels with a user friendly interface.

## Data Collection and APIs

### In the file titled "TranscriptGetter.py", you will find the function used to gather information about every video for a requested YouTuber. The function uses the Google YouTube API to gather a list of video IDs for every YouTube video as well as to gather relevant statistics for each video, such as likes recieved, views recieved, video duration, and date published. The function then also implements the YouTube Transcript API (by github user: jdepoix). The YouTube Transcript API is used to gather the entire English transcript for each video.

### From the transcript, other statistics can be calculated such as the words per minute for the video (total words/duration(minutes)), the longest word used, the number of swear words in the video, and the overall sentiment score of the video (calculated using the Natural Language Toolkit (NLTK) library).

### The data is returned as a pandas dataframe like so:



