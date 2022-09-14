import discord, os, requests, time, random
from replit import db
from keep_alive import keep_alive

my_secret = os.environ['token']
client = discord.Client()


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(msg):
    if msg.author == client.user:
        return

    if msg.content.startswith('-hello'):
        await msg.channel.send(f"Hello {msg.author}")

    if msg.content.startswith('-joke'):
        r = requests.get("https://official-joke-api.appspot.com/random_joke")
        joke = r.json()
        await msg.channel.send(joke["setup"])
        time.sleep(3)
        await msg.channel.send(joke["punchline"])

    if msg.content.startswith('-superjoke'):
        for index in range(0, 5):
            r = requests.get(
                "https://official-joke-api.appspot.com/random_ten")
            joke = r.json()
            await msg.channel.send(joke[random.randint(0, 9)]["setup"])
            time.sleep(2)
            await msg.channel.send(joke[random.randint(0, 9)]["punchline"])
            await msg.channel.send(
                "--------------------------------------------")
            time.sleep(1.5)

    if msg.content.startswith('-meme'):
        r = requests.get("https://meme-api.herokuapp.com/gimme")
        meme = r.json()
        while meme["nsfw"] == "true":
            r = requests.get("https://meme-api.herokuapp.com/gimme")
            meme = r.json()

        await msg.channel.send(f'Title: {meme["title"]}')
        await msg.channel.send(meme["url"])

    if msg.content.startswith('-randomSurvivorj'):
        survivors = [
            "Dwight", "Meg", "Claudette", "Jake", "Hag", "Bill", "David",
            "Laurie", "Jane", "Leon S. Kennedy", "Jill Valentine"
        ]
        randomSurvivor = survivors[random.randint(0, len(survivors))]
        await msg.channel.send(randomSurvivor)

    if msg.content.startswith('-randomSurvivorg'):
        survivors = [
            "Dwight", "Meg", "Claudette", "Jake", "Hag", "Bill", "David",
            "Laurie", "Elodie", "Felix", "Zarina", "Steve!", "Nancy", "Kate",
            "Ace Visconti", "Leon S. Kennedy", "Jill Valentine"
        ]
        randomSurvivor = survivors[random.randint(0, len(survivors))]
        await msg.channel.send(randomSurvivor)

    if msg.content.startswith('-crackflop'):
        randomFlip = random.randint(1, 2)
        if randomFlip == 1:
            randomFlip = "Heads"
        else:
            randomFlip = "Tails"

        await msg.channel.send('And the winner is: ' + randomFlip)



client.run(my_secret)
