import sys
import google
import random


def fetch_image(query):
    print('Getting result...')
    result = google.search_images(query,num=5,stop=5)
    print('->Got result!')
    image_urls = list()
    for r in result:
        print("-->" + r)
        image_urls.append(r)
    return image_urls[random.randint(0,len(image_urls))]


def fetch_video(query):
    print('Getting result...')
    result = google.search_videos(query, num=8, stop=8)
    print('->Got result!')
    video_urls = list()
    for r in result:
        #print("-->" + r)
        if 'watch?v=' in r:
            video_urls.append(r)
    if len(video_urls) > 1:
        return video_urls[random.randint(0, len(video_urls)-1)]
    elif len(video_urls) == 1:
        return video_urls[0]
    else:
        return "Could not find a video. Try typing a different query."


def fetch_news(query):
    print('Getting result...')
    result = google.search_news(query, num=4, stop=4)
    print('->Got result!')
    video_urls = list()
    for r in result:
        #print("-->" + r)
        #if 'watch?v=' in r:
        video_urls.append(r)
    if len(video_urls) > 1:
        return video_urls[random.randint(0, len(video_urls)-1)]
    elif len(video_urls) == 1:
        return video_urls[0]
    else:
        return "Could not find a news article. Try typing a different query."
