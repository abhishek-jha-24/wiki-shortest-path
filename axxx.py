from twilio.rest import Client
import keys
client = Client(keys.account_sid, keys.account_token)
from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
filename = 'finalized_model.sav'
import pickle
from googleapiclient.discovery import build
import re
api_key = "AIzaSyACfVnsEXZLUvwxkp813X9PZZeX0RYI1pY"
from html import unescape


# AIzaSyACfVnsEXZLUvwxkp813X9PZZeX0RYI1pY
# AIzaSyAuZaVDtA21Cx7e43EhqA2WEsKgespagyA

def video_comments(url):
    formed=[]
    # empty list for storing reply

    # creating youtube resource object
    youtube = build('youtube', 'v3',
                    developerKey=api_key)

    # retrieve youtube video results
    video_response=youtube.commentThreads().list(
    part='snippet,replies',
    videoId=url
    ).execute()
    print("found")
    # iterate video response    
        # extracting required info
        # from each result object 
    while video_response:
      for item in video_response['items']:
        print("found")
      break
    
    formed.sort(reverse=True)
    return formed

try:
  formed = video_comments("th08")
  for i in range(0, min(len(formed), 100)):
    now.append(str(formed[i][1]))
except Exception as e:
  now = []
  message = client.messages.create(
  body="video was deleted",
  from_ = keys.twilio_number,
  to = keys.target_number

  )
  print(e)
