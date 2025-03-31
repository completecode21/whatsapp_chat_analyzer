import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")

uploded_file = st.sidebar.file_uploader("choose a file")
if uploded_file is not None:
    bytes_data = uploded_file.getvalue()
    # change the data into utf-8 string
    data = bytes_data.decode('utf-8')
    # st.text(data)


    # create a dataframe of uploded data
    df = preprocessor.preprocess(data)

    #showing  dataframe in streamlit
    # st.dataframe(df)



    #fetch unique user
    user_list = df['users'].unique().tolist()
    user_list.remove('group notification')
    user_list.sort()
    # add all users details
    user_list.insert(0,'Overall')

    #create select user box
    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    #stats area
    if st.sidebar.button('Show Analysis'):
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            # display the count
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            # display the count
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("URL Shared")
            st.title(num_links)

        #showing monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['messages'],color = 'green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        #showing daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['full_date'], daily_timeline['messages'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

         #Activity Map
        st.title("Activity Map")

        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user,df)

            fig,ax  = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)

            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color = 'orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_activity_heatmap = helper.activity_heatmap(selected_user,df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_activity_heatmap)
        st.pyplot(fig)


        #finding the busiest user in the group(Group Level)
        if selected_user == 'Overall':
            st.title("Most Busy Users")
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()


            col1, col2, = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')

                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)


        #create word cloud
        st.title("Word Cloud")
        df_wc = helper.create_word_cloud(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)


        #most  common words
        st.title("Most Common Words")
        most_common_df = helper.most_common_words(selected_user,df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='horizontal')
        st.pyplot(fig)
        # st.dataframe(most_common_df)

        # emoji analysis
        st.title("Emoji Analysis")
        try:
            emoji_df = helper.emoji_count(selected_user, df)

            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(emoji_df)
            with col2:
                fig, ax = plt.subplots()
                ax.pie(emoji_df[1], labels=emoji_df[0], autopct='%0.2f')
                st.pyplot(fig)
        except Exception as ValueError:
            st.subheader("Emojis Are Not Shared!")