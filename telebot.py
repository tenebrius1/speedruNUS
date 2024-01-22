import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import pandas as pd
import numpy as np

TELEBOT_KEY = "<TELEBOT_KEY>"
BASE_URL = "https://nusmods.com/courses/"

START_MESSAGE = \
"""
Welcome to speedruNUS\!

Every student in NUS has some UEs they want to clear and we can help you find the modules that require the least amount of effort with no grading 😎

You have to fill up a questionnaire which will judge your aptitude and recommend the best combination to ZOOM 🏎️ to graduation\!

To begin, type\: /begin \<Units\>
Where \<Units\> is the number of Units you still need to fulfill\! 
\(Undergraduates need to fulfill at least 32 Units of UEs\)
"""

RC_CAPTION = \
"""You begin your journey in NUS and walk past various RCs\.
I hope your room is as nice as this, but do you currently stay in a RC\?
"""

FACULTY_CAPTION = \
"""
You feel your vision fading and when you open your eyes again, you find yourself in front of your own faculty\. What do you see\?
"""

CFG_CAPTION = \
"""
You then find yourself walking along a road with many passersby\. Some greet you, and introduce themselves, while others bump past you in a bid to rush off\.

How would you feel\? 🚶

1\. Horrible\. I hate social situations and I’m sure of my own path that I’m taking in life\.
2\. Ambivalent\. It’ll be nice to learn more but it’s not really that needed\.
3\. Great\! I love making new connections and would like to learn more soft skills to do so\!
"""

FASS_CAPTION = \
"""
Continuing on the road, you see a few teenagers spray painting a wall and writing poems using makeshift pencils out of charcoal\.

What would you do\? ✏️

1\. Quickly walk past, you shun anything arts\-related\.
2\. Stay a while and observe, no harm in checking it out\.
3\. Join in\! Freedom of expression is of utmost importance\.
"""

COM_CAPTION = \
"""
The road leads to a tall tower, and there is an access panel beside the door\. You see the panel has a puzzle that needs recursion\. But you also see an override button to open the door\.

What would you do\? 🧑‍💻

1\. I’m pressing the open button before reading the puzzle\. No time for that\.
2\. You glance over the puzzle and think about the solution\.
3\. It’s been 2 hours\. You still have 2 private test cases failing but you will NEVER give up\.
"""

CDE_CAPTION = \
"""
You open the door and find a small elf\-like creature tinkering with a machine\. He tells you that the purpose of the contraption is to close the curtains using a lever in the morning\. As he demonstrates the machine, it gets jammed halfway\.

What would you do\? 🧝

1\. Take the stairs up to the next floor, nothing to do here\.
2\. Discuss some potential issues with the elf then make your merry way\.
3\. Grab a wrench off the floor and tighten a few bolts\. Your work has just begun\.
"""

BUSINESS_CAPTION = \
"""
Leaving the elf, you reach a floor filled with glass rooms with people in heated discussions on different projects\. You are suddenly pulled into one of the rooms and shown a presentation with slides for marketing a product\.

You spot a few errors in the presentation, what do you do\? 📈

1\. Leave\. Not your product, not your problem\.
2\. Stay a little and tell them the errors then leave\.
3\. Go through the strategy slide by slide, the 4Ps of marketing has not left you yet
"""

MEDICINE_CAPTION = \
"""
On the next floor, you find yourself in a museum filled with human body parts\. A wiry looking lab technician scurries to you and asks if you want a tour of the place\.

What do you do\? 🧠

1\. You politely decline and move on\.
2\. You agree, curious to see what they have in stock\.
3\. Marveling at the different organs, you consistently press on for more information during the tour\.
"""

PUBLIC_HEALTH_CAPTION = \
"""
Almost at the top of the tower, the second last floor showcases people around a table, talking about a new health policy\. You spy an empty seat in the corner of your eye\.

What do you do\? 🧑‍⚖️

1\. Walk up the final flight of stairs\. These things are best left to others\.
2\. Listen in on the side, butting in when needed\.
3\. Join in\. It’s up to you to change the future\.
"""

YST_CAPTION = \
"""
As you approach the end of your journey, panting up the final flight of stairs, you hear the symphony of an angelic choir\. You walk towards the light, towards the end\.

How would you feel\?

1\. You would rather listen to the grunts of an old catfish than listen to classical music\.
2\. You walk and enjoy the music\. Not your favourite song, but it’ll do\.
3\. You bask in the radiance\. You will never forget this moment for the rest of your life\.
"""

