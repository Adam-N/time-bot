import csv
import datetime
import os

import discord
import pytz
from dateutil import tz
from discord.ext import commands
from discord import HTTPException

description = '''A bot that both provides current time, and future time conversions. 
                It also has a feature that you can use to create and post a 'Triumphant' list.'''
bot = commands.Bot(command_prefix='?', description=description)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
@commands.has_role('Staff')
async def remove():
    '''This command is usable by Staff only. Cleans up the Nominations file.'''
    try:
        os.remove('nominations.csv')
        await bot.say('File has been deleted. New file will be created next nomination.')
    except FileNotFoundError:
        await bot.say('File was not found.')


@bot.command(pass_context=True)
async def nominate(ctx, user: discord.User, *reason: str):
    '''Usable to nominate a User for Triumphant. Format: @user , `Reason`'''
    user_id = user.id
    # Joins the reasons so they become a single string.
    not_split_reason = " ".join(reason)
    not_split_reason = not_split_reason.strip(',')
    not_split_reason = not_split_reason.strip('"')

    # Creates a dictionay for the user to be stored to be put into the CSV File.
    name_list = {'name': user_id, 'reason': not_split_reason}
    with open('nominations.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in name_list.items():
            writer.writerow([key, value])

    await bot.say('Nominated {} for {}'.format(user, not_split_reason))


@commands.has_role('Staff')
@bot.command(pass_context=True)
async def post():

    # Sets up necessary variables.
    names = []
    reasons = []
    usernames = []
    server = bot.get_server('INSERT SERVER ID')
    triumphant_role = discord.utils.get(server.roles, name='INSERT ROLE NAME')

    # Removes Triumphant Role from previous users.
    for member in server.members:
        for role in member.roles:
            if role.name == "INSERT ROLE NAME":
                await bot.remove_roles(member, triumphant_role)

    # Writes the CSV file.
    with open('nominations.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        name_counter = 1
        list_counter = 0
        for row in csv_reader:

            # Iterates through the CSV file to get names of the users and reasons for nominations.
            # Also adds the Triumphant role to the user.

            if name_counter == 1:
                user_id = str(row[1])
                username = server.get_member(user_id=user_id)
                try:
                    await bot.add_roles(username, triumphant_role)
                except HTTPException:
                    await bot.say('Adding triumphant role failed. Perhaps you have insufficient roles.')
                usernames.append(username)
                display_username = username.display_name
                names.append(str(display_username))
                name_counter += 1
                list_counter += 1
            elif name_counter == 2:
                reasons.append(row[1])
                name_counter = 1

    # Uses embed to post the names and reasons.
    embed = discord.Embed(title="Triumphant!", description='Congratulations to the triumphant this week!',
                          color=0x00ff00)
    embed.add_field(name="Names:", value='\n'.join(names), inline=True)
    embed.add_field(name="Reasons:", value='\n'.join(reasons), inline=True)
    await bot.say(embed=embed)
    await bot.say('Congrats to the {}!'.format(discord.utils.get(server.roles, name='INSERT ROLE NAME').mention))


@bot.command(pass_context=True)
async def time():
    """Shows the time in a range of timezones."""

    timezones = {
        'PST/California': 'America/Los_Angeles',
        'EST/New York': 'America/New_York',
        'CET/Copenhagen': 'Europe/Copenhagen',
        'MSK/Moscow': 'Europe/Moscow',
        'AEST/Sydney': 'Australia/Sydney',
    }

    tz_field = []
    time_field = []
    for display, zone in timezones.items():
        tz_field.append("**{}**".format(display))
        time_field.append(datetime.datetime.now(pytz.timezone(zone)).strftime('%H:%M'))

    embed = discord.Embed(title="Time Conversions", description='Current Times', color=0x00ff00)
    embed.add_field(name="Time Zones", value='\n'.join(tz_field), inline=True)
    embed.add_field(name="Time", value='\n'.join(time_field), inline=True)
    await bot.say(embed=embed)


@bot.command()
async def convert(*time_input: str):
    """Shows a range of timezones in the future. Format: h:m day/month/year. Example 12:30 4/8/2018"""
    time_join = " ".join(time_input)
    time_to_convert = datetime.datetime.strptime(str(time_join), '%I:%M %d/%m/%y')
    timezones = {
        'PST/California': 'America/Los_Angeles',
        'EST/New York': 'America/New_York',
        'CET/Copenhagen': 'Europe/Copenhagen',
        'MSK/Moscow': 'Europe/Moscow',
        'AEST/Sydney': 'Australia/Sydney',
    }
    from_zone = tz.gettz('America/Edmonton')
    tz_field = []
    time_field = []
    for display, zone in timezones.items():
        tz_field.append("**{}**".format(display))
        mt = time_to_convert.replace(tzinfo=from_zone)
        to_zone = tz.gettz(zone)
        converted = mt.astimezone(to_zone)
        time_field.append(converted.strftime('%I:%M %d/%m/%y'))

    embed = discord.Embed(title="Time Conversions", description='In the Future', color=0x00ff00)
    embed.add_field(name="Time Zones", value='\n'.join(tz_field), inline=True)
    embed.add_field(name="Time", value='\n'.join(time_field), inline=True)
    await bot.say(embed=embed)


bot.run('INSERT BOT TOKEN HERE')
