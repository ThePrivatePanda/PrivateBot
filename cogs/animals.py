import discord, datetime
from discord.ext import commands
from discord.errors import Forbidden, HTTPException, NotFound


class animals(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="dog", aliases=["kutta", "kutte"])
    async def dog(self, ctx):
        response = await self.bot.session.get('https://some-random-api.ml/animal/dog')
        js = await response.json()
        url = js['image']
        return await ctx.send(embed=discord.Embed(title="Woof!").set_image(url=url))

    @commands.command(name="cat", aliases=["billi"])
    async def cat(self, ctx):
        response = await self.bot.session.get('https://api.thecatapi.com/v1/images/search', headers={'x-api-key':'b50758de-4a39-4113-a109-329a542fc323'})
        js = await response.json()
        url = js[0]['url']
        return await ctx.send(embed=discord.Embed(title="Meow").set_image(url=url))

    @commands.command(name="bunny")
    async def bunny(self, ctx):
        response = await self.bot.session.get('https://api.bunnies.io/v2/loop/random/?media=gif')
        js = await response.json()
        url = js['media']['gif']
        return await ctx.send(embed=discord.Embed(title="Bunny!").set_image(url=url))

    @commands.command(name="duck")
    async def duck(self, ctx):
        response = await self.bot.session.get('https://random-d.uk/api/v1/random?type=png')
        js = await response.json()
        url = js['url']
        return await ctx.send(embed=discord.Embed(title="Bunny!").set_image(url=url))

    @commands.command(name="fox")
    async def fox(self, ctx):
        response = await self.bot.session.get('https://randomfox.ca/floof/')
        js = await response.json()
        url = js['image']
        return await ctx.send(embed=discord.Embed(title="A Shiba!").set_image(url=url))

    @commands.command(name="lizard")
    async def lizard(self, ctx):
        response = await self.bot.session.get('https://nekos.life/api/v2/img/lizard')
        js = await response.json()
        url = js['url']
        return await ctx.send(embed=discord.Embed(title="lizard says liza!").set_image(url=url))

    @commands.command(name="shiba")
    async def shiba(self, ctx):
        response = await self.bot.session.get('http://shibe.online/api/shibes')
        js = await response.json()
        url = js[0]
        return await ctx.send(embed=discord.Embed(title="A Shiba!").set_image(url=url))

    @commands.command(name="koala")
    async def koala(self, ctx):
        response = await self.bot.session.get('https://some-random-api.ml/img/koala')
        js = await response.json()
        url = js['link']
        return await ctx.send(embed=discord.Embed(title="a me!").set_image(url=url))

    @commands.command(name="panda")
    async def panda(self, ctx):
        response = await self.bot.session.get('https://some-random-api.ml/img/panda')
        js = await response.json()
        url = js['link']
        return await ctx.send(embed=discord.Embed(title="Lé panda!").set_image(url=url))

    @commands.command(name="racoon")
    async def racoon(self, ctx):
        response = await self.bot.session.get('https://some-random-api.ml/animal/raccoon')
        js = await response.json()
        url = js['image']
        return await ctx.send(embed=discord.Embed(title="racoon says roo!").set_image(url=url))

    @commands.command(name="kangaroo")
    async def kangaroo(self, ctx):
        response = await self.bot.session.get('https://some-random-api.ml/animal/kangaroo')
        js = await response.json()
        url = js['image']
        return await ctx.send(embed=discord.Embed(title="Kangaroo with a K").set_image(url=url))

    @commands.command(name="red_panda", aliases=['redpanda'])
    async def red_panda(self, ctx):
        response = await self.bot.session.get('https://some-random-api.ml/animal/red_panda')
        js = await response.json()
        url = js['image']
        return await ctx.send(embed=discord.Embed(title="A red panda pog").set_image(url=url))

    @commands.command(name="bird")
    async def bird(self, ctx):
        response = await self.bot.session.get('https://some-random-api.ml/animal/birb')
        js = await response.json()
        url = js['image']
        return await ctx.send(embed=discord.Embed(title="B for Bird").set_image(url=url))

    


def setup(bot):
    bot.add_cog(animals(bot))

"""
[
    {
        "_id":"5cf1d1adc46fd30ceb78ea71",
        "index":8,
        "name":"The Cremona Elephant",
        "affiliation":"Holy Roman Emperor Frederick II",
        "species":"Unavailable",
        "sex":"Unavailable",
        "fictional":"false",
        "dob":"12XX",
        "dod":"Unavailable",
        "wikilink":"https://en.wikipedia.org/wiki/Cremona_elephant",
        "image":"https://elephant-api.herokuapp.com/pictures/008.jpg",
        "note":"A gift presented to Holy Roman Emperor Frederick II by Sultan of Egypt Al-Kamil, in 1229. Frederick used the elephant in his triumph parades."
    }
]"""