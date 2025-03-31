from collections import Counter

import emoji
import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud

extract = URLExtract()
def fetch_stats(selected_user, df):

    #when we select only 'overall'
    # if selected_user == 'Overall':
    #     # 1. fetch number of messages
    #     num_messages = df.shape[0]
    #     # 2. fetch number of words
    #     words = []
    #     for message in df['messages']:
    #         words.extend(message.split())
    #
    #     return num_messages, len(words)
    # # when we select any particular user
    # else:
    #     new_df = df[df['users'] == selected_user]
    #     new_messages = new_df.shape[0]
    #     words = []
    #     for message in new_df['messages']:
    #         words.extend(message.split())
    #
    #     return new_messages, len(words)

    if selected_user != 'Overall':

        df = df[df['users'] == selected_user]

    # total number of messages
    num_messages = df.shape[0]
    # total number of words
    words = []
    for message in df['messages']:
        words.extend(message.split())

    # total number of media shared
    num_media_messages = df[df['messages'] == "<Media omitted>\n"].shape[0]

    # fetch total number of links shared
    num_links =[]
    for message in df['messages']:
        num_links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(num_links)


def most_busy_users(df):
    x = df['users'].value_counts().head()
    df = round((df['users'].value_counts()/df.shape[0]) * 100, 2).reset_index().rename(columns={'index':'name','user':'percent'})

    return  x,df



# def create_word_cloud(selected_user,df):
#     f = open('stop_hinglish.txt', 'r')
#     stop_word = f.read()
#     if selected_user != 'Overall':
#         df = df[df['users'] == selected_user]
#     # remove group notification
#     temp = df[df['users'] != 'group notification']
#     # remove media ommitied
#     temp = temp[temp['messages'] != '<Media omitted>\n']

def create_word_cloud(selected_user,df):
    f = open('stop_hinglish.txt', 'r')
    stop_word = f.read()
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    # remove group notification
    temp = df[df['users'] != 'group notification']
    # remove media ommitied
    temp = temp[temp['messages'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y =[]
        for word in message.lower().split():
            if word not in stop_word:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500,height=500,min_font_size=20,background_color='white')
    temp['messages'] = temp['messages'].apply(remove_stop_words)
    df_wc = wc.generate(temp['messages'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user,df):
    # remove hinglish stop words
    f = open('stop_hinglish.txt', 'r')
    stop_word = f.read()

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    # remove group notification
    temp = df[df['users'] != 'group notification']
    # remove media ommitied
    temp = temp[temp['messages'] != '<Media omitted>\n']
    words = []
    for message in temp['messages']:
        for word in message.lower().split():
            if word not in stop_word:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return  most_common_df


def emoji_count(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    emojis = []
    for message in df['messages']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df




def monthly_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['messages'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time

    return timeline



def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return_daily_timeline = df.groupby('full_date').count()['messages'].reset_index()

    return return_daily_timeline



def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['day_name'].value_counts()


def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['month'].value_counts()



def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    user_activity_heatmap = df.pivot_table(index='day_name',columns='hour_period',values='messages',aggfunc='count').fillna(0)

    return user_activity_heatmap