END_OF_QUIZ_MSG = \
"""
Congratulations on finishing your journey\! We hope you enjoyed at least some of the encounters along the way\! 👏

You may now go through a curated queue of modules\.
If you want to take the module, press “Yes ✅” and it will be added to your list of modules\.
If not, press “No ❌” and we’ll show you the next best thing based on your preferences\!
To view the modules you have selected so far, press “View All 👀”

Let’s go\!\! 🏁
"""

WISHLIST_MSG = \
"""
We hope this helped you ZOOM through uni\!

Here are the list of modules you chose:
""" 

# USER RELATED DATA
users_mods_mapping = {}
user_preferences = {}

# MODULES
mods_master_df = pd.read_csv("master_list.csv")

bot = telebot.TeleBot(TELEBOT_KEY, parse_mode="MarkdownV2")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    bot.send_message(message.chat.id, START_MESSAGE)

@bot.message_handler(commands=['begin'])
def handle_begin(message):
    user_id = message.from_user.id
    users_mods_mapping[user_id] = {}
    user_preferences[user_id] = {}
    parts = message.text.split()
    if len(parts) != 2:
        bot.reply_to(message, "Please enter the number of Units you still need to fulfill\!")
        return
    else:
        units = int(parts[1])
        if units > 48:
            bot.reply_to(message, "There should be an upper limit to how lazy you are\. Please enter a number less than 48\n\(jkay there is an upper limit of 48 Units of UEs for undergrads\)")
            return
        else:
            user_id = message.from_user.id
            user_preferences[user_id]['units'] = units
            users_mods_mapping[user_id]['units_left'] = units
            bot.send_message(message.chat.id, "Great\! Let's begin\!")

            markup = InlineKeyboardMarkup()
            tembu = InlineKeyboardButton("Tembusu", callback_data='rc_tembu')
            capt = InlineKeyboardButton("CAPT", callback_data='rc_capt')
            rc4 = InlineKeyboardButton("RC4", callback_data='rc_rc4')
            yale = InlineKeyboardButton("Yale-NUS", callback_data='rc_yale')
            no_rc = InlineKeyboardButton("No RC", callback_data='rc_none')
            bot.send_photo(message.chat.id, open('double-room.png', 'rb'), caption=RC_CAPTION, reply_markup=markup.add(tembu, capt, rc4, yale, no_rc))

@bot.callback_query_handler(func=lambda call: call.data.startswith('rc_'))
def handle_rc(call):
    user_id = call.from_user.id
    user_preferences[user_id]['Tembusu College'] = -10
    user_preferences[user_id]['College of Alice and Peter Tan'] = -10
    user_preferences[user_id]['Residential College 4'] = -10
    user_preferences[user_id]['Yale-NUS College'] = -10
    if call.data == 'rc_tembu':
        user_preferences[user_id]['Tembusu College'] = 10
    elif call.data == 'rc_capt':
        user_preferences[user_id]['College of Alice and Peter Tan'] = 10
    elif call.data == 'rc_rc4':
        user_preferences[user_id]['Residential College 4'] = 10
    elif call.data == 'rc_yale':
        user_preferences[user_id]['Yale-NUS College'] = 10
    
    markup = InlineKeyboardMarkup()
    fass = InlineKeyboardButton("Too many readings. I’m from FASS 🎨", callback_data='faculty_fass')
    com = InlineKeyboardButton("A poster of SOCCAT! I’m from Computing 🖱️", callback_data='faculty_com')
    cde = InlineKeyboardButton("A real-life racecar. I’m from CDE 🏗️", callback_data='faculty_cde')
    yst = InlineKeyboardButton("A conservatory, I’m from YST 🎵", callback_data='faculty_yst')
    med = InlineKeyboardButton("White coats galore! I’m from Medicine 💊", callback_data='faculty_med')
    biz = InlineKeyboardButton("A little too much class participation! I’m from Business 🐍", callback_data='faculty_biz')
    sci = InlineKeyboardButton("Labs, labs everywhere! I’m from Science 🧑‍🔬", callback_data='faculty_sci')

    markup.add(fass)
    markup.add(com)
    markup.add(cde)
    markup.add(yst)
    markup.add(med)
    markup.add(biz)
    markup.add(sci)
    bot.send_photo(call.message.chat.id, open('faculty.png', 'rb'), caption=FACULTY_CAPTION, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('faculty_'))
