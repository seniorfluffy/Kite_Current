import math
import operator
import os
import random
import re
import time

from Config import Footer
import discord
import pygsheets

# this is a application to create a discord bot to allow for the general function of delta nu delta's dungeons and dragons system
# each player can have one multiple charecters and each person needs to be able to get the infromation about each item in
# the system.
# the primary function of this application is to keep track of players data and allow for players to access data about the system.
# gets the client secret file and authroizes bot to use google api and sheets

gc = pygsheets.authorize()
# api key for google sheets
# from a secret python file to allow for file to be uploaded to github

token = "NjIzNjI2NjUzODUwOTI3MTE0.XmNnAQ.z3X9ALIqK0yaL38InqMDBE9wndc"
client = discord.Client()

# this to get this sheet https://docs.google.com/spreadsheets/d/1oCgn7laejTuV0lqdxDqvi3qNhuW6JtSfwv26pmLrS94/edit$usp=sharing
sh = gc.open("Delta Nu Delta - Character Census Spreadsheet beta")
# select the first sheet
Census = sh[0]

# select all of the magic item sheets
AllItems = gc.open("Magic Items")

Uncommon = AllItems[0]
Rare = AllItems[1]
VRare = AllItems[2]
Items = []
uncommon = []
rare = []
vrare = []
f = open("holder.txt", "a")
f.close()


# does the downtime calculations
def downtime(numbers, additive):
    holder = ""
    holder2 = 0
    numbers = int(numbers)
    additive = int(additive)
    for number in range(1, numbers):
        roll = random.randint(1, 20)
        added = roll + additive;
        rounded = str(5 * math.ceil(added / 5))
        holder2 = holder2 + int(rounded)
        holder = holder + (" " + str(additive) + " + " + str(roll) + " = " + str(rounded) + " (" + str(holder2) + ") ")

    return holder, holder2


# reads from drive sheets and turns each sheet into an array
def readFromDrive(a, b):
    for array in a:
        if array[1] == "":
            break
        if array[1] == "name":
            break
        b.append(array)


# loads all sheets
readFromDrive(Uncommon.get_all_values(), uncommon)
readFromDrive(Rare.get_all_values(), rare)
readFromDrive(VRare.get_all_values(), vrare)
readFromDrive(uncommon, Items)
readFromDrive(rare, Items)
readFromDrive(vrare, Items)


# compares how simular two strings are
def comparestrings(string1, string2):
    if len(string1[1:]) == 0 or len(string2[1:]) == 0:
        return 0
    if string1[0] == string2[0]:
        return 1 + comparestrings(string1[1:], string2[1:])
    else:
        return comparestrings(string1[1:], string2[1:])


async def itemSend(message, item):
    embed = discord.Embed(
        title=item[0],
        description=item[10],
    )
    randFooter = random.choice(Footer)
    embed.set_footer(text=randFooter)
    embed.add_field(name="List item: " + str(item[0]), value=str(
        "Type: " + str(item[1]) + "\n" +
        "Rarity: " + str(item[2]) + "\n" +
        "Attunment: " + str(item[3]) + "\n" +
        "Price GP: " + str(item[5]) + "\n" +
        "Tool : " + str(item[6]) + "\n" +
        "Book: " + str(item[7]) + "\n" +
        "Notes: " + str(item[4]) + "\n"
    ))
    await message.channel.send(embed=embed)


# a function to randomly pick 3 items from a given array
def randomPick(type):
    done = True
    holder = []
    print(type)
    randPick = random.choices(type, k=3)
    holder.append(randPick)
    print(randPick)
    return holder


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord$')

    # for server in client.servers:
    #     for channel in server.channels:
    #         if channel.name == 'general':
    #             await client.send_message(channel, "Kite Has Entered The Server, type $help For more information in bot chat")


Wiley = False


