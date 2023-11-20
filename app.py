import streamlit as st
import matplotlib.pyplot as plt
import preprocessor, helper
import seaborn as sns

st.sidebar.title("Chat-Insights")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8") # bit stream to string
    # st.text(data)
    df = preprocessor.preprocess(data)

    st.dataframe(df)


    # Search the texts with word input
    st.title('Search messages with a word')
    # Create a text input for search
    search_term = ""
    search_term = st.text_input("Enter search term:")
    # Display the search term
    if search_term!="":
        st.write("Here are the texts with searched word:")
    for s in df['message']:
        if search_term!="" and s.find(search_term) != -1:
            st.text(s)


    # fetch unique users
    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    # stats area
    if st.sidebar.button("Show Analysis"):
        
        st.title("Top Statistics")

        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Total Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Total Links Shared")
            st.title(num_links)
        
        # monthly timeline
        st.heading("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()

        plt.plot(timeline['time'],timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.heading("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user,df)
        fig,ax = plt.subplots()

        plt.plot(daily_timeline['only_date'],daily_timeline['message'],color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        # activity map

        st.heading('Activity Map')
        col1,col2 = st.columns(2)

        with col1:
            st.title("Most Busy Day")
            col11, col22 = st.columns(2)
            with col11:
                year_list=timeline['year'].unique().tolist()
                year = st.selectbox(
                'Choose Year ',year_list,key="year_list")
            with col22:
                k=['January','February','March','April','May','June','July','August','September','October','November','December']
                month= st.selectbox(
                'Choose Month ',k,key="m_list")

            b=helper.solve2(df,year,month)
            print(b)
            fig,ax=plt.subplots()
            keys = [key for key in b.keys()]
            values = [value for value in b.values()]
            ax.bar(keys, [value[0] if len(value) == 1 else 0 for value in values],
               width=0.5,color='b')
            plt.xticks(rotation='vertical')
            st.pyplot(fig) 

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.heading("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)


        # finding the busiest user in the group
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # WordCloud
        st.heading('WordCloud')
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        plt.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        most_common_df = helper.most_common_words(selected_user,df)

        fig,ax = plt.subplots()

        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')

        st.title('Most Common Words')
        st.pyplot(fig)

        # emoji analysis
        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(5),labels=emoji_df[0].head(5), autopct="%0.2f")
            st.pyplot(fig)









    