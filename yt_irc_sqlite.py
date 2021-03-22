import argparse
import re

import sqlite3
import time
import datetime
import json

import os
import sys

'''
produce markdown files that contain:

- youtube embed link
- <server> <#chat> <date> <user> <link> (jekyll categories)

Regex to pull server, chat, date, user, etc

change to run om servers individually instead of having user do stuff for website

ninite?
'''


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

# Create the parser
my_parser = argparse.ArgumentParser(prog='yt_irc',
                                    usage='%(prog)s [option] PATH',
                                    description='description: parse IRC logs for youtube links then form into playlist(s)')

# 0.2 d/t use of sqlite instead of parsing plaintext logs
my_parser.version = '0.2'

# Add the arguments
my_parser.add_argument('Path',
                       metavar='PATH',
                       type=str,
                       help='provide path to sqlite3 file: /home/user/.thelounge/logs/user.sqlite3')

my_parser.add_argument('-v',
                       '--version',
                       action='version',
                       help='show version')

# Execute the parse_args() method
args = my_parser.parse_args()

input_path = args.Path

if not os.path.isfile(input_path):
    print('The path specified does not exist')
    sys.exit()


con  = sqlite3.connect(input_path)
pattern = re.compile("http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?")

youtube_dict = []

servername_options = {
    "fcad4ce3-f2a6-41ce-9ac9-0cfcd9a47552" : "chat.freenode.net",
    "c5df9b7b-3ad4-4091-aac1-7cc20933931e" : "irc.darkscience.net",
    "5d86b716-20da-4ca5-9abc-cdf15c8a6916" : "travincal.snoonet.org"
}

start = datetime.datetime.now()
for row in con.execute("SELECT network, channel, time, msg FROM messages WHERE msg LIKE '%youtu%'"):
    
    msg = json.loads(row[3])
    match = re.findall(pattern, msg['text'])

    if not match: continue
    
    server_name = servername_options[row[0]]
    channel = row[1]
    server_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(row[2]/1000))
    nickname = msg['from']['nick']
    

    youtube_link_info = {
        'server' : server_name,
        'chatroom' : channel,
        'date' : server_time,
        'nick' : nickname,
        'youtube_id' : match[0][0]
    }
    youtube_dict.append(youtube_link_info)


print(len(youtube_dict))

end = datetime.datetime.now()

# print query benchmark
print(end - start)


'''
# get absolute file paths to each chatroom log file
chatroom_paths = []
chatroom_count = 0
for server_log_dir in os.listdir(input_path):

    serverlog_path = os.path.join(input_path,server_log_dir)
    if os.path.isdir(serverlog_path):

        # dump individual files into list
        for chatlog_file in os.listdir(serverlog_path):
            chatroom_path = os.path.join(serverlog_path, chatlog_file)
            chatroom_paths.append(chatroom_path)

            print(chatroom_count, chatroom_path)
            chatroom_count += 1


#########################
# ask user for exclusions
#########################
while True:
    user_choice = input("\nEnter index to exclude from playlist (-1 when finished): ")

    if int(user_choice) == -1:
        break

    if int(user_choice) > -1:
        chatroom_paths.pop(int(user_choice))

    # relist out selections for exclusions
    for count, f in enumerate(chatroom_paths):
        print(count, f)


#############
# search logs
#############
pattern = re.compile("http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?")
youtube_ids = []

for chatroom_path in chatroom_paths:

    # find all youtube urls
    with open(chatroom_path, 'r') as fp:
        chatroom_log_text = fp.read()
        matches = re.findall(pattern, chatroom_log_text) # returns a tuple 

        # only keep first element of tuple containing youtube_id, discard the rest
        for match in matches:
            youtube_id = match[0]
            if youtube_id:
                youtube_ids.append(youtube_id)


#############################################################
# change list of IDs into usable links and output to terminal
#############################################################
list_of_lists = [[]] * int((len(youtube_ids) / 50))

# break large list into multiple smaller lists containing 50 youtube ids
list_of_lists = chunks(youtube_ids, 50)

for fifty_youtube_ids in list_of_lists:
    comma_seperated_youtube_ids = ','.join(fifty_youtube_ids)
    playlist_url = "https://www.youtube.com/watch_videos?video_ids=" + comma_seperated_youtube_ids
    print(playlist_url, '\n')

'''
