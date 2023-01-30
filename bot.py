import hikari
import lightbulb
from dotenv import load_dotenv
import os
import pickle
load_dotenv()

bot = lightbulb.BotApp(
    os.environ["TOKEN"],
    default_enabled_guilds=(204301234742493184)
)

birthdays = pickle.load(open("birthdays.pickle", "rb"))

@bot.command
@lightbulb.command("ping", "Says pong!")
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.context) -> None:
    await ctx.respond("Pong!")

@bot.command
@lightbulb.command("group", "This is a group command")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def group(ctx: lightbulb.context) -> None:
    pass

@group.child
@lightbulb.command("subcommand", "This is a subcommand")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def subcommand(ctx: lightbulb.context) -> None:
    await ctx.respond("This is a subcommand")

@bot.command
@lightbulb.option("message", "The message to echo", str)
@lightbulb.command("echo", "This Command echos your message")
@lightbulb.implements(lightbulb.SlashCommand)
async def echo(ctx: lightbulb.context) -> None:
    await ctx.respond(ctx.options.message)

@bot.command
@lightbulb.command("birthday", "command group to store everyones birthdays")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def birthday(ctx: lightbulb.context) -> None:
    pass

@birthday.child
@lightbulb.option("day", "The day you were born", int)
@lightbulb.option("month", "The month you were born", int)
@lightbulb.option("year", "The year you were born", int)
@lightbulb.command("add", "add your birthday to the list")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def add(ctx: lightbulb.context) -> None:
    birthday = {"Guild": ctx.guild_id, "User": int(ctx.author.mention[2:-1]), "Year": ctx.options.year, "Month": ctx.options.month, "Day": ctx.options.day}
    birthdays.append(birthday)
    pickle.dump(birthdays, open("birthdays.pickle", "wb"))
    await ctx.respond(f"{ctx.author.mention} your Birthday ({ctx.options.year}/{ctx.options.month}/{ctx.options.day}) has been added!")
bot.run()