# 244275535188983808
@client.event
async def on_message(message):
    channel = message.channel

    # an optional "feature" to make a joke to a friend if Wiley Knight attempts to send a message the bot will reply by
    # calling them a vampire
    if str(message.author.nick) == "Wiley Knight" and Wiley == True:
        await channel.send("stop trying to break the bot you vampire")
    # A command to pick three items from each sheet and output the selected

    if message.content.startswith('$Help') or message.content.startswith('$help'):
        embed = discord.Embed(
            title="Help",
            description="I need a hero",
        )
        randFooter = random.choice(Footer)
        embed.set_footer(text=randFooter)
        embed.add_field(name="$gold", value=str(
            "Calculates gold recieved for quests\n"
            "Format $gold (level) (difficulty)\n\n"
            "for example if you are a 5th level charecter who went on a 8 difficulty mission you would type:"
            "\n$gold 5 8"
        ), inline=False)
        embed.add_field(name="$downtime", value=str(
            "Calculates downtime roles\n"
            "Format: $downtime (downtime days used) (highest ability score modifier)\n"
            "\nexample if you have a 18 dex and that's your highest scrore you wanted to convert 10 downtime days to "
            "gold\n "
            "$downtime 10 4 \n"
        ), inline=False)
        embed.add_field(name="$price", value=str(
            "looks up a item from the westmarch item document and displays relevent information\n"
            "Format: $price (item Name)"
        ))
        await message.channel.send(embed=embed)
    if message.content.startswith('$gold') or message.content.startswith('$Gold'):
        try:
            input = message.content.split(" ")
            if input[1].upper() == "HELP":
                embed = discord.Embed(
                    title="$Gold",
                    description="Calculates post game gold income ",
                )
                randFooter = random.choice(Footer)
                embed.set_footer(text=randFooter)
                embed.add_field(name="$GOLD", value=str(
                    "Format $gold (level) (difficulty)\n\n"
                    "for example if you are a 5th level charecter who went on a 8 difficulty mission you would type:"
                    "\n$gold 5 8"
                ))
                await message.channel.send(embed=embed)
            elif int != type(int(input[1])) or int != type(int(input[2])):
                embed = discord.Embed(
                    title="Whoops$ something got entered wrong",
                    description="Calculates post game gold income ",
                )
                randFooter = random.choice(Footer)
                embed.set_footer(text=randFooter)
                embed.add_field(name="Gold", value=str(
                    "Format $gold (level) (difficulty)\n\n"
                    "for example if you are a 5th level character who went on a 8 difficulty mission you would type:"
                    "\n$gold 5 8"
                ))
                await message.channel.send(embed=embed)
            elif int(input[1]) > 20 and int(input[2]) > 40:
                await message.channel.send("error greater than level 20 or greater than cr 40")
            elif input[1] == "20":
                await message.channel.send(
                    "for a " + input[1] + "th level character and a Challenge rating of " + input[2] + " " + str(
                        320 + 30 * int(input[2])))
            else:
                await message.channel.send(
                    "a " + input[1] + "th level character going on a mission with a Challenge rating of " + input[
                        2] + " would earn:\n" + str(int(input[1]) * (10 + int(input[2])) + 20))
        except ValueError:
            print("gold error")

    if message.content.startswith('$RollItems') or message.content.startswith('$rollitems'):
        input = message.content.split(" ")
        if len(message.content) > 11:
            if input[1].upper() == "RollItems":
                embed = discord.Embed(
                    title="$Rollitems",
                    description="TOOL FOR WESTMARCH MASTERS. Randomly picks the items from the items list for the Westmarch rolled items list, ",
                )
                randFooter = random.choice(Footer)
                embed.set_footer(text=randFooter)
                embed.add_field(name="$GOLD", value=str(
                    "Format: $Rollitems"
                ))
                await message.channel.send(embed=embed)
        for items in random.sample(uncommon, k=7):
            await itemSend(message, items)
        for items in random.sample(rare, k=5):
            await itemSend(message, items)
        for items in random.sample(vrare, k=5):
            await itemSend(message, items)

    # a command to look up a magic item and get the price
    if message.content.startswith('$Price') or message.content.startswith('$Shop') or message.content.startswith(
            '$price') or message.content.startswith('$shop'):
            try:
                if message.content.upper() == re.compile('\\\$PRICE *') or message.content.upper()== "$PRICE":
                    embed = discord.Embed(
                        title="$Price",
                        description="Finds the price of items in the westmarch system \n \n to use type $price + the item you want to look up\n "
                                    "\n fo instance if you wanted to look up the 'carpet of flying' you would enter \n"
                                    "$price carpet of flying",
                    )
                    randFooter = random.choice(Footer)
                    embed.set_footer(text=randFooter)
                    await message.channel.send(embed=embed)
                else:
                    print("$".upper())
                    found = False
                    heap = []
                    for items in Items:
                        if items[0] != 'Name' and items[0] != "":

                            if "$PRICE " + items[0].upper() == message.content.upper():
                                print("got past name and items block")
                                await itemSend(message, items)
                                found = True
                            heap.append([items, comparestrings(items[0].upper(), message.content[7:].upper())])
                    heap.sort(key=operator.itemgetter(1), reverse=True)
                    if not found:
                        await message.channel.send("Could Not find the item do you mean one of these:")
                        counter = 1
                        os.remove("holder.txt")
                        f = open("holder.txt", "a")
                        for a in heap[:4]:
                            await message.channel.send(str(counter) + ". " + str((a[0])[0]) + " Price :" + str((a[0])[5]))
                            counter = counter + 1
                        f.close()
            except all:
                print("Price Error")



    if message.content.startswith('$Downtime') or message.content.startswith('$downtime'):
        try:
            Downtime = int(message.content.split(" ")[1])
            additive = int(message.content.split(" ")[2])

            if isinstance(additive, int) and isinstance(Downtime, int):
                if Downtime < 2000 and additive < 10:
                    a, b = downtime(Downtime, additive)
                    if len(a) > 1000:
                        await message.channel.send(" Total to big to display full results: \n Total :" + str(b))
                    else:
                        await message.channel.send("Results: " + str(a) + "\n" + " Total: " + str(b))
                else:
                    await message.channel.send(
                        "Error in downtime, either downtime rolled is greater than 2000 or additive is "
                        "greater than 10")
            else:
                await message.channel.send("enter in integers")
        except all:
            print("Downtime Error")

    if message.content.startswith('$Character') or message.content.startswith(
            '$character') or message.content.startswith('$char') or message.content.startswith('$Char'):
        # This command is to get all of a player's characters by reading from their discord names and comapring them to
        # google sheets names and printing all that are the same.

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
    # level up function that currently doesn
    """elif message.content.startswith('$lvlup') or message.content.startswith('$levelup') or message.content.startswith(
            '$13v31up'):
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
                    if slot $= "1":
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
    if message.content.startswith('$hack'):
        await channel.send("$Hacking the system :dark_sunglasses:")
        await channel.send("$r 1d20")
        time.sleep(1)
        await channel.send("Well that Didn't work")


# print(wks.get_all_values())

client.run(token)

# open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
