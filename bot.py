import lightbulb
from dotenv import load_dotenv
import os
import pickle
import datetime
from utils import get_formatted_date, check_if_valid_date, next_bd_unix
load_dotenv()

bot = lightbulb.BotApp(
    os.environ["TOKEN"],
    default_enabled_guilds=(int(os.environ["DEFAULT_GUILD"]),),
)

birthdays = pickle.load(open("birthdays.pickle", "rb"))
remind_time = pickle.load(open("remind.pickle", "rb"))

@bot.command
@lightbulb.command("birthday", "command group to store everyones birthdays")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def birthday(ctx: lightbulb.context) -> None:
    pass


@birthday.child
@lightbulb.option("year", "The year you were born", int)
@lightbulb.option("month", "The month you were born", int)
@lightbulb.option("day", "The day you were born", int)
@lightbulb.command("add", "add your birthday to the list")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def add(ctx: lightbulb.context) -> None:
    """adds a birthday to the list

    Args:
        ctx (lightbulb.context): context of the command
    """
    guild = ctx.guild_id
    mention = ctx.author.mention
    user = int(mention[2:-1])
    year = ctx.options.year
    month = ctx.options.month
    day = ctx.options.day

    if not check_if_valid_date(year, month, day):
        await ctx.respond(f"{mention} the date you entered is not valid!")
        return

    for i in birthdays:
        if i["User"] == user:
            if i["Guild"] == guild:
                await ctx.respond(f"{mention} you already have a birthday set! use /birthday change to change it!")
                return

    birthday = {"Guild": guild, "User": user,
                "Year": year, "Month": month, "Day": day}
    birthdays.append(birthday)

    pickle.dump(birthdays, open("birthdays.pickle", "wb"))

    await ctx.respond(f"{mention} your Birthday ({year}/{month}/{day}) has been added!")


@birthday.child
@lightbulb.option("year", "The year you were born", int)
@lightbulb.option("month", "The month you were born", int)
@lightbulb.option("day", "The day you were born", int)
@lightbulb.command("change", "change your birthday")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def change(ctx: lightbulb.context) -> None:
    """changes the birthday of a user

    Args:
        ctx (lightbulb.context): context of the command
    """
    guild = ctx.guild_id
    mention = ctx.author.mention
    user = int(mention[2:-1])
    year = ctx.options.year
    month = ctx.options.month
    day = ctx.options.day

    if not check_if_valid_date(year, month, day):
        await ctx.respond(f"{mention} the date you entered is not valid!")
        return

    for i in birthdays:
        if i["User"] == user:
            if i["Guild"] == guild:
                i["Year"] = year
                i["Month"] = month
                i["Day"] = day

                pickle.dump(birthdays, open("birthdays.pickle", "wb"))

                await ctx.respond(f"{mention} your Birthday ({year}/{month}/{day}) has been changed!")
                return

    await ctx.respond(f"{mention} you don't have a birthday set! use /birthday add to add it!")


@birthday.child
@lightbulb.command("remove", "remove your birthday")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def remove(ctx: lightbulb.context) -> None:
    """removes a birthday from the list

    Args:
        ctx (lightbulb.context): context of the command
    """
    guild = ctx.guild_id
    mention = ctx.author.mention
    user = int(mention[2:-1])

    for i in birthdays:
        if i["User"] == user:
            if i["Guild"] == guild:
                birthdays.remove(i)

                pickle.dump(birthdays, open("birthdays.pickle", "wb"))

                await ctx.respond(f"{mention} your Birthday has been removed!")
                return

    await ctx.respond(f"{mention} you don't have a birthday set! use /birthday add to add it!")


@birthday.child
@lightbulb.command("list", "list all birthdays")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def list(ctx: lightbulb.context) -> None:
    """lists all birthdays

    Args:
        ctx (lightbulb.context): context of the command
    """
    guild = ctx.guild_id
    birthdays_list = []

    for i in birthdays:
        if i["Guild"] == guild:
            user = await bot.rest.fetch_user(i["User"])
            birthdays_list.append(
                f"**{user.username}** - {get_formatted_date(i['Year'], i['Month'], i['Day'])} <t:{next_bd_unix(i['Month'], i['Day'])}:R>")

    if not birthdays_list:
        await ctx.respond("There are no birthdays set!")
        return

    await ctx.respond("**Birthdays:**\n" + "\n".join(birthdays_list))


@birthday.child
@lightbulb.command("help", "Help for the birthday command group")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def help(ctx: lightbulb.context) -> None:
    """help for the birthday command group

    Args:
        ctx (lightbulb.context): context of the command
    """
    await ctx.respond("`/birthday add` - add your birthday.\n`/birthday change` - change your birthday.\n`/birthday remove` - remove your birthday.\n`/birthday list` - list all birthdays.\n`/birthday help` - get this message.")

@bot.command()
@lightbulb.command("settings", "command group for settings")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def settings(self, ctx: lightbulb.SlashCommandContext) -> None:
    pass
    
@settings.child()
@lightbulb.option("Days", f"The number of days before the birthday to send the message [Default = 7; Current = {remind_time}]", int)
@lightbulb.command("remind", "set the number of days before the birthday to send a reminder message")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def remind(self, ctx: lightbulb.context) -> None:
    """sets the number of days before the birthday to send a reminder message
    
    Args:
        ctx (lightbulb.context): context of the command
    """
    days = ctx.options.Days
    if days < 1:
        await ctx.respond(f"{ctx.author.mention} The number of days must be greater than 0!")
        return
    if days > 365:
        await ctx.respond(f"{ctx.author.mention} The number of days must be less than 365!")
        return
    remind_time = days
    pickle.dump(remind_time, open("remind.pickle", "wb"))
    await ctx.respond(f"{ctx.author.mention} The number of days before the birthday to send the reminder message has been set to {days}!")

bot.run()