def handle_faculty(call):
    user_id = call.from_user.id
    if call.data == 'faculty_fass':
        user_preferences[user_id]['Arts and Social Science'] = 5
    elif call.data == 'faculty_com':
        user_preferences[user_id]['Computing'] = 5
    elif call.data == 'faculty_cde':
        user_preferences[user_id]['College of Design and Engineering'] = 5
    elif call.data == 'faculty_yst':
        user_preferences[user_id]['YST Conservatory of Music'] = 5
    elif call.data == 'faculty_med':
        user_preferences[user_id]['Yong Loo Lin Sch of Medicine'] = 5
    elif call.data == 'faculty_biz':
        user_preferences[user_id]['NUS Business School'] = 5
    elif call.data == 'faculty_sci':
        user_preferences[user_id]['Science'] = 5
    
    markup = InlineKeyboardMarkup()
    bad = InlineKeyboardButton("1", callback_data='cfg_bad')
    okay = InlineKeyboardButton("2", callback_data='cfg_okay')
    good = InlineKeyboardButton("3", callback_data='cfg_good')

    markup.add(bad, okay, good)
    bot.send_photo(call.message.chat.id, open('cfg.png', 'rb'), caption=CFG_CAPTION, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('cfg_'))
def handle_cfg(call):
    user_id = call.from_user.id
    if call.data == 'cfg_bad':
        user_preferences[user_id]['NUS'] = 0
    elif call.data == 'cfg_okay':
        user_preferences[user_id]['NUS'] = 1
    elif call.data == 'cfg_good':
        user_preferences[user_id]['NUS'] = 3
    
    markup = InlineKeyboardMarkup()
    bad = InlineKeyboardButton("1", callback_data='fass_bad')
    okay = InlineKeyboardButton("2", callback_data='fass_okay')
    good = InlineKeyboardButton("3", callback_data='fass_good')
    markup.add(bad, okay, good)
    bot.send_photo(call.message.chat.id, open('arts.png', 'rb'), caption=FASS_CAPTION, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('fass_'))
def handle_fass(call):
    user_id = call.from_user.id
    if call.data == 'fass_bad':
        user_preferences[user_id]['Arts and Social Science'] = user_preferences[user_id].get('fass', 0)
    elif call.data == 'fass_okay':
        user_preferences[user_id]['Arts and Social Science'] = user_preferences[user_id].get('fass', 0) + 1
    elif call.data == 'fass_good':
        user_preferences[user_id]['Arts and Social Science'] = user_preferences[user_id].get('fass', 0) + 3
    
    markup = InlineKeyboardMarkup()
    bad = InlineKeyboardButton("1", callback_data='com_bad')
    okay = InlineKeyboardButton("2", callback_data='com_okay')
    good = InlineKeyboardButton("3", callback_data='com_good')
    markup.add(bad, okay, good)
    bot.send_photo(call.message.chat.id, open('com.jpg', 'rb'), caption=COM_CAPTION, reply_markup=markup)
    
@bot.callback_query_handler(func=lambda call: call.data.startswith('com_'))
def handle_com(call):
    user_id = call.from_user.id
    if call.data == 'com_bad':
        user_preferences[user_id]['Computing'] = user_preferences[user_id].get('com', 0)
    elif call.data == 'com_okay':
        user_preferences[user_id]['Computing'] = user_preferences[user_id].get('com', 0) + 1
    elif call.data == 'com_good':
        user_preferences[user_id]['Computing'] = user_preferences[user_id].get('com', 0) + 3
    
    markup = InlineKeyboardMarkup()
    bad = InlineKeyboardButton("1", callback_data='cde_bad')
    okay = InlineKeyboardButton("2", callback_data='cde_okay')
    good = InlineKeyboardButton("3", callback_data='cde_good')
    markup.add(bad, okay, good)
    bot.send_photo(call.message.chat.id, open('cde.jpeg', 'rb'), caption=CDE_CAPTION, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('cde_'))
