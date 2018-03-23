
# coding: utf-8

# In[36]:


import telebot
from telebot import types

bot = telebot.TeleBot('575644509:AAF3oCfcW3gK5BrCXIHZSkVNrZFrcU2e9Q4')

markup_menu = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width=1)
btn_address1 = types.KeyboardButton('Погрешность')
btn_address2 = types.KeyboardButton('Метод наименьших квадратов')
markup_menu.add(btn_address1, btn_address2)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    msg = bot.send_message(message.chat.id, "Привет, я помогу тебе с лабой :)", reply_markup=markup_menu)
    bot.register_next_step_handler(msg, echo_all)
    

def echo_all(message):
    if message.text == 'Погрешность':
        msg = bot.send_message(message.chat.id,'Введи значения измеренной величины через пробел или запятую') 
        bot.register_next_step_handler(msg, x1)
    elif message.text == 'Метод наименьших квадратов':
        msg = bot.send_message(message.chat.id,'Введи значения X через пробел или запятую') 
        bot.register_next_step_handler(msg, X1)
        
def x1(message):
    global x
    x = [float(i) for i in message.text.split()] 
    msg = bot.send_message(message.chat.id,'Введи распределение Стьюдента: ')
    bot.register_next_step_handler(msg, tpf1)
    
def tpf1(message):
    tpf = float(message.text) 
    xs = 0 
    V = 0 
    for i in range(len(x)): 
        xs += x[i]/len(x) 
    for i in range(len(x)): 
        V += ((x[i]-xs)**2)/(len(x)-1) 
    S = V**(1/2) 
    msg = bot.send_message(message.chat.id, 'Среднее значение:   '+str(xs) ) 
    msg = bot.send_message(message.chat.id, 'Погрешность составляет:   ' + str(V))
    msg = bot.send_message(message.chat.id, 'Стандартное отклонение:   ' + str(S))
    msg = bot.send_message(message.chat.id, 'Относительное стандартное отклонение:   '+ str(S/xs)) 
    msg = bot.send_message(message.chat.id, 'Доверительный интервал составляет   ± ' + str(tpf*S/((len(x)**(1/2)))), reply_markup=markup_menu)
    bot.register_next_step_handler(msg, echo_all)

def X1(message):
    global X
    X = [float(i) for i in message.text.split()]
    msg = bot.send_message(message.chat.id,'Введи значения Y через пробел или запятую') 
    bot.register_next_step_handler(msg, Y1)
    
def Y1(message):
    global Y
    Y = [float(i) for i in message.text.split()]
    y = 0
    x = 0
    xy = 0
    xx = 0
    yy = 0
    for i in range(len(Y)):
        y += Y[i]
        x += X[i]
        xy += X[i]*Y[i]
        xx += X[i]**2
        yy += Y[i]**2
    b = (y*xx - x*xy)/(len(Y)*xx - x**2)
    a = (len(Y)*xy - x*y)/(len(Y)*xx - x**2)
    msg = bot.send_message(message.chat.id, 'Уравнение прямой имеет вид : y = ' + str(a) + '*x + ' + str(b), reply_markup=markup_menu)
    bot.register_next_step_handler(msg, echo_all)

bot.polling()

