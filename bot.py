import hikari
import lightbulb
from dotenv import load_dotenv
import os
import pickle

load_dotenv()

bot = lightbulb.BotApp(
    os.environ["TOKEN"],
    default_enabled_guilds=(int(os.environ["DEFAULT_GUILD"]),),
)

birthdays = pickle.load(open("birthdays.pickle", "rb"))

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
    guild = ctx.guild_id
    mention = ctx.author.mention
    user = int(mention[2:-1])
    year = ctx.options.year
    month = ctx.options.month
    day = ctx.options.day

    if year < 1900:
        await ctx.respond(f"{mention} only years before 1900! are allowed")
        return
    if month < 1 or month > 12:
        await ctx.respond(f"{mention} only months between 1 and 12 are allowed")
        return
    if day < 1 or day > 31:
        await ctx.respond(f"{mention} only days between 1 and 31 are allowed")
        return

    for i in birthdays:
        if i["User"] == user:
            if i["Guild"] == guild:
                await ctx.respond(f"{mention} you already have a birthday set! use /birthday change to change it!")
                return

    birthday = {"Guild": guild, "User": user, "Year": year, "Month": month, "Day": day}
    birthdays.append(birthday)

    pickle.dump(birthdays, open("birthdays.pickle", "wb"))

    await ctx.respond(f"{mention} your Birthday ({year}/{month}/{day}) has been added!")

@birthday.child
@lightbulb.option("day", "The day you were born", int)
@lightbulb.option("month", "The month you were born", int)
@lightbulb.option("year", "The year you were born", int)
@lightbulb.command("change", "change your birthday")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def change(ctx: lightbulb.context) -> None:
    guild = ctx.guild_id
    mention = ctx.author.mention
    user = int(mention[2:-1])
    year = ctx.options.year
    month = ctx.options.month
    day = ctx.options.day

    if year < 1900:
        await ctx.respond(f"{mention} only years before 1900! are allowed")
        return
    if month < 1 or month > 12:
        await ctx.respond(f"{mention} only months between 1 and 12 are allowed")
        return
    if day < 1 or day > 31:
        await ctx.respond(f"{mention} only days between 1 and 31 are allowed")
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


bot.run()
