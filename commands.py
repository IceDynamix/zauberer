import json
import random

import discord
import googletrans
import requests

PREFIX = "oh zauberer ich bitte um "
muschelHistory = []
muschelHistoryLength = 3


async def send(channel: discord.channel, s: str):
    print("> {}: {}".format(channel.name, s))
    await channel.send(s)


async def parseCommand(message: discord.message):
    print("{}: {}".format(message.author.name, message.content))
    m = message.content[len(PREFIX):].lower()
    for command in COMMANDS:
        if m.startswith(command):
            params = m[len(command):].strip()
            await COMMANDS[command]["function"](message, params)
            return

    await send(message.channel, "werter nutzer, ihre bitte scheint mir unbekannt")


async def magischeMiesmuschel(message: discord.message, params: str):
    answers = [
        "möglicherweise",
        "eventuell",
        "frag später ich bin beschäftigt",
        "einfach gentoo installieren",
        "zieh den rucksack aus wenn du mit mir redest",
        "frag nicht so blöd",
        "das würde mich überraschen",
        "ist das überhaupt möglich",
        "eines tages vielleicht",
        "halts maul",
        "das geht dich nichts an",
        "wen interessierts überhaupt",
        "sag nochmal ich hab dich nicht gehört",
        "die leitung ist schlecht warte kurz",
        "new phone who dis",
        "du hurensohn",
        "laber keinen scheiß",
        "was guckst du so blöd",
        "dafür solltest du gebannt werden"
    ]
    text = random.choice(
        [answer for answer in answers if answer not in muschelHistory]
    ) + " du hurensohn"
    muschelHistory[-muschelHistoryLength:].append(text)
    await send(message.channel, text)


async def quote(message: discord.message, params: str):
    with open("quotes.json", "r") as quotesFile:
        quotes = json.load(quotesFile)

    quote = random.choice(quotes)

    await send(
        message.channel,
        "> {}\n- {}, {}".format(quote["quote"], quote["author"], quote["date"])
    )


async def ping(message: discord.message, params: str):
    await send(message.channel, f"<@{message.author.id}>")


async def helpCommand(message: discord.message, params: str):
    helpText = []
    for i, command in enumerate(COMMANDS):
        line = "entweder" if i == 0 else "oder"
        line += f" `{command}` {COMMANDS[command]['help']}"
        helpText.append(line)
    await send(message.channel, '\n'.join(helpText))


async def goodTranslation(message: discord.message, params: str):
    translation = googletrans.Translator().translate(params, dest="de")
    await send(message.channel, translation.text.lower())


async def translation(message: discord.message, params: str):
    if params == "":
        await send(message.channel, "übersetz du doch mal eine leere nachricht du wichser")
        return
    word = params
    translator = googletrans.Translator()
    try:
        for i in range(8):
            language = random.choice(list(googletrans.LANGUAGES.keys()))
            word = translator.translate(word, dest=language).text
        await goodTranslation(message, word)
    except Exception as e:
        await send(message.channel, "mein mana ist aufgebraucht, probiers gleich nochmal du hurensohn")


async def uhrzeit(message: discord.message, params: str):
    await send(message.channel, "schau auf deine eigene uhr du hurensohn")


async def dog(message: discord.message, params: str):
    url = "https://api.thedogapi.com/v1/images/search"
    image = json.loads(requests.get(url).text)[0]["url"]
    await send(message.channel, image)


async def cat(message: discord.message, params: str):
    url = "https://api.thecatapi.com/v1/images/search"
    image = json.loads(requests.get(url).text)[0]["url"]
    await send(message.channel, image)


async def number(message: discord.message, params: str):
    await send(message.channel, "3")


COMMANDS = {
    "die uhrzeit": {
        "function": uhrzeit,
        "help": "für die faulen menschen"
    },
    "die miesmuschel": {
        "function": magischeMiesmuschel,
        "help": "für die weisheit der magischen miesmuschel"
    },
    "eine zahl": {
        "function": number,
        "help": "für eine zahl"
    },
    "ein zitat": {
        "function": quote,
        "help": "für die nostalgie eines zufälligen zitates"
    },
    "einen ping": {
        "function": ping,
        "help": "um gepingt zu werden"
    },
    "eine gute übersetzung für": {
        "function": goodTranslation,
        "help": "für eine gute übersetzung nach deutsch"
    },
    "eine übersetzung für": {
        "function": translation,
        "help": "für eine übersetzung durch 8 zufällige sprachen gejagt und dann auf deutsch übersetzt"
    },
    "ein hundebild": {
        "function": dog,
        "help": "für ein zufälliges hundebild"
    },
    "ein katzenbild": {
        "function": cat,
        "help": "für ein zufälliges katzenbild"
    },
    "hilfe": {
        "function": helpCommand,
        "help": "für diese nachricht, du hurensohn"
    }
}
