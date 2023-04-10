# importing the required libraries

from urlextract import URLExtract
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()
def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['name'] == selected_user]

    # Fetch the number of messages
    num_messages = df.shape[0]

    # Fetch the total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # Fetch the number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>'].shape[0]

    # Fetch the number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages,len(words),num_media_messages, len(links)

def most_busy_users(df):
    x = df['name'].value_counts().head(5)
    df = round((df['name'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','name':'percent'})
    return x,df

def create_wordcloud(selected_user,df):

    f = open(r"C:\Users\acer\OneDrive\Documents\Whatsapp Chat Analysis\stop_hinglish.txt",'r')
    stop_words = f.read()

    
    if selected_user != 'Overall':
        df = df[df['name'] == selected_user]

    temp = df[df['name'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>']

    # nested function for stopwords

    def remove_stop_words(message):
        Y = []
        for word in message.lower().split():
            if word not in stop_words:
                Y.append(word)
        return " ".join(Y)
    

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

# most common words

def most_common_words(selected_user,df):

    f = open(r"C:\Users\acer\OneDrive\Documents\Whatsapp Chat Analysis\stop_hinglish.txt",'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['name'] == selected_user]

    temp = df[df['name'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))

    return most_common_df

# Emoji Analysis

def emoji_helper(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['name'] == selected_user]

    emojis = []

    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['name'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['name'] == selected_user]

    daily_timeline = df.groupby('date_num').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['name'] == selected_user]

    return df['day_name'].value_counts()


def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['name'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['name'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap

    
    
