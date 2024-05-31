import streamlit as st
import preprocess
import helper
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns

# Page title and sidebar branding
st.sidebar.title("WhatsApp Chat Analyzer")
st.sidebar.title("by CJ KONWAR")
st.title("WhatsApp Chat Analyzer")

# File uploader for selecting chat data
uploader_file = st.sidebar.file_uploader("Choose a file")
if uploader_file is not None:
    bytes_data = uploader_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocess.preprocess(data)

    # List of users for analysis
    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0, "Overall")
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):
        # Fetching stats
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

        # Displaying top statistics
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Messages", num_messages)
        with col2:
            st.metric("Total Words", words)
        with col3:
            st.metric("Media Shared", num_media_messages)
        with col4:
            st.metric("Links Shared", num_links)

        # Adding borders around statistics section
        st.markdown('<hr style="border: 1px solid #008080;">', unsafe_allow_html=True)

        # Monthly timeline
        timeline = helper.monthly_timeline(selected_user, df)
        fig = px.line(timeline, x='time', y='message', labels={'time': 'Time', 'message': 'Messages'})
        fig.update_layout(xaxis_tickangle=-90)
        st.title("Monthly Timeline")
        st.plotly_chart(fig)

        # Adding borders around timeline section
        st.markdown('<hr style="border: 1px solid #008080;">', unsafe_allow_html=True)

        # Daily timeline
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=daily_timeline['only_date'], y=daily_timeline['message'], mode='lines+markers',
                                 line=dict(color='blue'), name='Messages'))
        fig.update_layout(title='Move the cursor to see the Dates', xaxis_title='Date', yaxis_title='Messages',
                          xaxis_tickangle=-90)
        st.title("Daily Timeline")
        st.plotly_chart(fig)

        # Adding borders around daily timeline section
        st.markdown('<hr style="border: 1px solid #008080;">', unsafe_allow_html=True)

        # Activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)
        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig = go.Figure()
            fig.add_trace(go.Bar(x=busy_day.index, y=busy_day.values, name='Activity'))
            fig.update_layout(title='Weekly Activity Map', xaxis_title='Day of the Week',
                              yaxis_title='Number of Messages')
            st.plotly_chart(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig = go.Figure()
            fig.add_trace(go.Bar(x=busy_month.index, y=busy_month.values, name='Activity'))
            fig.update_layout(title='Monthly Activity Map', xaxis_title='Month',
                              yaxis_title='Number of Messages')
            st.plotly_chart(fig)

        # Adding borders around activity map section
        st.markdown('<hr style="border: 1px solid #008080;">', unsafe_allow_html=True)

        # Weekly activity heatmap
        st.title("Weekly Activity Heatmap")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(user_heatmap, ax=ax, cmap="viridis", cbar_kws={'label': 'Number of Messages'})
        ax.set_title('Weekly Activity Heatmap', fontsize=16)
        ax.set_xlabel('Time Period', fontsize=12)
        ax.set_ylabel('Day of the Week', fontsize=12)
        plt.xticks(rotation=90, ha='right')
        plt.yticks(rotation=0)
        st.pyplot(fig)

        # Adding borders around heatmap section
        st.markdown('<hr style="border: 1px solid #008080;">', unsafe_allow_html=True)

        # Most busy users
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_users(df)
            fig = go.Figure(data=[go.Bar(x=x.index, y=x.values)])
            fig.update_layout(title='Most Busy Users', xaxis_title='Users', yaxis_title='Activity Count',
                              xaxis={'categoryorder': 'total descending'}, xaxis_tickangle=-90)
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(fig)
            with col2:
                st.dataframe(new_df)

        # Adding borders around most busy users section
        st.markdown('<hr style="border: 1px solid #008080;">', unsafe_allow_html=True)

        # Word cloud
        st.title("WORD CLOUD")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # Adding borders around word cloud section
        st.markdown('<hr style="border: 1px solid #008080;">', unsafe_allow_html=True)

        # Most common words
        most_common_df = helper.most_common_words(selected_user, df)
        fig = go.Figure(go.Bar(x=most_common_df[0], y=most_common_df[1]))
        fig.update_layout(xaxis=dict(tickangle=-90), yaxis_title="Frequency", xaxis_title="Words")
        st.title("Most Common Words")
        st.plotly_chart(fig)

        # Adding borders around most common words section
        st.markdown('<hr style="border: 1px solid #008080;">', unsafe_allow_html=True)

        # Emoji analysis
        st.title("Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user, df)
        st.dataframe(emoji_df, height=800, width=1000)
