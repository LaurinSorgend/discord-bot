import hikari
import lightbulb
from dotenv import load_dotenv
import os

load_dotenv()

bot = lightbulb.BotApp(
    os.environ["TOKEN"],
    default_enabled_guilds=(204301234742493184)
)

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

bot.run()
