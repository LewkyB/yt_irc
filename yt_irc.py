import argparse
import re

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

my_parser.version = '0.1'

# Add the arguments
my_parser.add_argument('Path',
                       metavar='PATH',
                       type=str,
                       help='provide path to .thelounge/logs/user')

my_parser.add_argument('-v',
                       '--version',
                       action='version',
                       help='show version')

# Execute the parse_args() method
args = my_parser.parse_args()

input_path = args.Path

if not os.path.isdir(input_path):
    print('The path specified does not exist')
    sys.exit()

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
