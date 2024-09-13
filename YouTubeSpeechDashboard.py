import pandas as pd
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State
import plotly.express as px
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from TranscriptGetter import get_transcript_info

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

app.layout = html.Div(

    dbc.Container([

        dcc.Store(id='api-key-store'),

        dbc.Row([
            dbc.Col([
                html.H2("YouTube Channel Speech Analyzer", className="text-center fs-1 mt-3")
            ])
        ]),
        dbc.Row([
            dbc.Col(
                html.Img(src="https://upload.wikimedia.org/wikipedia/commons/e/ef/Youtube_logo.png", height="70px")
                , width=1, className="px-0 mx-0"),
            dbc.Col(
                dcc.Input(id="input", type="text",  # value="renhelsing",
                          placeholder="Type a YouTube channel name (case sensitive) to learn more...",
                          debounce=True, style={"width": "100%", "height": "100%"}), width=7, className="px-0 mx-0")
        ], style={"height": "10vh"}, justify="center", className="mt-3"),
        dbc.Row([
            dbc.Col(
                dbc.Modal(  # makes a pop-up prompting user to enter their api key to be used
                    id='api-key-modal',
                    children=[
                        dbc.Container([

                            dbc.Row(
                                html.H3("Welcome to the Youtube Speech Analysis Dashboard!", className="text-center")
                            ),
                            dbc.Row(
                                html.H4("Enter a Google YouTube API Key to Get Started", className="text-center")
                            ),
                            dbc.Row(
                                dcc.Input(id='api-key-input', type='password', placeholder='Enter your API key',
                                          n_submit=0, debounce=0),
                            )
                        ])
                    ],
                    is_open=True,  # Modal is visible by default
                    size="lg"
                ))
        ]),
        dbc.Row([
            dbc.Col(
                dbc.Modal(  # makes a pop-up telling user that they did not enter a valid chanel name
                    id='invalid-user-modal',
                    children=[
                        dbc.Container([
                            dbc.Row([
                                html.H3("Invalid Username Entered", className="text-center"),
                                html.H4("Please try again", className="text-center")
                            ]),
                        ])
                    ],
                    is_open=False,  # Modal is invisible by default
                    size="lg"
                ))
        ]),
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H6("% Videos W/O Transcripts", className="card-title text-center"),
                        html.H3(id="percent_unavailable", children={}, className="text-center"),
                    ]),
                    dbc.CardFooter(
                        html.H6("Videos W/O Transcripts are Not Considered")
                    )
                ]), width=3, className="mr-3"
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H6("Avg Words per Minute", className="card-title text-center"),
                        html.H3(id="average_wpm", children={}, className="text-center")
                    ]),
                    dbc.CardFooter([
                        dbc.Container([
                            dbc.Row([
                                dbc.Col(
                                    html.A(
                                        "Fastest Video",
                                        target="_blank",
                                        id="fastest-video",
                                        style={'color': 'red', 'textDecoration': 'underline', 'fontSize': '14px'},
                                        className="text-center"
                                    )
                                ),
                                dbc.Col(
                                    html.A(
                                        "       Slowest Video",
                                        target="_blank",
                                        id="slowest-video",
                                        style={'color': 'red', 'textDecoration': 'underline', 'fontSize': '14px'},
                                    ),
                                )
                            ], justify="center")
                        ])

                    ])
                ]), width=3, className="ml-3"
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H6("Avg Sentiment (-1 to 1)", className="card-title text-center"),
                        html.H3(id="sentiment_aggregate_score", children={}, className="text-center")
                    ]),
                    dbc.CardFooter([
                        # link to most negative video and most positive video

                        dbc.Container([
                            dbc.Row([
                                dbc.Col(
                                    html.A(
                                        "Most Positive Video   ",
                                        target="_blank",
                                        id="most-positive-video",
                                        style={'color': 'red', 'textDecoration': 'underline', 'fontSize': '14px'}
                                    ),
                                ),
                                dbc.Col(
                                    html.A(
                                        "Most Negative Video",
                                        target="_blank",
                                        id="most-negative-video",
                                        style={'color': 'red', 'textDecoration': 'underline', 'fontSize': '14px'}
                                    )
                                )
                            ])
                        ])
                    ])
                ]), width=3, className="mr-3"
            )
        ], className="mt-5", justify="center"),
        dbc.Row([
            dbc.Col(
                dcc.Graph(id='boxplot', config={'responsive': True}, figure={}, style={'height': "100%"}), width=6,
                style={"height": "75vh"}
            ),
            dbc.Col(
                dcc.Graph(id='sentiment_v_views', config={'responsive': True}, figure={}, style={'height': "100%"}),
                width=6, style={"height": "75vh"}
            )
        ], className="mt-5 mb-5", justify="center"),
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H6("Longest Word Used", className="card-title text-center"),
                        html.H3(id="longest_word", children={}, className="text-center")
                    ]),
                    dbc.CardFooter(
                        html.A("Video with Longest Word",
                               target="_blank",
                               id="longest-word-vid",
                               style={'color': 'red', 'textDecoration': 'underline', 'fontSize': '14px'},
                               ), className="text-center"
                    )
                ]), width=4
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H6("Swear Words per Video (Mean)", className="card-title text-center"),
                        html.H3(id="avg_swear_words", children={}, className="text-center")
                    ]),
                    dbc.CardFooter(
                        html.A("Video With Most Swear Words",
                               id="most-swear-words",
                               className="text-center",
                               style={'color': 'red', 'textDecoration': 'underline', 'fontSize': '14px'}
                               ),
                        className="text-center"
                    )
                ]), width=4
            )
        ], justify="center"),
        dbc.Row([
            dbc.Col(
                dcc.Graph(id='wordcounts', config={'responsive': True}, figure={}, style={'height': "100%"}),
                width=10
            )
        ], justify="center", className="mt-5")
    ],
        fluid=True, style={'background-color': '#EEEEEE'}), style={"overflowX": "hidden"}
)


