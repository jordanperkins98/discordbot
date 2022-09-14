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

    if msg.content.startswith('-dbreset'):
        db["winCount"] = 0
        db["target"] = 0
        await msg.channel.send('Database reset')

    if msg.content.startswith('-target'):
        db["target"] = msg.content[7:len(msg.content)]
        await msg.channel.send(f'Target set to {db["target"]}')

    if msg.content.startswith('-streak'):
        streak = db["winCount"]
        target = db["target"]
        await msg.channel.send(f'Current streak is :{streak}/{target}')

    if msg.content.startswith('-WildWest'):
        streak = db["winCount"]
        streak += 1
        if streak > int(db["highScore"]):
            db["highScore"] = streak
        db["winCount"] = streak
        target = db["target"]
        if streak == target:
            await msg.channel.send(
                f'{streak}/{target} We going straight to the Wild Wild West')
        elif streak > int(target):
            streak -= 1
            await msg.channel.send(
                f'Please increase the target with -target followed by target')
        else:
            await msg.channel.send(f'Current streak is: {streak}/{target}')

    if msg.content.startswith('-WeSuck'):
        db["winCount"] = 0
        r = requests.get(
            "https://evilinsult.com/generate_insult.php?lang=en&type=json")
        insult = r.json()
        await msg.channel.send(insult["insult"], tts=True)

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

    if msg.content.startswith('-sethighscore'):
        db["highScore"] = msg.content[13:len(msg.content)]
        await msg.channel.send(f'High Score set to {db["highScore"]}')

    if msg.content.startswith('-highscore'):
        await msg.channel.send(f'Best score is: {db["highScore"]}')

    if msg.content.startswith('-crackflop'):
        randomFlip = random.randint(1, 2)
        if randomFlip == 1:
            randomFlip = "Heads"
        else:
            randomFlip = "Tails"

        await msg.channel.send('And the winner is: ' + randomFlip)


keep_alive()
client.run(my_secret)