import pygame

import random
import time
import copy
pygame.init()
color_x = 0
img_x = 'blackmast.png'
# создание переменных
    # размер экрана
WIDTH = 700 
HEIGHT = 500

FPS = 50
    # цвета
RED = (255, 0, 0)
BLACK_RED = (117, 43, 43)
BROWN = (153,76,0)
YELLOW = (255,255,0)
BLUE = (0,0,255)
BLACK_BLUE = (0,51,102)
GREEN = (0, 200, 0)
BLACK_GREEN = (0,102,0)
BLACK = (0, 0, 0)
ORANGE = (255, 128, 0)
BACKGROUND = (0, 255, 100)
WHITE = (255, 255, 255)
BLACK_WHITE = (0, 0, 0, 128)
BLACK_PURPLE = (179, 78, 242, 0.76)
colors = [RED, GREEN, ORANGE, BACKGROUND]
# создание screen и  clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
# координаты мыши и состояние связанные с ней
x_mouse, y_mouse = 0, 0
x, y = 0, 0

click = False
id_card = 0

sort_choise = 0  # 0 - по значимости, 1 - по масти
# игровые состояния
start = False
played = 0 # состояние разыгрывание игры
game_state = 0
    #  остальное
played_card_check = 0

played_chips = 0 # количеств осыграных очков

combination,chips,multy = '',0,0 # комбинация, количество очков, множитель

chips_permen = 0
multy_permen = 0 

r = 100

combo_cards = []
    # таймеры и счетчик кадров
timer = 0
start_timer = 0 
frame_count = 0
# перменные для перехода назад между состояниями
Back = False
back_point = 0
back_frame = 0
end_timer = 1
# данные игрока
max_hand = 4
max_delete = 4
hand = 4 # рука
hand_play = 0 # кол-во сыгранных рук
delete = 4 # сбросы
delete_play = 0 # кол-во сыгранных сбросов
money = 4
joker_time = 0


ante = 1
reroll_cost = 4
# Данные для карт
Cards_var = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
Cards_point = ['2', '3', '4', '5', '6', '7', "8", "9", "10", "10", "10", "10", "11"]
Card_sort = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
masts = ["red", "black", "orange", "green"]
mast_order = {"red": 0, "black": 1, "orange": 2, "green": 3}
play_ruka = []
played_cards = []
# Колода карт
joker_play = True

coloda = []
coloda_copy = []
game_coloda = []
clicked = []
# прочее
img_blackmast = pygame.image.load('assets//blackmast.png')
img_greenmast = pygame.image.load('assets//greenmast.png')
img_redmast = pygame.image.load('assets//redmast.png')
img_orangemast = pygame.image.load('assets//orangemast.png')

ante_points = [100,300,800,2000,5000,11000,20000,35000,50000]
blind = 1
blind_multy = 1

