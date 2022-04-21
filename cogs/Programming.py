# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import requests
import os
import sys
from datetime import datetime
import pytz
import dateutil.parser


class Programming(commands.Cog):
    """The description for Programming goes here."""

    contest_url = 'https://kontests.net'

    cwd = os.getcwd()
    sys.path.append(f'{cwd}..')
    from setup import available_contests

    def __init__(self, bot):
        self.bot = bot

    def time_convert(self, convert, fmt):
        """Converts time to a different format."""
        fmt = dateutil.parser.parse(convert)
        # convert zulu time to eastern standard time
        fmt = fmt.astimezone(pytz.timezone('US/Eastern'))
        # convert format to d-m-Y H:M:S
        fmt = fmt.strftime('%d-%m-%Y %H:%M:%S')

        return fmt.split()


    # contest information
    @commands.command(name='contest', aliases=['contestinfo'])
    async def contest(self, ctx, *, site=''):
        """
        Get information about the current contest.
        """
        if not site:
            # return all the possible endpoints
            await ctx.send('You did not specifcy a contest site.\nHere are the available sites:')
            embed = discord.Embed(title='Contest Information', description='\n'.join(
                self.available_contests), color=0x00ff00)
            return await ctx.send(embed=embed)

        site = site.replace(' ', '_')
        # print(site)
        if site not in self.available_contests:
            await ctx.send(f'Error: {site} is not a valid contest site.\nThe available sites are:')
            embed = discord.Embed(title='Contest Information', description='\n'.join(
                self.available_contests), color=0x00ff00)
            return await ctx.send(embed=embed)

        # replace spaces with _
        endpoint = f'/api/v1/{site}'
        r = requests.get(self.contest_url + endpoint)

        if r.status_code != (200 or 204):
            return await ctx.send(f'Error: {r.status_code}')

        data = r.json()
        contests = []
        for entry in data:
            # print(f"HERE HERE HERE: {'T' in entry['start_time']}")
            start_d, start_t = self.time_convert(entry['start_time'], self.available_contests[site][1])
            end_d, end_t = self.time_convert(entry['end_time'], self.available_contests[site][1])
            contests.append(
                f'{entry["name"]} - Date: {start_d} - Start: {start_t} - End: {end_t} - {entry["url"]}')

        # embed the contest data
        embed = discord.Embed(title=f'{" ".join([item.capitalize() for item in site.split("_")])}', description='\n'.join(contests), color=0x00ff00)
        image = self.available_contests[site][0]
        embed.set_thumbnail(url=image)
        await ctx.send(embed=embed)

    
    @commands.command(name='qr', aliases=['qrcode'])
    async def qr(self, ctx, *, qr_url):
        """
        Generate a QR code from a given URL.
        """
        url = 'http://api.qrserver.com/v1/read-qr-code/?fileurl='
        qr_url = 'https://media.discordapp.net/attachments/881610369318150228/966467287479631952/unknown.png'

        r = requests.get(url + qr_url)
        await ctx.send('Loading...')
        if r.status_code != (200 or 204):
            return await ctx.send(f'Error: {r.status_code}')

        data = r.json()
        return await ctx.send(data[0]['symbol'][0]['data'])


def setup(bot):
    bot.add_cog(Programming(bot))
