import datetime
import discord
import os
import json


def seconds_until(hours, minutes):
    given_time = datetime.time(hours, minutes)
    now = datetime.datetime.now()
    future_exec = datetime.datetime.combine(now, given_time)
    if (future_exec - now).days < 0:  # If we are past the execution, it will take place tomorrow
        future_exec = datetime.datetime.combine(now + datetime.timedelta(days=1), given_time) # days always >= 0

    return (future_exec - now).total_seconds()


def get_args(msg):
    if isinstance(msg, discord.Message):
        return msg.content.split(' ')
    else:
        raise ValueError("The argument is not discord.Message")


def is_from_guild(ctx):
    if isinstance(ctx.author, discord.Member):
        return True
    else:
        return False


def get_source(name=None):
    source_path = os.getcwd() + "/../sources/source_real.json"

    # load source
    with open(source_path, 'r', encoding="utf-8") as file:
        sources = json.load(file)

    if name is None:
        return sources
    else:
        return sources[name]