import argparse
import re

import os
import sys

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

# ask user for exclusions
while True:
    user_choice = input("\nEnter server name to exclude from playlist (-1 when finished): ")

    if int(user_choice) == -1:
        break

    if int(user_choice) > -1:
        chatroom_paths.pop(int(user_choice))

    # relist out selections for exclusions
    for count, f in enumerate(chatroom_paths):
        print(count, f)

fullpath_chatroom_list = []

for chatlog_file in chatroom_paths:
    new_path = os.path.join(input_path, chatlog_file)
    fullpath_chatroom_list.append(new_path)

for f in fullpath_chatroom_list:
    print(f)

pattern = re.compile("http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?")

matches = []

for file in fullpath_chatroom_list:
    with open(file, 'r') as reader:
        datafile = reader.read()
        matches.append(re.findall(pattern, datafile))
        #print (matches)

print(matches)
# youtube_ids = [match[0] for match in matches]
