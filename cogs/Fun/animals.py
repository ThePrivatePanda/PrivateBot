from nextcord.ext import commands
from nextcord import Embed, Colour
import random

class animals(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def randomapi_animal(animal):
        response = await self.bot.session.get(f"https://some-random-api.ml/animal/{animal}")
        response_js = await response.json()
        return response_js["image"], response_js["fact"]

    @commands.command(name="animal", aliases=["dog", "cat", "fox", "koala", "panda", "racoon", "kangaroo", "bird", "red_panda"])
    async def get_animal_randomapi(self, ctx):
        something = await self.randomapi_animal(ctx.message.replace("!!", "").split(" ")[0])
        return await ctx.send(embed=Embed(description=something[0], color=Colour(random.randint(0, 255)), image=something[1]))

    @commands.command(name="bunny")
    async def bunny(self, ctx):
        response = await self.bot.session.get('https://api.bunnies.io/v2/loop/random/?media=gif')
        js = await response.json()
        url = js['media']['gif']
        return await ctx.send(embed=Embed(title="Bunny!").set_image(url=url))

    @commands.command(name="duck")
    async def duck(self, ctx):
        response = await self.bot.session.get('https://random-d.uk/api/v1/random?type=png')
        js = await response.json()
        url = js['url']
        return await ctx.send(embed=Embed(title="Bunny!").set_image(url=url))

    @commands.command(name="lizard")
    async def lizard(self, ctx):
        response = await self.bot.session.get('https://nekos.life/api/v2/img/lizard')
        js = await response.json()
        url = js['url']
        return await ctx.send(embed=Embed(title="lizard says liza!").set_image(url=url))

    @commands.command(name="shiba")
    async def shiba(self, ctx):
        response = await self.bot.session.get('http://shibe.online/api/shibes')
        js = await response.json()
        url = js[0]
        return await ctx.send(embed=Embed(title="A Shiba!").set_image(url=url))

    
def setup(bot):
    bot.add_cog(animals(bot))