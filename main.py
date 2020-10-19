import discord

import commands


def token() -> str:
    with open("token.secret") as tokenFile:
        return tokenFile.read()


class zauberer(discord.Client):
    async def on_ready(self):
        print("ich habe wieder mana")

    async def on_message(self, message):
        # don't respond to ourselves
        if (message.author == self.user or
                not message.content.lower().startswith(commands.PREFIX)):
            return
        await commands.parseCommand(message)


if __name__ == "__main__":
    client = zauberer()
    client.run(token())

# https://discord.com/oauth2/authorize?client_id=1767649698889859084&scope=bot&permissions=8
