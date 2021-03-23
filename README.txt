Audrey Leong al3854, Grace He gh2549
Postgresql account: al3854@columbia.edu (al3854)

web application URL: 

Implementation Details
    What has been implemented:
        - dashboard with links to other pages as well as the song that is currently playing
        - search bar by song name
        - profile page
        - list of followers and following (with unfollow buttons) 
        - list of liked songs, their artists, and their albums (with unlike buttons)
        - a playlist page with the playlists you have created, as well as those you follow
          (made interactive by letting you click on the playlist to see more details on which songs
          are in there and who the playlist is made by)
        - aforementioned individual playlist pages along with liked songs page have hrefs to 
          individual artist and album pages (redundancy to mimic the spotify UI that lets you access
          the information from various pages)
        - individual artist pages, album pages, and playlist pages
        - a queue page where you can view what is currently playing and what songs will be played 
          next

    What hasn't been implemented:
        - picture attribute for members
        - triggers and assertions, as previously noted in part2
        - setting page
        - following, and liking interactions

2 Web Pages with the the most interesting database operations in terms of what the pages are used for, 
how the page is related to the database operations (e.g., inputs on the page are used in such and such 
way to produce database operations that do such and such), and why you think they are interesting.

The page that lists all the liked-songs (/liked-songs) has the ability to unlike a song. This
interaction is achievable through clicking the "unlike" button next to a song in the "liked-songs"
page. The name of the song was passed through flask and inputted through a SQL query to find the 
song_ID. The song_id was then used to remove the entry in the table l_likes_s. This page would 
automatically redirect/refresh the page, showing that the song was unliked and removed from the list 
of liked songs. I thought that this operation would be difficult, but was able to successfully 
implement its functionality, while making the transition of unliking a song flawless. 

The dashboard has the most interesting database operations. 