def handle_cde(call):
    user_id = call.from_user.id
    if call.data == 'cde_bad':
        user_preferences[user_id]['College of Design and Engineering'] = user_preferences[user_id].get('cde', 0)
    elif call.data == 'cde_okay':
        user_preferences[user_id]['College of Design and Engineering'] = user_preferences[user_id].get('cde', 0) + 1
    elif call.data == 'cde_good':
        user_preferences[user_id]['College of Design and Engineering'] = user_preferences[user_id].get('cde', 0) + 3
    
    markup = InlineKeyboardMarkup()
    bad = InlineKeyboardButton("1", callback_data='biz_bad')
    okay = InlineKeyboardButton("2", callback_data='biz_okay')
    good = InlineKeyboardButton("3", callback_data='biz_good')
    markup.add(bad, okay, good)
    bot.send_photo(call.message.chat.id, open('biz.png', 'rb'), caption=BUSINESS_CAPTION, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('biz_'))
def handle_biz(call):
    user_id = call.from_user.id
    if call.data == 'biz_bad':
        user_preferences[user_id]['NUS Business School'] = user_preferences[user_id].get('biz', 0)
    elif call.data == 'biz_okay':
        user_preferences[user_id]['NUS Business School'] = user_preferences[user_id].get('biz', 0) + 1
    elif call.data == 'biz_good':
        user_preferences[user_id]['NUS Business School'] = user_preferences[user_id].get('biz', 0) + 3
    
    markup = InlineKeyboardMarkup()
    bad = InlineKeyboardButton("1", callback_data='med_bad')
    okay = InlineKeyboardButton("2", callback_data='med_okay')
    good = InlineKeyboardButton("3", callback_data='med_good')
    markup.add(bad, okay, good)
    bot.send_photo(call.message.chat.id, open('med.png', 'rb'), caption=MEDICINE_CAPTION, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('med_'))
def handle_med(call):
    user_id = call.from_user.id
    if call.data == 'med_bad':
        user_preferences[user_id]['Yong Loo Lin Sch of Medicine'] = user_preferences[user_id].get('med', 0)
    elif call.data == 'med_okay':
        user_preferences[user_id]['Yong Loo Lin Sch of Medicine'] = user_preferences[user_id].get('med', 0) + 1
    elif call.data == 'med_good':
        user_preferences[user_id]['Yong Loo Lin Sch of Medicine'] = user_preferences[user_id].get('med', 0) + 3
    
    markup = InlineKeyboardMarkup()
    bad = InlineKeyboardButton("1", callback_data='ph_bad')
    okay = InlineKeyboardButton("2", callback_data='ph_okay')
    good = InlineKeyboardButton("3", callback_data='ph_good')
    markup.add(bad, okay, good)
    bot.send_photo(call.message.chat.id, open('ph.png', 'rb'), caption=PUBLIC_HEALTH_CAPTION, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('ph_'))
def handle_ph(call):
    user_id = call.from_user.id
    if call.data == 'ph_bad':
        user_preferences[user_id]['SSH School of Public Health'] = 0
    elif call.data == 'ph_okay':
        user_preferences[user_id]['SSH School of Public Health'] = 1
    elif call.data == 'ph_good':
        user_preferences[user_id]['SSH School of Public Health'] = 3
    
    markup = InlineKeyboardMarkup()
    bad = InlineKeyboardButton("1", callback_data='yst_bad')
    okay = InlineKeyboardButton("2", callback_data='yst_okay')
    good = InlineKeyboardButton("3", callback_data='yst_good')
    markup.add(bad, okay, good)
    bot.send_photo(call.message.chat.id, open('yst.png', 'rb'), caption=YST_CAPTION, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('yst_'))
def handle_yst(call):
    user_id = call.from_user.id
    if call.data == 'yst_bad':
        user_preferences[user_id]['YST Conservatory of Music'] = user_preferences[user_id].get('yst', 0)
    elif call.data == 'yst_okay':
        user_preferences[user_id]['YST Conservatory of Music'] = user_preferences[user_id].get('yst', 0) + 1
    elif call.data == 'yst_good':
        user_preferences[user_id]['YST Conservatory of Music'] = user_preferences[user_id].get('yst', 0) + 3
    
    bot.send_message(call.message.chat.id, END_OF_QUIZ_MSG)

    # Send the first module option
    ranked_mod_list = get_ranked_mod_list(user_id)
    users_mods_mapping[user_id]['current_index'] = 0  # Initialize current index

    if users_mods_mapping[user_id]['units_left'] > 0 and ranked_mod_list:
        send_module_option(user_id, call.message.chat.id, ranked_mod_list, 0)

