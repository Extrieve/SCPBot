# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import requests
import os
import sys
import datetime


class Programming(commands.Cog):
    """The description for Programming goes here."""

    contest_url = 'https://kontests.net'

    cwd = os.getcwd()
    sys.path.append(f'{cwd}..')
    from config import available_contests

    def __init__(self, bot):
        self.bot = bot

    # contest information
    @commands.command(name='contest', aliases=['contestinfo'])
    def ztoest(value):
        d, t = value.split('T')
        l = []
        l2 = []
        l = t.split(':')
        l2 = d.split('-')
        i2 = int(l2[2])
        i = int(l[0])
        i -= 4
        if i < 0:
            i += 24
            i2 -= 1
            l[0] = str(i)
            l2[2] = str(i2)
        else:
            l[0] = str(i)

        date = f'{l2[1]}-{l2[2]}-{l2[0]}'
        time = f'{l[0]}:{l[1]} EST'
        return date, time

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
            start_time = entry['start_time']
            end_time = entry['end_time']

            # TODO: Change time format

            contests.append(
                f'{entry["name"]} - {start_time} - {end_time} - {entry["url"]}')

        # embed the contest data
        embed = discord.Embed(title=f'{" ".join([item.capitalize() for item in site.split("_")])}', description='\n'.join(
            contests), color=0x00ff00)
        image = self.available_contests[site]
        embed.set_thumbnail(url=image)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Programming(bot))
