import discord
import random
import json
from monzo.monzo import Monzo

with open("details.json") as data:
    tokens = json.load(data)
discordToken = tokens["tokens"][0]["DiscordToken"]
Mclient = Monzo(tokens["tokens"][0]["MonzoToken"])

account_id = Mclient.get_first_account()["id"]
Dclient = discord.Client()

@Dclient.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == Dclient.user:
        return

    if message.content.lower().startswith('balance'):
        balance = Mclient.get_balance(account_id)
        embed=discord.Embed(title="Ola's Bank Balance")
        embed.add_field(name="Total Balance", value="£{}".format(balance["total_balance"]/100), inline=True)
        embed.add_field(name="Available Balance", value="£{}".format(balance["balance"]/100), inline=True)
        embed.add_field(name="Spent Today", value="£{}".format(balance["spend_today"]/100), inline=True)
        embed.set_footer(text="Stop spending so much money")
        await Dclient.send_message(message.author, embed=embed)

    if message.content.lower().startswith("pots"):
        pots = Mclient.get_pots()
        embed=discord.Embed(title="Ola's Money Pots")
        embed.add_field(name=pots["pots"][0]["name"], value="£{}".format(pots["pots"][0]["balance"]/100), inline=False)
        embed.add_field(name=pots["pots"][3]["name"], value="£{}".format(pots["pots"][3]["balance"]/100), inline=False)
        await Dclient.send_message(message.author, embed=embed)


    if message.content.lower().startswith("Shutdown"):
        await Dclient.send_message(message.author, "Okay bye then.")
        Dclient.close()

@Dclient.event
async def on_ready():
    print('Logged in as')
    print(Dclient.user.name)
    print(Dclient.user.id)
    print('------')

Dclient.run(discordToken)
