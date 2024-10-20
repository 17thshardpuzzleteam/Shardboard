# Overview

Shardboard is a web-based dashboard for viewing and managing a team's status in a large puzzlehunt (such as MIT Mystery Hunt).
It is meant to be used in conjunction with [M-Bot](https://github.com/17thshardpuzzleteam/Mbot), a Discord bot that handles most of the heaver-duty puzzle/channel/sheet management.
The main purpose of Shardboard is to provide a condensed view of the current hunt state: allowing users to view puzzles categorized by round/meta, easily filter to see puzzle types they are interested in, and provide a centralized hub for important collaboration links.

# Setup

1. Make sure you have python and pip installed (Python 3.10+ or so). If you want, create a `virtualenv` for project dependencies.
2. Install dependencies with `pip install -r requirements.txt`.
3. Create a database with `python manage.py migrate`. (At this point, you can also configure M-Bot to point at that database).
4. Start the server with `python manage.py runserver`.
5. To view a hunt, create one with M-Bot using the `!createhunt -bighunt` command and add a round+puzzle. You should then be able to log into Shardboard using the credentials you provide M-Bot when creating the hunt.