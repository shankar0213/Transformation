from navigation import make_sidebar
import streamlit as st
import pandas as pd
from pytube import Playlist
from streamlit_player import st_player
import os

make_sidebar()


 
def get_playlist_videos(playlist_url):
    playlist = Playlist(playlist_url)
    return playlist.video_urls
 
def main():
    z=''
    st.title("YouTube Playlist Player")
 
    playlist_url = st.text_input("Enter YouTube Playlist Link:")
    if playlist_url:
        playlist_videos = get_playlist_videos(playlist_url)
 
        if st.button("Play Playlist"):
            for i in range(len(playlist_url)):
                if playlist_url[i] == '=':
                    z=(playlist_url[i+1:len(playlist_url)])
                    break
            print('z=',z)        
         
            data = {'sno':[1],
           
                'playlist': ['PL89t04T3yNybk1OM9npy_sqgGamrv843F&si=jxbmR9KqxeqElgAG'],
                'name': ['name1']
            }
            data.update({"playlist": z})
 
# Create a DataFrame from the dictionary
            df = pd.DataFrame(data)
            df=df.sample(frac=1).reset_index()
           
            x=0
            html =  """
            <iframe id="ytplayer" type="text/html" width="685" height="333"
            src="https://www.youtube.com/embed/?listType=playlist&list={}"
             encrypted-media; gyroscope; picture-in-picture"
            frameborder="0" allowfullscreen allow="autoplay"
            >
            """
         
            while x<1:
                st.components.v1.html(html.format(df.at[x,'playlist']),  height=350,scrolling=False)
                x+=1
 
 
if __name__ == "__main__":
    main()
