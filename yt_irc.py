import argparse

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
                       help='provide path to .thelounge/logs')

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

# show index with available dir
print("\nIndex\t Directory")
print("-----\t ---------")

for dir in dir_list:
    print(dir_list.index(dir),'\t', dir)

user_choice = input("\nSelect user by index: ")

print(input_path.insert(user_choice))