@app.callback(
    [
        Output('boxplot', 'figure'),
        Output('wordcounts', 'figure'),
        Output("percent_unavailable", 'children'),
        Output("longest_word", 'children'),
        Output("longest-word-vid", 'href'),
        Output("avg_swear_words", 'children'),
        Output("most-swear-words", 'href'),
        Output("average_wpm", 'children'),
        Output("sentiment_aggregate_score", "children"),
        Output("sentiment_v_views", "figure"),
        Output("fastest-video", "href"),
        Output("slowest-video", "href"),
        Output("most-positive-video", "href"),
        Output("most-negative-video", "href"),
        Output('invalid-user-modal', 'is_open')],

    Input('input', 'value'),
    State('api-key-store', 'data'),
    prevent_initial_call=True
)
def create_graphs(channel_name, api_key):
    try:

        df = get_transcript_info(channel_name, api_key) if channel_name and api_key else None

        if df is None:  # when user enters invalid username, yielding an empty dataframe from function

            return (None, None, "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", None, "N/A", "N/A",
                    "N/A", "N/A", True)

        # Calculates the percentage of videos without a transcript, because videos without transcripts will not be
        # considered in this analysis
        videos_with_no_words = len(df[df["transcript"] == "Transcript not available"].values)
        percent_not_available = round((videos_with_no_words / df.shape[0]) * 100, 2)

        df = df[df["transcript"] != "Transcript not available"]
        df["views"] = df["views"].astype("int")
        df["likes"] = df["likes"].astype("int")
        df["duration_minutes"] = df["duration_minutes"].astype("int")
        df["date_published"] = pd.to_datetime(df["date_published"])
        df["number_swear_words"] = df["number_swear_words"].astype("int")
        df["year"] = df["date_published"].dt.year
        df['sentiment_score'] = pd.to_numeric(df['sentiment_score'], errors='coerce')

        # This block creates a list of every word spoken on the chanel by concatenating all the transcripts
        # and then splitting them
        all_words = ""
        for transcript in df["transcript"].values:
            all_words += transcript
        all_words = all_words.encode('utf-8', 'ignore').decode('utf-8', 'ignore').split(" ")

        def make_word_graph(all_words):

            """
            Makes a dictionary by looping through all_words where the key is a word and the value is the
            amount of times the word is used. To make results more interesting, words that were found
            in the top 500 of Google's Most Common English Words dataset were not included. I found this
            approach to be more effective at producing interesting results than using nltk.stopwords.

            The list of common english words does not include contractions. They are very common words
            so for the sake of finding more interesting words, I will filter these words out
            (list of contractions came from ChatGPT prompt)
            """

            # stores word as key and # of times used as values
            word_usage = {}

            # converting file of most common words to a list of the top 500 most common words
            with open("google-10000-english-usa.txt", "r") as most_common_english_words:
                most_common_english_words = most_common_english_words.readlines()

                for i in range(0, len(most_common_english_words)):
                    most_common_english_words[i] = most_common_english_words[i][:-1]
                most_common_english_words = most_common_english_words[:500]

            # used ChatGPT to write a list of common english contractions to be excluded
            english_contractions = ["arent", "cant", "couldnt", "didnt", "doesnt",
                                    "dont", "hadnt", "hasnt", "havent", "hed", "hell",
                                    "hes", "id", "ill", "im", "ive", "isnt", "itll",
                                    "its", "lets", "mightnt", "mustnt", "shed", "shell",
                                    "shes", "shouldnt", "thatll", "thats", "theres", "theyd",
                                    "theyll", "theyre", "theyve", "wasnt", "well", "were",
                                    "weve", "werent", "whatll", "whats", "wont", "wouldnt",
                                    "youd", "youll", "youre", "youve"]

            def is_ascii(word):
                """
                Used to check if a word only contains ASCII supported characters, returns true if
                all characters in a word have unicode numbers < 128, since those characters are
                ASCII supported. YouTube transcripts can often include characters that are not supported
                by ASCII, such as the musical note character.
                """
                return all(ord(char) < 128 for char in word)

            for word in all_words:
                if word.lower() not in most_common_english_words and word.lower() not in english_contractions and is_ascii(
                        word) and word not in ["", " ", "\n"]:
                    word_usage[word] = word_usage.get(word, 0) + 1

            most_common_words = pd.DataFrame(list(word_usage.items()), columns=['key', 'value']).sort_values("value",
                                                                                                             ascending=False)
            word_counts = px.histogram(most_common_words[:100], x="key", y="value", color_discrete_sequence=['red'])
            word_counts.update_layout(

                yaxis=dict(title="# of Times Used"),
                xaxis=dict(title="Words"),
                title=dict(text="Most Frequently Used Words", x=0.5)

            )

            return word_counts

        def make_box_graph():
            """
            Makes box plot by year with line graph overlay to compare the distribution of words per minute
            of videos to average views by year. This is to test if a certain speaking speed is better
            for video engagement or if simply keeping a consistent speaking speed is better for engagement
            """

            avg_views_df = df[["year", "views"]].groupby(by="year").mean()

            box_trace = go.Box(
                x=df['year'],
                y=df['words_per_min'],
                name="Words per Minute of Videos"
            )
            line_trace = go.Scatter(
                x=avg_views_df.index,
                y=avg_views_df['views'],
                name='Avg Views per Year',
                yaxis='y2'
            )

            box_plot = make_subplots(specs=[[{"secondary_y": True}]])
            box_plot.add_trace(box_trace)
            box_plot.add_trace(line_trace, secondary_y=True)

            box_plot.update_layout(
                legend=dict(
                    yanchor="top",
                    y=0.99,
                    xanchor="left",
                    x=0.01
                ),
                title={
                    'text': "Distribution of Videos by WPM by Year",
                    'y': 0.9,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'
                },
                yaxis=dict(title="Words per Minute"),
                yaxis2=dict(title="Average Views", overlaying="y", side="right"),
                xaxis=dict(
                    tickangle=40,
                    tickmode='array',
                    tickvals=list(avg_views_df.index),
                    ticktext=[str(year) for year in avg_views_df.index]  # Ensure x-axis ticks are integers
                ),
            )

            return box_plot

        def make_sentiment_graph():

            """
            Returns a bar graph with sentiment score on the x-axis and average views/likes on the y-axis.
            There is 2 bars for each sentiment score, one for the average # of views for that sentiment score
            and the other for the average # of likes for that sentiment score. Used to see if a certain sentiment
            score is more likely to produce better video statistics.
            """

            grouped_df = df[["sentiment_score", "likes", "views"]].groupby('sentiment_score').mean().reset_index()

            sentiment_engagement = go.Figure(data=[
                go.Bar(name='Views', x=grouped_df['sentiment_score'], y=grouped_df['views'], marker_color='#FF0000'),
                go.Bar(name='Likes', x=grouped_df['sentiment_score'], y=grouped_df['likes'], marker_color='#C4C4C4')
            ])

            sentiment_engagement.update_layout(
                title=dict(text='Views and Likes by Sentiment Score', x=0.5),
                xaxis_title='Sentiment Score',
                yaxis_title='Avg Views & Likes',
                barmode='group',
                legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01
                            )
            )

            return sentiment_engagement

        def longest_word():

            """
            Returns the longest word spoken on the channel as well as what video it is from
            """

            # Initialize with the first video's longest word and link
            longest_word = df.iloc[0]["longest_word"]
            vid_longest_word = df.iloc[0]["link"]

            # Iterate through each row using iloc method
            for i in range(1, len(df)):
                current_word = df.iloc[i]["longest_word"]
                if len(current_word) > len(longest_word):
                    longest_word = current_word
                    vid_longest_word = df.iloc[i]["link"]

            return longest_word, vid_longest_word

        avg_swear_words = round(df["number_swear_words"].mean(), 2)

        def most_swear_words():

            """
            Returns a link to video with most swear words
            """

            # Initialize with the first video's longest word and link
            max_swears = df.iloc[0]["number_swear_words"]
            vid_most_swears = df.iloc[0]["link"]

            # Iterate through each row using iloc
            for i in range(1, len(df)):

                if df.iloc[i]["number_swear_words"] > max_swears:
                    max_swears = df.iloc[i]["number_swear_words"]
                    vid_most_swears = df.iloc[i]["link"]

            return vid_most_swears

        def average_wpm():

            """Calculates the average words per minute across all videos"""

            return round(df["words_per_min"].mean(), 0)

        def average_sentiment():

            """Calculates the average sentiment score across all videos"""

            return round(df["sentiment_score"].mean(), 2)

        def fastest_video():

            """Returns link to video with the highest words per minute"""

            sorted_df = df.sort_values(by='words_per_min', ascending=False)
            return sorted_df.iloc[0]["link"]

        def slowest_video():

            """Returns link to video with the lowest words per minute"""

            sorted_df = df.sort_values(by='words_per_min', ascending=True)
            return sorted_df.iloc[0]["link"]

        def most_positive_video():

            """Returns link to video with the highest sentiment score"""

            sorted_df = df.sort_values(by='sentiment_score', ascending=False)
            return sorted_df.iloc[0]["link"]

        def most_negative_video():

            """Returns link to video with the lowest sentiment score"""

            sorted_df = df.sort_values(by='sentiment_score', ascending=True)
            return sorted_df.iloc[0]["link"]

        return (
        make_box_graph(), make_word_graph(all_words), percent_not_available, longest_word()[0], longest_word()[1],
        avg_swear_words, most_swear_words(), average_wpm(), average_sentiment(), make_sentiment_graph(),
        fastest_video(), slowest_video(), most_positive_video(), most_negative_video(), False)

    except Exception: # case where YouTube transcript api does not work (which can be common)

        return (go.Figure(), go.Figure(), "N/A", "N/A", "N/A", "N/A", "www.youtube.com",
                "N/A", "N/A", go.Figure(), "www.youtube.com", "www.youtube.com",
                "www.youtube.com", "www.youtube.com", False)


@app.callback(
    [Output('api-key-modal', 'is_open'),
     Output('api-key-store', 'data')],
    Input('api-key-input', 'n_submit'),
    State('api-key-input', 'value')
)
def submit_api_key(n_submit, api_key):
    """
        Removes the modal window from the Dash window if the user enters a YouTube API Key
    """
    if n_submit != 0 and api_key:  # Check if Enter is pressed and key is provided
        # Remove blur and close modal
        return False, api_key
    # Apply blur and keep modal open
    return True, dash.no_update


if __name__ == '__main__':
    app.run_server(debug=True, port=3000)
