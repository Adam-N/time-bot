import datetime

import pytz
import discord
from dateutil import tz
from discord.ext import commands

description = '''A bot that both provides current time, and future time conversions.'''
bot = commands.Bot(command_prefix='?', description=description)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command(pass_context=True)
async def time(ctx):
    """Shows the time in a range of timezones."""
    await bot.send_typing(ctx.message.channel)

    timezones_to_convert_dict = {
        'PT/California': 'America/Los_Angeles',
        'MT/Alberta': 'America/Edmonton',
        'CT/Winnipeg': 'America/Winnipeg',
        'ET/New York': 'America/New_York',
        'UK/London': 'Europe/London',
        'CET/Copenhagen': 'Europe/Copenhagen',
        'AEST/Sydney': 'Australia/Sydney',
    }

    tz_field = []
    time_field = []
    for display, zone in timezones_to_convert_dict.items():
        tz_field.append("**{}**".format(display))
        time_field.append(datetime.datetime.now(pytz.timezone(zone)).strftime('%H:%M'))

    embed = discord.Embed(title="Time Conversions", description='Current Times', color=0x00ff00)
    embed.add_field(name="Time Zones", value='\n'.join(tz_field), inline=True)
    embed.add_field(name="Time", value='\n'.join(time_field), inline=True)
    await bot.say(embed=embed)


@bot.command(pass_context=True)
async def convert(ctx, time_zone_input: str, *time_input: str):
    """Shows a range of timezones in the future. Format: h:m day/month/year. Example 12:30 4/8/2018"""
    await bot.send_typing(ctx.message.channel)
    try:
        time_join = " ".join(time_input)
        time_join.strip(' ')
        time_to_convert = datetime.datetime.strptime(str(time_join), '%H:%M %d/%m/%y')

        tz_dict = {
            'PT': 'America/Los_Angeles',
            'MT': 'America/Edmonton',
            'CT': 'America/Winnipeg',
            'ET': 'America/New_York',
            'SK': 'Canada/Saskatchewan',
            'UK': 'Europe/London',
            'CET': 'Europe/Paris',
            'AU': 'Australia/Sydney'
        }
        timezones_to_use = {
            'PT/California': 'America/Los_Angeles',
            'MT/Alberta': 'America/Edmonton',
            'SK/Saskatchewan': 'Canada/Saskatchewan',
            'CT/Winnipeg': 'America/Winnipeg',
            'ET/New York': 'America/New_York',
            'UK/London': 'Europe/London',
            'CET/Copenhagen': 'Europe/Copenhagen',
            'AEST/Sydney': 'Australia/Sydney',
        }

        from_zone = tz.gettz(tz_dict.get(time_zone_input))
        tz_field = []
        time_field = []
        for display, zone in timezones_to_use.items():
            tz_field.append("**{}**".format(display))
            mt = time_to_convert.replace(tzinfo=from_zone)
            to_zone = tz.gettz(zone)
            converted = mt.astimezone(to_zone)
            time_field.append(converted.strftime('%H:%M %d/%m/%y'))

        embed = discord.Embed(title="Time Conversions", description='In the Future', color=0x00ff00)
        embed.add_field(name="Time Zones", value='\n'.join(tz_field), inline=True)
        embed.add_field(name="Time", value='\n'.join(time_field), inline=True)
        await bot.say(embed=embed)
    except ValueError:
        await bot.say('Check formatting for your command. Must be in HH:MM d/m/y using the 24 hour clock.')


@bot.command()
async def timezones():
    tz_dict = {
        'PT': 'Pacific Time',
        'MT': 'Mountain Time',
        'SK': 'Saskatchewan Time',
        'CT': 'Central Time',
        'ET': 'Eastern Time',
        'UK': 'United Kingdom',
        'CET': 'Central European Time',
        'AU': 'Australian (Sydney)'
    }
    embed = discord.Embed(title='Time Zones', description='Usable Timezones', color=0x00ff00)
    embed.add_field(name='Time Zones', value='\n'.join(tz_dict), inline=True)
    embed.add_field(name='Names', value='\n'.join(tz_dict.values()))
    await bot.say(embed=embed)


bot.run('INSERT BOT TOKEN HERE')
