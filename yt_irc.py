import argparse
import glob

import os
import sys

'''
glob instead of grep

add IF to check if the file name matches the excludes
and the logic for opening the file and getting the links

probably better to give it the dir instead of req it to be a certain dir



'''

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

# store all available dir into list
dir_list = [f for f in os.listdir(input_path) if os.path.isdir( os.path.join(input_path,f))]


chatroom_list = []

for dir in dir_list:
    for f in os.listdir(os.path.join(input_path, dir)):
        chatroom_list.append(os.path.join(dir, f))

for f in chatroom_list:
    print(chatroom_list.index(f), f)

while True:
    user_choice = input("\nEnter server name to exclude from playlist (-1 when finished): ")
    if int(user_choice) == -1:
        break

    if int(user_choice) > -1: chatroom_list.pop(int(user_choice))

    for f in chatroom_list:
        print(chatroom_list.index(f), f)

fullpath_chatroom_list = []

for f in chatroom_list:
    new_path = os.path.join(input_path, f)
    fullpath_chatroom_list.append(new_path)

for f in fullpath_chatroom_list:
    print(f)

#print(input_path.insert(user_choice))