update_rects = [] # список объектов которые нужно отрисовывать
# класс карты
class Card:
    # создание класса
    def __init__(self, x, y, w, h, mast, num, point, color, image, id, sort):
        self.rect = pygame.Rect(x, y, w, h)
        self.rect_inv = pygame.Rect(x, y, w, h + 5)
        self.mast = mast
        self.num = num
        self.point = point
        self.color = color
        self.rectimg = pygame.Rect(x, y + 20, w // 2, h // 3) 
        
        self.img = pygame.transform.scale(image, (w // 2, h // 3))
        self.is_hovered = False
        self.target_y = y
        self.base_y = y
        self.id = id
        self.sort = sort
        self.play_control = 0

    def draw(self):
        # Отрисовка карты
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
        screen.blit(self.img, self.rectimg)
        # Отрисовка текста (значение карты)
        font = pygame.font.SysFont(None, 18)
        text = font.render(f"{self.num} ", True, self.color)
        text2 = font.render(f"{self.num} ", True, self.color)
        screen.blit(text, (self.rect.x + 5, self.rect.y + 5))
        screen.blit(text2, (self.rect.x + 40, self.rect.y + 70))
    # функция выбора карты 
    
    def choise(self):
        
        
        global x_mouse, y_mouse, clicked
        if self.rect_inv.collidepoint(x_mouse, y_mouse):
            if not self.is_hovered:
                self.is_hovered = True
                self.target_y = self.base_y - 30
        else:
            if self.is_hovered:
                self.is_hovered = False
                self.target_y = self.base_y
        if self.rect in clicked:
            self.target_y = self.base_y - 30

        if self.rect.y > self.target_y:
            self.rect.y -= 5
            self.rectimg.y -= 5
            self.rect_inv.y -= 5
        elif self.rect.y < self.target_y:
            self.rect.y += 5
            self.rectimg.y += 5
            self.rect_inv.y += 5
    def move(self):
        if self.rect.y > self.target_y:
            self.rect.y -= 5
            self.rectimg.y -= 5
            self.rect_inv.y -= 5
        elif self.rect.y < self.target_y:
            self.rect.y += 5
            self.rectimg.y += 5
            self.rect_inv.y += 5
    # функция играния карты 
    def play(self):
        if self.play_control == 1:
            font = pygame.font.SysFont(None, 20)
            text3 = font.render(f"+{self.point} ", True, BLUE)
            screen.blit(text3, (self.rect.x + 20, self.rect.y - 15))
    # создание такой же карты 
    def copy(self):
        
        new_card = Card(
            x=self.rect.x,
            y=self.rect.y,
            w=self.rect.w,
            h=self.rect.h,
            mast=self.mast,
            num=self.num,
            point=self.point,
            color=self.color,
            image=self.img,  
            id=self.id,
            sort=self.sort
        )
        # Копируем остальные атрибуты
        new_card.rect_inv = pygame.Rect(
            self.rect_inv.x,
            self.rect_inv.y,
            self.rect_inv.w,
            self.rect_inv.h
        )
        new_card.rectimg = pygame.Rect(
            self.rectimg.x,
            self.rectimg.y,
            self.rectimg.w,
            self.rectimg.h
        )
        new_card.is_hovered = self.is_hovered
        new_card.target_y = self.target_y
        new_card.base_y = self.base_y
        new_card.play_control = self.play_control
        return new_card      
    
# класс джокеров
class Joker:
    # создание джокера
    def __init__(self,x,y,w,h,rare,multy,add,give_point,image,price,ability,name,info,info2,sort):    
        self.rect = pygame.Rect(x,y,w,h)
        self.name = name
        self.rare = rare
        self.price = price 
        self.ability = ability
        self.multy = multy
        self.add = add
        self.give_point  = give_point
        self.info = info
        self.info2 = info2 
        self.sort = sort
        self.image_path = image  
        self.img = pygame.image.load(image)  
        self.img = pygame.transform.scale(self.img, (w, h))
        self.choised = False
        self.clicked = False
        # интерфейс джокера
        self.joker_interface = [
            Object(x + 30,y,135,80,WHITE,f'{multy}{give_point} {add}',15,x+ 40,y+40,'','фон инфо',BLACK),    
            Object(700,700,1,1,WHITE,f'{name}',18, x+ 40,y +10,'','название',BLACK),
            Object(700,700,1,1,WHITE,f'{info2}',15,x+ 40,y+40,'','инфо2',BLACK), 
            Object(700,700,1,1,WHITE,f'{info}',15,x+ 40,y+40,'','инфо',BLACK),
        ]
        self.clicked_interface = [
            Object(x + 30,y,75,30,RED,f'продать за {price/2}',14,x+ 40,y+40,'sell','кнопка',WHITE),    
            
            
        ]    
    
    # отрисовка джокера
    def draw(self):
        
        screen.blit(self.img, self.rect)
        
    # отрисовка интерфейса джокера
    def draw_inter(self):
        global update_rects
        if self.choised and not self.clicked:
            for obj in self.joker_interface:
                obj.draw()

        elif self.clicked:
            for obj in self.clicked_interface:
                obj.draw()
                
    # выбор джокера
    def choise(self):
        global x_mouse, y_mouse  
        if self.rect.collidepoint(x_mouse,y_mouse):
            if not self.choised:
                self.choised = True
        else:
            if self.choised:
                self.choised = False     
    #  нажатие на джокер
    def click(self):
        
        if self.clicked:
            self.choised = False
            
            
             
            
#  класс объектов интерфейса без изображение
class Object:
    # создание объекта 
    def __init__(self, x, y, w, h, color, text, text_size, x_text, y_text, function, name,text_color):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.font = pygame.font.SysFont(None, text_size)
        self.text = self.font.render(f"{text}", True, text_color)
        self.x_text = x_text
        self.y_text = y_text
        if len(color) == 4 and color[3] != 255:
            self.surface = pygame.Surface((w, h), pygame.SRCALPHA)
        else:
            self.surface = None
        self.function = function
        self.name = name
        self.text_color = text_color
    # отрисовка объекта
    def draw(self):
        if self.surface:  
            self.surface.fill(self.color)  
            screen.blit(self.surface, self.rect)
        else: 
            pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text, (self.x_text, self.y_text))
    # функции объектов
    def func(self):
        
        
        global sort_choise,delete,played,r,hand,timer,game_state,start,coloda,coloda_copy,back_point,Back,hand_play,delete_play,chips_permen,multy_permen,blind,blind_multy,money,reroll_cost,played_chips,game_coloda
        
       
        if played != 1:
            # функция сброса
            if self.function == 'delete':
                if delete >= 1 and clicked:
                    for joke in invent_jokers:
                        if joke.name == 'игра фишек':
                            joke.give_point += len(clicked)
                    delete -= 1
                    delete_play += 1
                    for card in clicked:
                        game_coloda.remove(card)  
                    create_game_coloda(8 - len(game_coloda))
                    clicked.clear()
            #  функция сортировки
            if self.function == 'sort':
                if sort_choise == 0:
                    sort_choise = 1
                elif sort_choise == 1:
                    sort_choise = 0
            # играние руки
            if self.function == 'play':
                if hand >= 1:
                    if len(clicked) >= 1:
                        
                        for joke in invent_jokers:
                                if joke.name == 'игра фишек':
                                    joke.give_point += len(clicked)*2
                        
                        clicked_copy = clicked.copy()
                        for card_ in clicked_copy:
                            for card in game_coloda:
                                if card.rect == card_:
                                    
                                    played_cards.append(card)
                                    game_coloda.remove(card)
                                    clicked.remove(card)
                                    # Обновляем состояние карты
                                    card.target_y = 200  # Новая позиция для сыгранных карт
                                    card.base_y = 200  # Обновляем базовую позицию
                                    
                                    break
                        combination, chips, multy, combo_cards = determine_poker_combination(played_cards)
                        for card in combo_cards:
                            card.play_control = 1
                        played = 1  #
                        hand_play += 1 
                        r = 100
                        chips_permen = 0
                        multy_permen = 0 
                        hand -= 1
                        timer = 0
                        
        # начало игры                
        if self.function == 'start_game':
                start = True
                game_state = 1         
        # выход из паузы         
        if self.function == 'unpause': 
            game_state = 1
        # выход в меню        
        if self.function == 'menu':
            coloda.clear()  
            coloda_copy.clear() 
            game_coloda.clear()  
            clicked.clear()  
            played_cards.clear() 
            invent_jokers.clear()
            played = 0 
            game_state = 0
            blind = 1
            blind_multy = 1
        # настройки        
        if self.function == 'setting':
                game_state = 3
                
        # переход обратно посостоянию  
        if self.function == 'back':
                
            back_point = game_state - 1
            game_state = 1
            Back = True
        
        # обновление асортимента магазина 
        if self.function == 'reroll':
            if money >= reroll_cost:
                money -= reroll_cost
                reroll_cost += 1
                shop_update()
        # продолжени игры (выход из магазина)
        if self.function == 'resume':
            game_state = 1
            played_chips = 0
            hand = 4
            delete = 4
            game_coloda = []
            create_game_coloda(8)
            

            
            f = -600
            for i, card in enumerate(game_coloda):
                card.rect.x = (g * (i + 1)) - f
                card.rect.y = 360  # Основной rect
                card.base_y = 360
                card.target_y = 360

                
                card.rect_inv.x = card.rect.x
                card.rect_inv.y = card.rect.y
                card.rectimg.x = card.rect.x + 15  
                card.rectimg.y = card.rect.y + 20  
   
            
            
            
            
            
 # спрайты (объекты с изображениямми)                   
class Sprite:
    def __init__(self,x,y,w,h,image,name,function):
        self.rect = pygame.Rect(x,y,w,h)
        self.img = pygame.image.load(image)
        self.img = pygame.transform.scale(self.img, (w, h))
        self.name = name
        self.function = function
    
    def draw(self):
        
        screen.blit(self.img, self.rect)
    def func(self):
        return False
               
                                            
# создвние интерфейса
    # основной интерфейс игры
interface = [
    Object(45, 350, 495, 105, random.choice(colors), '', 1, 0, 0, '', 'фон рамки',WHITE),
    Object(40, 350, 5, 105, BLACK, '', 1, 0, 0, '', 'левая часть рамки',WHITE),
    Object(40, 450, 495, 5, BLACK, '', 1, 0, 0, '', 'нижняя часть рамки',WHITE),
    Object(535, 350, 5, 105, BLACK, '', 1, 0, 0, '', 'правая часть рамки',WHITE),
    Object(40, 350, 495, 5, BLACK, '', 1, 0, 0, '', 'верхняя часть рамки',WHITE),
    Object(WIDTH // 2 + 10, HEIGHT - 40, 150, 35, RED, 'Сброс', 20, WIDTH // 2 + 10 + 10, HEIGHT - 40 + 10, 'delete', 'сброс',WHITE),
    Object(WIDTH // 2 - 160, HEIGHT - 40, 150, 35, BLUE,'играть руку', 16, WIDTH // 2 - 160 + 10, HEIGHT - 40 + 10, 'play', 'игра руки',WHITE),
    Object(650, 465, 50, 50, BACKGROUND, str(len(coloda)), 30, 630, 475, '', 'кол-во карт',WHITE),
    Object(440, 320, 100, 30, ORANGE, 'значимости', 15, 440, 335, 'sort', 'кнопка сортировки',WHITE),
    Object(600, 320, 100, 30, BACKGROUND, 'сортировка по', 15, 440, 320, '', 'кнопка сортировки2',WHITE),
    Object(10,70,140,250,BLACK_GREEN,'Инфо',25,50,90,'','Инфо',WHITE),
    Object(15,230,50,40,BLUE,'РУКИ',14,27,233,'','окно для отображение рук',WHITE),
    Object(700,230,50,40,BLUE,'4',17,37,253,'','кол-во рук',WHITE),
    Object(95,230,50,40,RED,'СБРОСЫ',14,97,233,'','окно для отображение рук',WHITE),
    Object(700,230,50,40,BLUE,'4',17,117,253,'','кол-во сбросов',WHITE),
    Object(15,280,50,30,BLACK,'4$',20,32,290,'','деньги',YELLOW),
    Object(95,275,50,40,GREEN,'Анте',16,110,280,'','анте',YELLOW),
    Object(85,275,1,1,GREEN,f'{ante}/8',23,112,295,'','номер анте',BLACK),
    Object(70,180,5,5,BLACK_GREEN,'X',30,70,180,'','X',WHITE),
    Object(15,177,50,25,BLUE,'1000',14,18,185,'','кол-во фишек',WHITE),
    Object(90,177,50,25,RED,'1000',14,98,185,'','множетель',WHITE),
    Object(40,140,100,20,BLACK_GREEN,'карта',20,45,140,'','Рука сыгранная',WHITE),
    Object(10,10, 140,55,BLACK_RED,'Маленький блайнд',17,13,19,'','блайнд',WHITE),
    Object(800,10, 1,1,BLACK,'',17,13,39,'','сыгранные очки',WHITE),
    Sprite(600,370,70,100,'assets//coloda.png','колода',''),
    Sprite(610,370,70,100,'assets//coloda.png','колода',''),
    Sprite(620,370,70,100,'assets//coloda.png','колода',''),
    Sprite(120,10,30,30,'assets//Casino_Chip.png','фишка около блайнда',''),
    Object(155,10,400,100,BLACK_WHITE,'0/5',20,160,117,'','джокеры',WHITE)
]
    
    
    

    #  меню
menu_interface =[
Sprite(200,50,280,190,'assets//menulogo.png','название игры в меню',''),   
Sprite(310,200,50,80,'assets//cardlogo.png','карта меню',''),   
Object(230,440,90,50,RED,'PLAY',23,255,460,'start_game','ИГРАТЬ',WHITE)    
    
    
]
    # во время паузы
pause_interface = [
Object(200,170,300,250,ORANGE,'',1,0,0,'','Фон паузы',WHITE),
Object(215,335,270,60,BLACK,'',23,287,355,'','Выход из паузы фон',BLACK),
Object(220,340,260,50,RED,'ПРОДОЛЖИТЬ',23,287,355,'unpause','Выход из паузы',BLACK),
Object(215,265,270,60,BLACK,'',23,287,355,'','открытие меню фон',BLACK),
Object(220,270,260,50,RED,'МЕНЮ',27,317,285,'menu','открытие меню',BLACK),
Object(215,195,270,60,BLACK,'',23,287,355,'','настройки фон',BLACK),
Object(220,200,260,50,RED,'НАСТРОЙКИ',27,293,215,'setting','настройки',BLACK)
]
    # настройки
setting_interface = [
Object(50,50,400,400,ORANGE,'',1,0,0,'','фон настройки',WHITE),
Object(60,70,40,40,ORANGE,'<',55,73,72,'back','кнопка назад',WHITE)   
    
    
]

# джокеры
    # все доступные джокеры
all_jokers = [
Joker(0,0,55,75,'common','+','множитель',4,'assets//basic_joker.png',4,'','Джокер','','',1),
Joker(0,0,55,75,'rare','+','фишки',0,'assets//chips_joker.png',8,'','игра фишек', '+2 за сыгранную карту','+1 за сброшенную карту',1),
Joker(0,0,55,75,'common','+','фишки',0,'assets//cardchips_joker.png',4,'','инвертор карт','+2 за каждую карту','в колоде',1),
Joker(0,0,55,75,'uncommon','x','множитель',3,'assets//invert_joker.png',8,'','перевернутый','x3, -0,2 за каждый ост','авшийся сброс и руку',2),
Joker(0,0,55,75,'common','+','множитель',0,'assets//random_joker.png',6,'','случайный','случайности не','случайны',1)
]
    # интвентарь с джокерами
invent_jokers =[
  
    
]
    # джокеры в магазине
shop_jokers = [
    
]
# интерфейс в магазине
shop_interface = [
    Object(10,70,140,250,BLACK_GREEN,'Инфо',25,50,90,'','Инфо',WHITE),
    Object(15,230,50,40,BLUE,'РУКИ',14,27,233,'','окно для отображение рук',WHITE),
    Object(700,230,50,40,BLUE,'4',17,37,253,'','кол-во рук',WHITE),
    Object(95,230,50,40,RED,'СБРОСЫ',14,97,233,'','окно для отображение рук',WHITE),
    Object(700,230,50,40,BLUE,'4',17,117,253,'','кол-во сбросов',WHITE),
    Object(15,280,50,30,BLACK,'4$',20,32,290,'','деньги',YELLOW),
    Object(95,275,50,40,GREEN,'Анте',16,110,280,'','анте',YELLOW),
    Object(85,275,1,1,GREEN,f'{ante}/8',23,112,295,'','номер анте',BLACK),
    Object(70,180,5,5,BLACK_GREEN,'X',30,70,180,'','X',WHITE),
    Object(15,177,50,25,BLUE,'0',14,18,185,'','кол-во фишек',WHITE),
    Object(90,177,50,25,RED,'0',14,98,185,'','множетель',WHITE),
    Object(40,140,100,20,BLACK_GREEN,'',20,45,140,'','Рука сыгранная',WHITE),
    Object(170,480,500,550,BROWN,'SHOP',50,370,190,'','магазин',WHITE),
    Object(175,300,90,30,RED,'Переброс',16,180,307,'reroll','переброс',WHITE),
    Object(175,340,90,30,GREEN,'Продолжить',16,180,347,'resume','продолжить',WHITE),
    Object(155,10,400,100,BLACK_WHITE,'0/5',20,160,117,'','джокеры',WHITE)
    
    
    
]
# Создание колоды
def create():
    coloda_crea = []
    id_card = 0
    for mast in masts:
        for num, point, sor in zip(Cards_var, Cards_point, Card_sort):
            id_card += 1
            if mast == 'red':
                color_x = RED
                img_x = img_redmast
            elif mast == 'black':
                img_x = img_blackmast
                color_x = BLACK
            elif mast == 'orange':
                img_x = img_orangemast
                color_x = ORANGE
            elif mast == 'green':
                img_x = img_greenmast
                color_x = GREEN
            coloda_crea.append(Card(0, 360, 55, 90, mast, num, point, color_x, img_x, id_card, sor))
    return coloda_crea
    

# генерация колоды для руки
def create_game_coloda(num):
    for _ in range(num):
        if len(coloda):
            card = random.choice(coloda)
            coloda.remove(card)
            
            #
            card.rect.x = 0  
            card.rect.y = 360
            card.base_y = 360
            card.target_y = 360
            
            # Явный сброс rect_inv и rect_img
            card.rect_inv.x = card.rect.x
            card.rect_inv.y = card.rect.y
            card.rectimg.x = card.rect.x + 15
            card.rectimg.y = card.rect.y + 20
            
            game_coloda.append(card)




#  определение покерной комбинации
def determine_poker_combination(cards):
    sorted_cards = sorted(cards, key=lambda x: Card_sort[Cards_var.index(x.num)], reverse=True)
    
    mast_count = {}
    value_count = {}
    for card in sorted_cards:
        mast_count[card.mast] = mast_count.get(card.mast, 0) + 1
        value_count[card.num] = value_count.get(card.num, 0) + 1
        
    is_flush = any(count >= 5 for count in mast_count.values())
    
    unique_values = sorted(set(Card_sort[Cards_var.index(card.num)] for card in sorted_cards), reverse=True)
    is_straight = False
    for i in range(len(unique_values) - 4):
        if unique_values[i] - unique_values[i + 4] == 4:
            is_straight = True
            break
    
    if not is_straight and 14 in unique_values:
        low_straight = [2, 3, 4, 5, 14]
        if all(v in unique_values for v in low_straight[:-1]):
            is_straight = True
            straight_cards = [c for c in sorted_cards 
                            if Card_sort[Cards_var.index(c.num)] in low_straight]
            
            straight_cards = sorted(straight_cards, 
                                  key=lambda x: Card_sort[Cards_var.index(x.num)] if x.num != 'A' else 1)
    if is_flush and is_straight:
        if unique_values[0] == 14:
            return "Роял-флэш", 120, 10, sorted_cards[:5]
        else:
            return "Стрит-флэш", 100, 8, sorted_cards[:5]
    
    if any(count == 4 for count in value_count.values()):
        return "Каре", 60, 7, [card for card in sorted_cards if value_count[card.num] == 4]
    
    if any(count == 3 for count in value_count.values()) and any(count == 2 for count in value_count.values()):
        return "Фулл-хаус", 40, 4, [card for card in sorted_cards if value_count[card.num] in [2, 3]]
    
    if is_flush:
        return "Флэш", 35, 4, [card for card in sorted_cards if mast_count[card.mast] >= 5]
    
    if is_straight:
        return "Стрит", 30, 4, sorted_cards[:5]
    
    if any(count == 3 for count in value_count.values()):
        return "Сет", 30, 3, [card for card in sorted_cards if value_count[card.num] == 3]
    
    if list(value_count.values()).count(2) >= 2:
        return "Две пары", 20, 2, [card for card in sorted_cards if value_count[card.num] == 2]
    
    if any(count == 2 for count in value_count.values()):
        return "Пара", 10, 2, [card for card in sorted_cards if value_count[card.num] == 2]
    
    return "Старшая карта", 5, 1, [sorted_cards[0]]


    
def poker_combin(spisok,spisok_2):
    global combination,chips,multy,combo_cards
    selected_cards = []
    
    for card_ in spisok:
        for card in spisok_2:
            if card.rect == card_:
                selected_cards.append(card)
                break
    if len(selected_cards) >=1:
                combination,chips,multy,combo_cards = determine_poker_combination(selected_cards)
    else :
                combination,chips,multy = '',0,0

 #  обновление магазина
def shop_update():
    global shop_jokers
    shop_jokers = []
    for _ in range(2):  
        template = random.choice(all_jokers)
        new_joker = Joker(
            x=0, y=0,
            w=template.rect.w,
            h=template.rect.h,
            rare=template.rare,
            multy=template.multy,
            add=template.add,
            give_point=template.give_point,
            image=template.image_path,  
            price=template.price,
            ability=template.ability,
            name=template.name,
            info=template.info,
            info2=template.info2,
            sort=template.sort
        )
        shop_jokers.append(new_joker)
        
# Основной цикл игры
g = 61
joker_g = 60
while True:
    
    update_rects = []
    frame_count += 1
    x_mouse, y_mouse = pygame.mouse.get_pos()
    # магазин
    if game_state == 4:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    back_point = game_state
                    game_state = 2
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                        x, y = event.pos 
                        for obj in shop_interface:
                                if obj.rect.collidepoint(x, y):
                                    obj.func() 

                        for joke in invent_jokers:
                            if joke.rect.collidepoint(x, y):
                                
                                if joke.clicked == False:
                                    
                                    joke.clicked = True
                                    
                                elif joke.clicked:
                                    
                                    joke.clicked = False
                                
                                
                            
                            if joke.clicked:
                                for obj in joke.clicked_interface:
                                    if obj.rect.collidepoint(x,y):
                                        if object.function == 'sell':
                                            money += joke.price/2
                                            
                                            invent_jokers.remove(joke)
                            
                        for joke in shop_jokers:
                            if joke.rect.collidepoint(x, y):
                                
                                if joke.clicked == False:
                                    
                                    joke.clicked = True
                                    
                                elif joke.clicked:
                                    
                                    joke.clicked = False
                            
                            if joke.clicked:
                                for obj in joke.clicked_interface:
                                    if obj.rect.collidepoint(x,y):
                                        if object.function == 'buy':
                                            if money >= joke.price and len(invent_jokers) <= 5:
                                                money -= joke.price
                                                joke.clicked = False
                                                invent_jokers.append(joke)
                                                shop_jokers.remove(joke)
                                                
                        
        update_rects.append(screen.fill(GREEN))
        
            
        for object in shop_interface:
            if object.name == 'магазин':
                if shop_timer <= 25:
                    
                    object.rect.y -= 12
                    shop_timer += 1
                    
            if object.name == 'переброс' and frame_count % 10 == 0:
                 object.text = object.font.render(f'переброс {reroll_cost}$', True, object.text_color) 
                    
            object.draw()    
            update_rects.append(object.rect)
        
        for object in shop_interface:
            if object.name == 'кол-во карт' and frame_count % 10 == 0:
                object.text = object.font.render(f'{str(len(coloda))}/{52}', True, object.text_color)
            if object.name == 'кол-во сбросов' and frame_count % 15 == 0:
                object.text = object.font.render(str(delete), True, object.text_color)
            if object.name == 'кол-во рук' and frame_count % 15 == 0:
                object.text = object.font.render(str(hand), True, object.text_color)
            if object.name == 'деньги' and frame_count % 10 == 0:
                object.text = object.font.render(f'{int(money)}$', True, object.text_color)
            if object.name == 'Рука сыгранная' and  frame_count % 5 == 0:
                
                
                object.text = object.font.render(f'{combination}', True, object.text_color)
                
                    
                    
        
                
            if object.name == 'множетель' and frame_count % 5 == 0:
                
                
                object.text = object.font.render(f'{multy}', True, object.text_color)
                
            if object.name == 'номер анте' and frame_count % 44 == 0:
                
                object.text = object.font.render(f'{ante}/8', True, object.text_color)
                       
            
            if object.name == 'кол-во фишек' and frame_count % 5 == 0:
                
                
                object.text = object.font.render(f'{chips}', True, object.text_color)
                
            if object.name == 'сыгранные очки' and frame_count % 30 == 0:
                
                object.text = object.font.render(f'{played_chips}/{ante_points[ante]*blind_multy}',True,object.text_color)    
        joker_c = 1       
        for joker in shop_jokers:
            joker.rect.x,joker.rect.y = g*(joker_c+4) - 20,300
            if not joker.clicked and frame_count % 3 == 0:
                    for object in joker.joker_interface :
                        if object.name == 'фон инфо':
                            object.text = object.font.render(f'{joker.multy}{joker.give_point} {joker.add}',True,object.text_color)
                            object.rect.x, object.rect.y, object.x_text, object.y_text = joker.rect.x + 50, joker.rect.y, joker.rect.x + 65, joker.rect.y + 60
                        if object.name == 'название':
                                
                                object.rect.x, object.rect.y, object.x_text, object.y_text = joker.rect.x + 50, joker.rect.y, joker.rect.x + 65, joker.rect.y + 10
                        if object.name == 'инфо':
                            object.rect.x, object.rect.y, object.x_text, object.y_text = joker.rect.x + 50, joker.rect.y, joker.rect.x + 55, joker.rect.y + 25
                        if object.name == 'инфо2':
                            object.rect.x, object.rect.y, object.x_text, object.y_text = joker.rect.x + 50, joker.rect.y, joker.rect.x + 55, joker.rect.y + 35
                
            elif joker.clicked:
                    
                    for object in joker.clicked_interface:
                        if object.name == 'кнопка':
                            object.color = GREEN
                            object.text = object.font.render(f'купить за {int(joker.price)}$',True,object.text_color)
                            object.function = 'buy'
                            object.rect.x, object.rect.y, object.x_text, object.y_text = joker.rect.x, joker.rect.y + 80, joker.rect.x , joker.rect.y + 85
                            
                 
                    
            if joker.name == 'инвертор карт' and frame_count % 40 == 0 :
                    joker.give_point = len(coloda)* 2
                        
            if joker.name == 'перевернутый' and frame_count % 50 == 0:
                    joker.give_point = round(3 - 0.2*(hand + delete),1)   
                        
            if joker.name == 'случайный' :
                    if played != 1:
                        joker_time += 1
                        if joker_time % 10 == 0:
                                joker.give_point = random.randint(1,23)
            
            joker.choise()                
            joker.draw()
            update_rects.append(joker.rect)
            joker_c += 1
            
        for joker in shop_jokers:
                joker.draw_inter()      
                                
        joker_c = 1    
        if len(invent_jokers) >= 1:
            for joker in invent_jokers:
                joker.rect.x,joker.rect.y = g*(joker_c+2) - 20,20
                if not joker.clicked and frame_count % 3 == 0:
                    for object in joker.joker_interface :
                        if object.name == 'фон инфо':
                            object.text = object.font.render(f'{joker.multy}{joker.give_point} {joker.add}',True,object.text_color)
                            object.rect.x, object.rect.y, object.x_text, object.y_text = joker.rect.x + 50, joker.rect.y, joker.rect.x + 65, joker.rect.y + 60
                        if object.name == 'название':
                                
                                object.rect.x, object.rect.y, object.x_text, object.y_text = joker.rect.x + 50, joker.rect.y, joker.rect.x + 65, joker.rect.y + 10
                        if object.name == 'инфо':
                            object.rect.x, object.rect.y, object.x_text, object.y_text = joker.rect.x + 50, joker.rect.y, joker.rect.x + 55, joker.rect.y + 25
                        if object.name == 'инфо2':
                            object.rect.x, object.rect.y, object.x_text, object.y_text = joker.rect.x + 50, joker.rect.y, joker.rect.x + 55, joker.rect.y + 35
                
                elif joker.clicked:
                    for object in joker.clicked_interface:
                        if object.name == 'кнопка':
                            object.color = RED
                            object.text = object.font.render(f'продать за {int(joker.price/2)}$',True,object.text_color)
                            object.function = 'sell'
                            object.rect.x, object.rect.y, object.x_text, object.y_text = joker.rect.x, joker.rect.y + 80, joker.rect.x , joker.rect.y + 85
                            
                 
                    
                if joker.name == 'инвертор карт' and frame_count % 40 == 0 :
                    joker.give_point = len(coloda)* 2
                
                if joker.name == 'перевернутый' and frame_count % 50 == 0:
                    joker.give_point = round(3 - 0.2*(hand + delete),1)   
                
                if joker.name == 'случайный' :
                    if played != 1:
                        joker_time += 1
                        if joker_time % 10 == 0:
                            joker.give_point = random.randint(1,23)
                        
                        
                
                joker.choise()
                joker.draw()
                update_rects.append(joker.rect)
                joker_c += 1
                
            
                    
            for joker in invent_jokers:
                joker.draw_inter()    
            
            
            
            
    # настройки
    if game_state == 3:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                        x, y = event.pos 
                        for obj in setting_interface:
                                if obj.rect.collidepoint(x, y):
                                    obj.func() 
                                    
                                       
        for object in setting_interface:
            object.draw()    
            update_rects.append(object.rect)
    
    # пауза
    if game_state == 2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = back_point
                    
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                
                for obj in pause_interface:
                   
                    if obj.rect.collidepoint(x, y):
                        
                        obj.func()
                        

        
        
        for object in pause_interface:
            object.draw()
            update_rects.append(object.rect)
                                
    # меню
    if game_state == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                    x, y = event.pos 
                    for obj in menu_interface:
                            if obj.rect.collidepoint(x, y):
                                obj.func()
                                
                                
                        
        update_rects.append(screen.fill(BLACK_BLUE))
        
        for object in menu_interface:
            object.draw()
            update_rects.append(object.rect)
        
    
    
    
    
    
    
    # игра
    if game_state == 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    back_point = game_state
                    game_state = 2
            # проверка на нажатие 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    # проверка на нажатие карты
                    for card in game_coloda:
                        if card.rect_inv.collidepoint(x, y):
                            if card not in clicked:  
                                clicked.append(card)
                            else:
                                clicked.remove(card)
                    # проверка на нажатий кнопок интерфейса
                    for obj in interface:
                        if obj.rect.collidepoint(x, y):
                            obj.func()
                            # меняет текст кнопки сортировки
                            if obj.function == 'sort':
                                if sort_choise == 1:
                                    obj.text = obj.font.render(f'масти', True, WHITE)
                                elif sort_choise == 0:
                                    obj.text = obj.font.render(f'значимости', True, WHITE)
                    
                    
                    for joke in invent_jokers:
                        if joke.rect.collidepoint(x, y):
                            
                            if joke.clicked == False:
                                
                                joke.clicked = True
                                
                            elif joke.clicked:
                                
                                joke.clicked = False
                            
                            
                        
                        if joke.clicked:
                            for obj in joke.clicked_interface:
                                if obj.rect.collidepoint(x,y):
                                    if object.function == 'sell':
                                        money += joke.price/2
                                        invent_jokers.remove(joke)

        
        if start:
            played_chips = 0
            hand = 4 # рука
            hand_play = 0
            delete = 4 # сбросы
            delete_play = 0
            money = 4
            blind = 1
            coloda_copy = create()
            coloda = coloda_copy.copy()
            
            create_game_coloda(8- len(game_coloda))
            game_coloda.sort(key=lambda card: card.sort, reverse=True)
            f = - 600
            start = False
            
            
        
        
        
        
        if played != 1:
            
            poker_combin(clicked,game_coloda)
        
        # отрисовка интерфейса
       
        update_rects.append(screen.fill(BACKGROUND))
        
                    
        
        
        
        for object in interface:
            if object.name == 'кол-во карт' and frame_count % 10 == 0:
                object.text = object.font.render(f'{str(len(coloda))}/{52}', True, object.text_color)
            if object.name == 'кол-во сбросов' and frame_count % 15 == 0:
                object.text = object.font.render(str(delete), True, object.text_color)
            if object.name == 'кол-во рук' and frame_count % 15 == 0:
                object.text = object.font.render(str(hand), True, object.text_color)
            if object.name == 'деньги' and frame_count % 10 == 0:
                object.text = object.font.render(f'{int(money)}$', True, object.text_color)
            if object.name == 'Рука сыгранная' and  frame_count % 5 == 0:
                
                
                object.text = object.font.render(f'{combination}', True, object.text_color)
                
            if object.name == 'джокеры':
                object.text = object.font.render(f'{len(invent_jokers)}/5', True, object.text_color)            
                    
        
                
            if object.name == 'множетель' and frame_count % 5 == 0:
                
                
                object.text = object.font.render(f'{multy}', True, object.text_color)
                
            if object.name == 'номер анте' and frame_count % 44 == 0:
                
                object.text = object.font.render(f'{ante}/8', True, object.text_color)
                       
            
            if object.name == 'кол-во фишек' and frame_count % 5 == 0:
                
                
                object.text = object.font.render(f'{chips}', True, object.text_color)
                
            if object.name == 'сыгранные очки' and frame_count % 30 == 0:
                
                object.text = object.font.render(f'{played_chips}/{ante_points[ante]*blind_multy}',True,object.text_color)  
            
            if object.name == 'блайнд' and frame_count % 34 == 0:
                if blind == 1:
                    object.text = object.font.render(f'Малый блайнд',True,object.text_color)
                
                elif blind == 2:
                    object.text = object.font.render(f'средний блайнд',True,object.text_color)
                    
                elif blind == 3:
                    object.text = object.font.render(f'Большой блайнд',True,object.text_color)
                                    
                
            object.draw()
            update_rects.append(object.rect)
            
            
            
            
            
        if f <= 10:
          f += 25 
        else:
            f = 15
        c = 1
        # отрисовка колоды 
        for card in game_coloda:
            card.rect.x = (g * c) - f
            card.rectimg.x = (g * c) - f + 15
            card.rect_inv.x = (g * c) - f
            card.draw()
            update_rects.append(card.rect)
            card.choise()
            c += 1
        l = 1
        
        joker_c = 1
        if len(invent_jokers) >= 1:
            for joker in invent_jokers:
                joker.rect.x,joker.rect.y = g*(joker_c+2) - 20,20
                if not joker.clicked and frame_count % 3 == 0:
                    for object in joker.joker_interface :
                        if object.name == 'фон инфо':
                            object.text = object.font.render(f'{joker.multy}{joker.give_point} {joker.add}',True,object.text_color)
                            object.rect.x, object.rect.y, object.x_text, object.y_text = joker.rect.x + 50, joker.rect.y, joker.rect.x + 65, joker.rect.y + 60
                        if object.name == 'название':
                                
                                object.rect.x, object.rect.y, object.x_text, object.y_text = joker.rect.x + 50, joker.rect.y, joker.rect.x + 65, joker.rect.y + 10
                        if object.name == 'инфо':
                            object.rect.x, object.rect.y, object.x_text, object.y_text = joker.rect.x + 50, joker.rect.y, joker.rect.x + 55, joker.rect.y + 25
                        if object.name == 'инфо2':
                            object.rect.x, object.rect.y, object.x_text, object.y_text = joker.rect.x + 50, joker.rect.y, joker.rect.x + 55, joker.rect.y + 35
                
                elif joker.clicked: 
                    for object in joker.clicked_interface:
                        if object.name == 'кнопка':
                            object.color = RED
                            object.text = object.font.render(f'продать за {int(joker.price/2)}$',True,object.text_color)
                            object.function = 'sell'
                            object.rect.x, object.rect.y, object.x_text, object.y_text = joker.rect.x, joker.rect.y + 80, joker.rect.x , joker.rect.y + 85
                            
                 
                    
                if joker.name == 'инвертор карт' and frame_count % 40 == 0 :
                    joker.give_point = len(coloda)* 2
                
                if joker.name == 'перевернутый' and frame_count % 50 == 0:
                    joker.give_point = round(3 - 0.2*(hand + delete),1)   
                
                if joker.name == 'случайный' :
                    if played != 1:
                        joker_time += 1
                        if joker_time % 10 == 0:
                            joker.give_point = random.randint(1,23)
                        
                        
                
                joker.choise()
                joker.draw()
                update_rects.append(joker.rect)
                joker_c += 1
                
            
                    
            for joker in invent_jokers:
                joker.draw_inter()
                    
            
        if played == 1:
            l = 1  
            for card in played_cards:
                # Обновляем координаты карты
                played_card_check = 0
                card.rect.x = g * l + r
                card.rectimg.x = g * l + r + 15
                card.rect_inv.x = g * l + r
                
                # Отрисовываем карту
                card.draw()
                card.move()
                
                if card.rect.y <= 200: 
                    card.play()
                    combination, chips, multy, combo_cards = determine_poker_combination(played_cards)
                    chips += sum(int(card.point) for card in combo_cards)
                    if len(invent_jokers) >= 1:
                        invent_jokers.sort(key=lambda joker: joker.sort)
                        for joker in invent_jokers:
                            
                            if joker.add == 'фишки':
                                if joker.multy == '+':
                                    chips += joker.give_point 
                                elif joker.multy == 'x':
                                    chips*= joker.give_point    
                            elif joker.add == 'множитель':
                                if joker.multy == '+':
                                     multy += joker.give_point 
                                elif joker.multy == 'x':
                                    multy*= joker.give_point
                                    
                    if chips % 0.5 != 0:
                        chips = round(chips)
                    if multy % 0.5 != 0:
                        multy = round(chips)             
                    timer += 1
                    
                if timer >= 200:
                    for card in played_cards:
                        card.play_control = 0
                    r += 6.7    
                if card.rect.x >= 570:
                    played = 0
                    played_chips += chips * multy
                    played_cards = []
                    create_game_coloda(8 - len(game_coloda))
                    if played_chips <= ante_points[ante]*blind_multy and hand <= 0:
                        coloda.clear()  
                        coloda_copy.clear() 
                        game_coloda.clear()  
                        clicked.clear()  
                        played_cards.clear() 
                        played = 0 
                        game_state = 0
                        blind = 0
                        blind_multy = 1
                
                        
                    
                    
                
                l += 1 
        
        if played_chips >= ante_points[ante]*blind_multy:
                end_timer += 1.5 
                
                played_cards.clear()
                if end_timer >= 120:
                    end_timer = 0
                    blind += 1
                    if blind == 2:
                        blind_multy = 1.5
                        money += 3
                    if blind == 3:
                        blind_multy = 2
                        money += 4
                    
                    if blind == 4:
                        money += 5
                        ante += 1
                        blind = 1
                        blind_multy = 1
                    for object in shop_interface:
                        if object.name == 'магазин':
                            
                                
                            object.rect.y = 480
                    played = 0         
                    shop_update()
                    coloda = coloda_copy.copy()
                    clicked = []
                    reroll_cost = 4
                    money += hand  
                    shop_timer = 0
                    game_state = 4
                    played_chips = 0        
        
        # сортировка карт
        if sort_choise == 1:
            game_coloda.sort(key=lambda card: (mast_order[card.mast], -int(card.point)))
        elif sort_choise == 0:
            game_coloda.sort(key=lambda card: card.sort, reverse=True)
        
        
    if Back:
        back_frame += 1
    if Back == True and back_frame >=1:
        game_state = back_point
        back_frame = 0    
        Back = False
      
    
    pygame.display.update(update_rects)
        
    clock.tick(FPS)