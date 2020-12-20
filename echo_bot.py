import telebot
from telebot import types

import time
import json


#creating a bot instance
bot = telebot.TeleBot("1415374930:AAHfQmdaLrzYDQxYhNXTa0L7xOtTljE5r7s")

STICKER_ID = 'CAACAgIAAxkBAANqX9j3Q9NNtVlV8IgMMr9NbAWBiJ8AAukBAAJWnb0KMRoixENZlv8eBA'
AUDIO_ID = 'CQACAgIAAxkBAANvX9j5tCmrs3Y7CWPWyOt1qZLcXbgAAigJAAJ8DshKQpEH_cqd494eBA'
DOCUMENT = "BQACAgIAAxkBAAOGX9kAAevFKqIj4WPOf0klTJEJD-LhAAJKCgACTCbISloChaCm-VzVHgQ"



knownUsers = []  # todo: save these in a file,
userStep = {}  # so they won't reset every time the bot restarts

commands = {  # command description used in the "help" command
    'start'       : 'Get used to the bot',
    'help'        : 'Gives you information about the available commands',
    'sendLongText': 'A test using the \'send_chat_action\' command',
    'getImage'    : 'A test using multi-stage messages, custom keyboard, and media sending'
}

imageSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True)  # create the image selection keyboard
imageSelect.add('Mickey', 'Minnie')# added two buttons

hideBoard = types.ReplyKeyboardRemove()  # if sent as reply_markup, will hide the keyboard

def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
        print("New user detected, who hasn't used \"/start\" yet")
        return 0

@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if cid not in knownUsers:  # if user hasn't used the "/start" command yet:
        knownUsers.append(cid)  # save user id, so you could brodcast messages to all users of this bot later
        userStep[cid] = 0  # save user id and his current "command level", so he can use the "/getImage" command
        bot.send_message(cid, "Hello, stranger, let me scan you...")
        bot.send_message(cid, "Scanning complete, I know you now")
        command_help(m)  # show the new user the help page

    else:
        bot.send_message(cid, "I already know you, no need for me to scan you again!")

 #help page
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "The following commands are available: \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  # send the generated help page        


# chat_action example (not a good one...)
@bot.message_handler(commands=['sendLongText'])
def command_long_text(m):
    cid = m.chat.id
    bot.send_message(cid, "If you think so...")
    bot.send_chat_action(cid, 'typing')  # show the bot "typing" (max. 5 secs)
    time.sleep(3)
    bot.send_message(cid, ".")

    # user can chose an image (multi-stage command example)
@bot.message_handler(commands=['getImage'])
def command_image(m):
    cid = m.chat.id
    bot.send_message(cid, "Please choose your image now", reply_markup=imageSelect)  # show the keyboard
    userStep[cid] = 1  # set the user to the next step (expecting a reply in the listener now)
    #bot.send_message(cid, "Please choose your image now", reply_markup=imageSelect)  # show the keyboard
    #userStep[cid] = 1  # set the user to the next step (expecting a reply in the listener now)

@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)
def msg_image_select(m):
    cid = m.chat.id
    text = m.text

    # for some reason the 'upload_photo' status isn't quite working (doesn't show at all)
    bot.send_chat_action(cid, 'typing')

    if text == 'Mickey':  # send the appropriate image based on the reply to the "/getImage" command
        bot.send_photo(cid, open('rooster.jpg', 'rb'),
                       reply_markup=hideBoard)  # send file and hide keyboard, after image is sent
        userStep[cid] = 0  # reset the users step back to 0
    elif text == 'Minnie':
        bot.send_photo(cid, open('kitten.jpg', 'rb'), reply_markup=hideBoard)
        userStep[cid] = 0
    else:
        bot.send_message(cid, "Please, use the predefined keyboard!")
        bot.send_message(cid, "Please try again")

	

@bot.message_handler(commands = ['getmusic','getsticker','getdocument'])
def getmusic_and_sticker(message):
	if "getmusic" in message.text:
		bot.send_audio(message.chat.id, AUDIO_ID)
	if "getsticker" in message.text:
		bot.send_sticker(message.chat.id, STICKER_ID)
	if "getdocument" in message.text:
		bot.send_document(message.chat.id, DOCUMENT)	

bot.polling(none_stop = True)






