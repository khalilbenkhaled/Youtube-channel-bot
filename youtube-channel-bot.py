from __future__ import unicode_literals
from selenium import webdriver
from time import sleep
import youtube_dl
from moviepy.editor import *
import glob
from os import remove
from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo


#Getting the clips

chrome_driver_path = r"C:\Users\khalil\Documents\dev\chromedriver.exe"
URL = "https://www.twitch.tv/directory/game/Overwatch/clips?range=7d"

driver = webdriver.Chrome(chrome_driver_path)
driver.get(URL)
sleep(5)


clips_urls = []
clips_names = []
time = 0
while time <= 600:
    clips = driver.find_elements_by_css_selector('.sc-AxjAm.kJwHLD a')
    views = driver.find_elements_by_css_selector('.sc-AxjAm.iVDSNS p')
    lengths = driver.find_elements_by_css_selector('.sc-AxjAm.eFyVLi p')
    for l in lengths:
        s = l.text
        t = int(s[2]) * 10 + int(s[3])
        time += t

    driver.execute_script("arguments[0].scrollIntoView(true);", clips[len(clips)-1])
    sleep(1)

print(time)
for clip in clips:
    clips_names.append(clip.get_attribute("href"))
    clips_urls.append(clip.text)

for j in range(len(lengths)):
    s = lengths[j].text
    number = int(s[2])*10+int(s[3])
    if number == 0:
        lengths[j] = 60
    else:
        lengths[j] = number



data = {}
for k in range(len(clips_names)):
    data[k] = {

            "name": clips_names[k],
            "url": clips_urls[k],
            "length": lengths[k]
    }

#downloading the clips:

for k in range(len(data)):
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([data[k]["name"]])

#this part writes the name of the streamer on the clip
for file in glob.glob("*mp4"):
    clip = VideoFileClip(file)

    text = TextClip(data[k]["name"], font="Pumpkin_Pancakes", fontsize=70, color="white", stroke_color="black", stroke_width=3, kerning=-1)
    text.set_position(pos=(0, 0))

    video = CompositeVideoClip([clip, text])
    video.duration = clip.duration
    video.write_videofile("Edited_"+file)
    remove(file)


#this part concatenates the clips to make THE video

final = []

for file in glob.glob("*mp4"):
    clip1 = VideoFileClip(file)
    final.append(clip1)


final_clip = concatenate_videoclips(final, method="compose")
final_clip.write_videofile("final_video.mp4")

#uploading the video


channel = Channel()
channel.login("client_secrets.json", "credentials.storage")

# setting up the video that is going to be uploaded
video = LocalVideo(file_path="final_video.mp4")

#setting the video settings

video.set_title(data[0]["url"]+" Overwatch funny twitch moments")
video.set_description("This is an automated youtube channel")
video.set_tags(["this", "tag"])
video.set_category("gaming")
video.set_default_language("en-US")

# setting status
video.set_embeddable(True)
video.set_license("creativeCommon")
video.set_privacy_status("public")
video.set_public_stats_viewable(True)

video = channel.upload_video(video)
print(video.id)
print(video)

driver.quit()




















