import telebot
from telebot import types

import time
import json
from bot_helper import print_list



#creating a bot instance
bot = telebot.TeleBot("1415374930:AAHfQmdaLrzYDQxYhNXTa0L7xOtTljE5r7s")








#reply_markup to dialogue(yes or no)
markup_create = types.ReplyKeyboardMarkup()
btn_yes = types.KeyboardButton('yes')
btn_no = types.KeyboardButton('no')
markup_create.add(btn_yes, btn_no)

#reply_markup to end dialogue
markup_remove = types.ReplyKeyboardRemove()


#list of bots users
list_users = []




@bot.message_handler(commands = ['start'])
def write_to_list(msg):
    send_to = msg.chat.id # chat id of the sender
    user = msg.from_user  # --> returns user object
    user_name = user.first_name 
    list_users.append(user_name) #add first_name to the list
    bot.send_message(send_to,'Hello {}'.format(user_name))
    #print_list(list_users) #-->> prints bot_users list



@bot.message_handler(commands = ['italic'])
def send_message_in_italic(msg):
    send_to = msg.chat.id 
    text = '<i>In the italic style</i>' # pass the text
    bot.send_message(send_to, text, parse_mode = 'html',disable_notification = False)
    

@bot.message_handler(func = lambda msg: msg.text == 'dialogue')
def show_dialogue_markup(msg):
    send_to = msg.chat.id 
    bot.send_message(send_to,'Are you happy?',reply_markup = markup_create)
    
@bot.message_handler(func = lambda msg: msg.text == 'yes')
def show_dialogue_markup(msg):
    send_to = msg.chat.id 
    bot.send_message(send_to,'Are you friendly?',reply_markup = markup_remove)

@bot.message_handler(func = lambda msg: msg.text == 'no')
def show_dialogue_markup(msg):
    send_to = msg.chat.id 
    bot.send_message(send_to,'Are you angry?',reply_markup = markup_remove)



@bot.inline_handler(lambda query: query.query == 'show')
def query_text(inline_query):
    try:
        r = types.InlineQueryResultArticle('1', 'Result', types.InputTextMessageContent('Result message.'))
        r2 = types.InlineQueryResultArticle('2', 'Result2', types.InputTextMessageContent('Result message2.'))
        bot.answer_inline_query(inline_query.id, [r, r2])
    except Exception as e:
        print(e)
    ''' 
@bot.message_handler(content_type = ['text'])
def print_list(msg):
    
    bot.reply_to(msg.chat.id, 'this is a list')



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
'''
bot.polling(none_stop = True)