def send_module_option(user_id, chat_id, ranked_mod_list, index):
    mod_code = ranked_mod_list[index]
    message = format_message(user_id, mod_code)
    markup = InlineKeyboardMarkup()
    no = InlineKeyboardButton("No", callback_data=f'res_{mod_code}_no')
    yes = InlineKeyboardButton("Yes", callback_data=f'res_{mod_code}_yes')
    markup.add(no, yes)
    bot.send_message(chat_id, message, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('res_'))
def handle_res(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    data_parts = call.data.split('_')
    mod_code, response = data_parts[1], data_parts[2]

    # Process the user's response
    if response == 'yes':
        # Corrected way to get module credit as a single value
        module_credit = mods_master_df.loc[mods_master_df['moduleCode'] == mod_code, 'moduleCredit'].squeeze()
        if pd.notna(module_credit):
            users_mods_mapping[user_id]['units_left'] -= module_credit
            users_mods_mapping[user_id].setdefault("wishlist", []).append(mod_code)

    # Move to the next module option
    users_mods_mapping[user_id]['current_index'] += 1
    index = users_mods_mapping[user_id]['current_index']
    ranked_mod_list = get_ranked_mod_list(user_id)

    if users_mods_mapping[user_id]['units_left'] > 0 and index < len(ranked_mod_list):
        send_module_option(user_id, chat_id, ranked_mod_list, index)
    elif index >= len(ranked_mod_list):
        # Handle the end of the module options
        bot.send_message(chat_id, "You've reviewed all options\.")
    else:
        bot.send_message(chat_id, WISHLIST_MSG)
        final_mod_msg = format_wishlist(user_id)
        bot.send_message(chat_id, final_mod_msg)


def format_message(user_id, module_code) -> str:
    mod_info = mods_master_df[mods_master_df['moduleCode'] == module_code].iloc[0]
    mod_code = mod_info['moduleCode']
    mod_title = mod_info['title'].replace('.', '\.').replace('-', '\-',).replace('(', '\(').replace(')', '\)')
    mod_credit = int(mod_info['moduleCredit']) if mod_info['moduleCredit'].is_integer() else str(mod_info['moduleCredit']).replace('.', '\.')
    mod_origin = mod_info['faculty'].replace('.', '\.').replace('-', '\-',) + ' \| ' + '_' + mod_info['department'].replace('.', '\.').replace('-', '\-',) + '_'
    mod_description = mod_info['description'].replace('.', '\.').replace('-', '\-',).replace('(', '\(').replace(')', '\)').replace('+', '\+')
    mod_units_left = int(users_mods_mapping[user_id]['units_left']) if 'units_left' in users_mods_mapping[user_id] else 0
    return f"{mod_code} \({mod_credit} Units\)\n*{mod_title}*\n\n{mod_origin}\n\n{mod_description}\n\nYou have {mod_units_left} Units left\! 🏁"

def get_ranked_mod_list(user_id):
    # Copy for each user
    user_mods_df = mods_master_df.copy()
    user_mods_df['faculty'] = np.where(user_mods_df['faculty'] == "Residential College", user_mods_df['department'], user_mods_df['faculty'])
    user_preferences_df = pd.DataFrame.from_dict(user_preferences[user_id], orient='index')
    user_mods_df = user_mods_df.merge(user_preferences_df, left_on='faculty', right_index=True).rename(columns={0: 'score'})
    # Sort by score (descending)
    user_mods_df = user_mods_df.sort_values(by=['score'], ascending=False)
    return user_mods_df['moduleCode'].tolist()

def format_wishlist(user_id):
    wishlist = users_mods_mapping[user_id]['wishlist']
    msg = ""
    for mod in wishlist:
        title = mods_master_df[mods_master_df['moduleCode'] == mod]['title'].values[0].replace('-', '\-').replace('(', '\(').replace(')', '\)')
        mod_url = f"{BASE_URL}{mod}"
        num_units = mods_master_df[mods_master_df['moduleCode'] == mod]['moduleCredit'].values[0]
        num_units = str(int(num_units)) if num_units.is_integer() else str(num_units).replace('.', '\.')
        msg += f"{mod} \({num_units} Units\): [{title}]({mod_url})\n"
    return msg

if __name__ == "__main__":
    bot.polling()