import os
import random
import discord
import re
import pygsheets

# this is a application to create a discord bot to allow for the general function of delta nu delta's dungeons and dragons system
    # each player can have one multiple charecters and each person needs to be able to get the infromation about each item in
    # the system.
# the primary function of this application is to keep track of players data and allow for players to access data about the system.


# gets the client secret file and authroizes bot to use google api and sheets
gc = pygsheets.authorize()
# api key for google sheets
token = "NjIzNjI2NjUzODUwOTI3MTE0.Xicrfw.IHjN7itL7Fr9L6vchFVlJDKUgQ0"
client = discord.Client()
# this to get this sheet https://docs.google.com/spreadsheets/d/1oCgn7laejTuV0lqdxDqvi3qNhuW6JtSfwv26pmLrS94/edit?usp=sharing
sh = gc.open("Delta Nu Delta - Character Census Spreadsheet beta")
# select the first sheet
Census = sh[0]

# select all of the magic item sheets
Uncommon = gc.open("Magic Items Uncommon.xlsx")
Rare = gc.open("Magic Items Rare")
VRare = gc.open("Magic Items Very Rare ")
Uncommon = Uncommon[0]
Rare = Rare[0]
VRare = VRare[0]
Items = []
uncommon = []
rare = []
vrare = []


# reads from drive sheets and turns each sheet into an array
def readFromDrive(a, b):
    for array in a:
        if array[1] == "":
            break

        b.append(array)
        #        if array[2] == "":
        #           break
        #      print(message.content[6:])
        #     print(array[1])
        #    if array[1] == message.content[7:]:


# loads all sheets
readFromDrive(Uncommon.get_all_values(), uncommon)
readFromDrive(Rare.get_all_values(), rare)
readFromDrive(VRare.get_all_values(), vrare)
readFromDrive(uncommon, Items)
readFromDrive(rare, Items)
readFromDrive(vrare, Items)
print(Items)


# update the first sheet with df, starting at cell B2.
def comparestrings(string1, string2):
    if len(string1[1:]) == 0 or len(string2[1:]) == 0:
        return 0
    if string1[0] == string2[0]:
        return 1 + comparestrings(string1[1:], string2[1:])
    else:
        return comparestrings(string1[1:], string2[1:])

# a function to randomly pick 3 items from a given array
def randomPick(type):
    done = True
    holder = []
    print(type)
    while done:
        randpick = random.choice(type)

        holder.append(randpick)
        # if len(holder) =
        done = False
    print(randpick)
    return holder


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


# 244275535188983808
@client.event
async def on_message(message):
    channel = message.channel

    #an optional "feature" to make a joke to a friend if Wiley Knight attempts to send a message the bot will reply by
    #calling them a vampire
    # if str(message.author.nick) == "Wiley Knight":
    #    channel = message.channel
    #    await channel.send("stop trying to break the bot you vampire")

    # A command to pick three items from each sheet and output the selected.
    if message.content.startswith('!RollItems') or message.content.startswith('!rollitems'):
        randomPick(uncommon)
        await channel.send(randomPick(rare))
        await channel.send(randomPick(vrare))

    # a comand to look up a magic item and get the price
    if message.content.startswith('!Price') or message.content.startswith('!Shop') or message.content.startswith(
            '!price') or message.content.startswith('!shop'):
        found = False
        for items in Items:
            if (items[1] == ""):
                break
            print(items[1])

            if items[1] == message.content[7:] and items[1] != "Name":
                print(" | ".join(items))

                await channel.send(" | ".join(items[1:8]))
                await channel.send()
                found = True

    if message.content.startswith('!Char') or message.content.startswith('!Characters') or message.content.startswith(
            '!characters') or message.content.startswith('!char'):
        # This command is to get all of a player's characters by reading from their discord names and comapring them to
        #google sheets names and printing all that are the same.

        # await channel.send(message.author.nick)
        # print(wks.get_all_values())
        holder3 = 0
        for array in Census.get_all_values():
            # holder = message.content.split()
            # print(holder[1] + " " + holder[2])

            if array[12] == message.author.nick:
                print(array[12] + str(message.author.nick))
                holder = ""
                holder2 = "true"
                holder3 = holder3 + 1
                for adding in array:
                    if holder2 == "false":
                        if adding != "":
                            holder = holder + " " + adding + " /"
                    else:
                        holder2 = "false"
                        await channel.send("Slot: " + str(holder3))
                await channel.send(holder + "\n")

    #level up function that currently
    """elif message.content.startswith('!lvlup') or message.content.startswith('!levelup') or message.content.startswith(
            '!13v31up'):
        from datetime import date
        today = date.today()
        input = message.content.split()
        channel = message.channel
        print(int(input[1]))
        if not (input[1].isdigit()):
            await channel.send("Error reading slot number")
        if input[2].isdigit():
            await channel.send("Error Class")
        else:
            slot = input[1]
            for array in Census.get_all_values():
                array[0] = today.strftime("%B/%d,/%Y")
                # holder = message.content.split()
                # print(holder[1] + " " + holder[2])
                if array[12] == message.author.nick:
                    array[13] = "FALSE"
                    if slot != "1":
                        slot = int(slot) - 1
                    else:
                        array[4] = int(array[4]) + 1
                        if array[0] == input[2]:
                            array[5] = str(array[5])
                        elif array[5] == input[2]:
                            array[5] = str(array[5])
                        elif array[5] == input[2]:
                            array[5] = str(array[5])
                        elif array[5] == "":
                            array[5] = input[2]
                        elif array[7] == "":
                            array[7] = input[2]
                        elif array[9] == "":
                            array[9] = input[2]
                        Census.append_table(values=array)
"""


# print(wks.get_all_values())

client.run(token)

# open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
