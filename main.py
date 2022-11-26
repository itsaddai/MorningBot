import os
import json
import discord
import requests
from continuity import continuity

intent = discord.Intents.default()
intent.members = True
intent.message_content = True
client = discord.Client(intents=intent)


def weather(city):
  try:
    rooturl = "http://api.openweathermap.org/data/2.5/weather?"
    api_key = os.getenv("api_key")

    url = f"{rooturl}q={city}&apikey={api_key}&units=metric"
    r = requests.get(url)

    data = r.json()

    city = data['name']
    temp = data['main']['temp']
    temp2 = data['main']['feels_like']
    temp3 = data['main']['humidity']
    temp4 = data['weather'][0]['description']
    temp5 = data['sys']['country']

    embed = discord.Embed(title=f"{city}"
                          ' Weather',
                          description=f"{temp4.capitalize()}",
                          color=0x14aaeb)
    embed.add_field(name="Temperature: ", value=f"{temp:.0f}°C", inline=True)
    embed.add_field(name="Feels like: ", value=f"{temp2:.0f}°C", inline=True)
    embed.add_field(name="Humidity: ", value=f"{temp3}%", inline=True)
    embed.add_field(name="Country: ", value=f"{temp5}", inline=True)

    return embed

  except:
    embed = discord.Embed(title="Invalid location...", color=0x14aaeb)
    embed.add_field(
      name="Error...",
      value=
      "The weather information for this city is unavailable, please enter another city name.",
      inline=True)
    return embed


def quotes():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " \n- " + json_data[0]['a']
  return (quote)


@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(msg):
  if msg.author == client.user:
    return
  if msg.content.startswith("#morning"):
    quote = quotes()
    city = msg.content[9::].lower()
    data = weather(city)
    await msg.channel.send(quote)
    await msg.channel.send(embed=data)


continuity()

client.run(os.getenv('token'))
