from tkinter import Y
import pygame
import random
import sqlite3
pygame.init()
pygame.mixer.init()

connect=sqlite3.connect('records.db')
cursor = connect.cursor()
# cursor.execute('''
#     Create Table runs(
#         points INT,
#         jump INT,
#         speed INT,
#         runner_name TEXT
#     )
# ''')


# cursor.execute('''Insert Into runs(points, jump, speed,runner_name) Values(0,0,0,'starter')''')
#cursor.execute('''Insert Into runs(points, jump, speed,runner_name) Values(6,7,8,'example one')''')
#cursor.execute('''Insert Into runs(points, jump, speed,runner_name) Values(20,30,40,'12345678901234567890')''')
#cursor.execute('''Drop Table runs''')
cursor.execute('''Select * from runs ORDER BY points DESC''')
connect.commit()
ftchall=cursor.fetchall()
print(ftchall)

window_1 = pygame.display.set_mode((700,700))
bg = (250,250,250)   
jump_sound = pygame.mixer.Sound("sounds/jump.ogg")
mountain_theme = pygame.mixer.music.load('sounds/sky theme.ogg')
hit_sound = pygame.mixer.Sound("sounds/hitted.ogg")
power_up=pygame.mixer.Sound('sounds/p-up.ogg')
pygame.mixer.music.play(-1)
sounds = [jump_sound,hit_sound,power_up]
bg_music = [mountain_theme]
volume = 1
clock =  pygame.time.Clock()
fall_speed = 5
jump_speed = 10
jump_time = 0
max_jump_time = 25
everything = []
all_platforms = []
platform_now = []
healthes = []
game = True
jump = False
fall = False
move_right = False
move_left = False
on_platform = True
animate_walk = 1
animate_round = 1
turned_right = True
win = True
hitted = False
hit_cooldown = None
walk_right_1 = pygame.image.load('images/walk animation right.png')
walk_right_2 = pygame.image.load('images/walk animation right 2.png')
walk_right_3 = pygame.image.load('images/walk animation right 3.png')
walk_left_1 = pygame.transform.flip(walk_right_1,True,False)
walk_left_2 = pygame.transform.flip(walk_right_2,True,False)
walk_left_3 = pygame.transform.flip(walk_right_3,True,False)
stand_left = pygame.transform.flip(pygame.image.load('images/stand animation right.png'),True,False)
jump_left = pygame.transform.flip(pygame.image.load('images/jump animation.png'),True,False)
fall_left =pygame.transform.flip(pygame.image.load('images/fall animation.png'),True,False)
direction_right = True

class Player():
    def __init__(self,move_speed):
        self.rect = pygame.Rect(326,536,48,64)
        self.image = pygame.image.load('images/stand animation right.png')
        self.move_speed = move_speed
        
    def draw(self):
        window_1.blit(self.image,(self.rect.x,self.rect.y))
class Platform():
    def __init__(self,x=250,y=700):
        self.rect = pygame.Rect(x,y,200,50)
        self.image = pygame.image.load('images/platform.png')
        everything.append(self)
        all_platforms.append(self)
        self.buff = None
        self.new_platforms_list = []
    def draw(self):
        window_1.blit(self.image,(self.rect.x,self.rect.y))
class Item():
    def __init__(self,ground,img,buff):
        self.rect = pygame.Rect(ground.rect.x+75,ground.rect.y-50,50,50)
        self.image = pygame.image.load(img)
        self.ground = ground
        everything.append(self)
        self.buff = buff
        self.new_platforms_list = []
        self.speed = 2
        for a in range(100):
            self.new_platforms_list.append(a)
    def draw(self):
        window_1.blit(self.image,(self.rect.x,self.rect.y))     
class HealthBar():
    def __init__(self):
        self.rect = pygame.Rect(0,0,300,100)
        self.image = pygame.image.load('images/healthbar.png')
        self.hp = 10
    def draw(self):
        start_x = 50
        start_y = 25
        for health in range(1,self.hp):
            new_health = pygame.Rect(start_x,start_y,25,50)
            pygame.draw.rect(window_1,(250,150,150),new_health)
            start_x+=30
        window_1.blit(self.image,(self.rect.x,self.rect.y))
class PointBar():
    def __init__(self,point):
        self.rect = pygame.Rect(470,12,195,60)
        self.image = pygame.image.load('images/pointbar.png')
        self.font = pygame.font.SysFont('Tsiox', 70)
        self.point = point
        self.text = self.font.render('очки '+str(self.point), True, (250,150,150))
    def draw(self):
        window_1.blit(self.image,(self.rect.x,self.rect.y))
        window_1.blit(self.text,(self.rect.x+5,self.rect.y+5))
        
class Button():
    def __init__(self,x,y,wid,hei,image,here=None):
        self.rect = pygame.Rect(x,y,wid,hei)
        if here!=None:
            self.image = pygame.image.load(image)
        if here:
            self.image = image
        
    def draw(self):
        window_1.blit(self.image,(self.rect.x,self.rect.y))

class SoundBar():
    def __init__(self,vol_y):
        vol_x=200
        self.volumes=[]
        self.vol_rect_cols=[]
        for j in range(10):
            volume_rect = pygame.Rect(vol_x,vol_y,25,50)
            self.volumes.append(volume_rect)
            vol_rect_col = (255,128,170)
            self.vol_rect_cols.append(vol_rect_col)
            vol_x+=30
    def draw(self):
        for g in self.volumes:
            pygame.draw.rect(window_1,self.vol_rect_cols[self.volumes.index(g)],g)

base_platform = Platform()
base_platform.image = pygame.image.load('images/platform 2.png')
base_platform_2 = Platform(500,580)
first_jump_boost = Item(base_platform_2,'images/jump_boost.png','jump')
base_platform_3 = Platform(y=450)
base_platform_3.image = pygame.image.load('images/platform 3.png')
base_platform_4 = Platform(100,300)
base_platform_4.image = pygame.image.load('images/platform 2.png')
base_platform_5 = Platform(300,200)
base_platform_6 = Platform(y=75)
player = Player(3)
health = HealthBar()
game_sounds = SoundBar(410)
music=SoundBar(570)
points = PointBar(len(all_platforms))
# losing = pygame.Rect(200,300,300,100)

def stats():
    opened = True
    stats_y= 220
    while opened:
        window_1.blit(pygame.image.load('images/rate.png'),(100,100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
                cursor.close()
                connect.close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    opened = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    stats_y+=10
                if event.button == 5:
                    stats_y-=10

        stats_y_copy = stats_y

        if stats_y_copy >= 180 and stats_y_copy <=500:

            window_1.blit(pygame.font.SysFont('', 25).render('нікнейм', True, (250,140,120)),(130,stats_y_copy-60))
            window_1.blit(pygame.font.SysFont('', 25).render('очки', True, (250,140,120)),(290,stats_y_copy-60))
            window_1.blit(pygame.font.SysFont('', 25).render('прижок', True, (250,140,120)),(380,stats_y_copy-60))
            window_1.blit(pygame.font.SysFont('', 25).render('швидкість', True, (250,140,120)),(470,stats_y_copy-60))

        for run in ftchall:
            if stats_y_copy >=130  and stats_y_copy <=550:
                window_1.blit(pygame.font.SysFont('', 20).render(str(run[3]), True, (250,150,130)),(130,stats_y_copy))
                window_1.blit(pygame.font.SysFont('', 20).render(str(run[0]), True, (250,150,130)),(300,stats_y_copy))
                window_1.blit(pygame.font.SysFont('', 20).render(str(run[1]), True, (250,150,130)),(390,stats_y_copy))
                window_1.blit(pygame.font.SysFont('', 20).render(str(run[2]), True, (250,150,130)),(480,stats_y_copy))
            stats_y_copy+=35

        pygame.display.update()
        clock.tick(60)
        

def lose():
    close = False
    while not close:
        window_1.blit(pygame.image.load('images/end.png'),(200,300))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
                cursor.close()
                connect.close()

        pygame.display.update()
        clock.tick(60)

# def help_info():
#     esc = False
#     while not esc:
#         None

def pause():
    close = False
    # help = Button(100,450,500,100,'help.png')
    # animate_press = 'unpressed'
    while not close:
        window_1.blit(pygame.image.load('images/pause.png'),(200,200))
        window_1.blit(pygame.image.load('images/sounds.png'),(200,305))
        window_1.blit(pygame.image.load('images/music.png'),(200,465))
        game_sounds.draw()
        music.draw()
        # if animate_press!= 'unpressed':
        #     if pygame.time.get_ticks()-animate_press>= 250:
        #         help.image = pygame.image.load('help.png')
        # help.draw()                                                                           

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
                cursor.close()
                connect.close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    close = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                for f in game_sounds.volumes:
                    if f.collidepoint(pygame.mouse.get_pos()):
                        for gi in range(len(game_sounds.vol_rect_cols)):
                            game_sounds.vol_rect_cols[gi]=(66,66,66)
                        game_sounds.vol_rect_cols[game_sounds.volumes.index(f)]=(255,128,170)
                        for fig in game_sounds.vol_rect_cols:
                            if game_sounds.vol_rect_cols.index(fig) <= game_sounds.volumes.index(f):
                                game_sounds.vol_rect_cols[game_sounds.vol_rect_cols.index(fig)] = (255,128,170)

                        sounds_vol=(int(game_sounds.volumes.index(f))+1)*0.1
                        for some_sound in sounds:
                            pygame.mixer.Sound.set_volume(some_sound,sounds_vol)
                        
                        
                for fi in music.volumes:
                    if fi.collidepoint(pygame.mouse.get_pos()):
                        music_vol=(int(music.volumes.index(fi))+1)*0.1
                        pygame.mixer.music.set_volume(music_vol)

                        for ig in range(len(music.vol_rect_cols)):
                            music.vol_rect_cols[ig]=(66,66,66)
                        music.vol_rect_cols[music.volumes.index(fi)]=(255,128,170)
                        for fij in music.vol_rect_cols:
                            if music.vol_rect_cols.index(fij) <= music.volumes.index(fi):
                                music.vol_rect_cols[music.vol_rect_cols.index(fij)] = (255,128,170)
            

        pygame.display.update()
        clock.tick(60)

def main_game(usernick,max_jump_time=max_jump_time,move_right = move_right, move_left=move_left,direction_right=direction_right,jump=jump,jump_time=jump_time,hitted=hitted,animate_walk=animate_walk,animate_round=animate_round):
    jump_boosts = 1
    while win:
        window_1.blit(pygame.image.load('images/background 1.png'),(0,0))                     
        player.draw()
        for obj in everything:
            obj.draw()
        points.draw()
        points.point = len(all_platforms)
        points.text = points.font.render('очки:'+str(points.point-7), True, (0,131,143))
        health.draw()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
                cursor.close()
                connect.close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                        stats()
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    move_right=True
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    move_left=True    
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    if on_platform:
                        jump = True
                        on_platform = False
                        pygame.mixer.Sound.play(jump_sound)
                if event.key == pygame.K_ESCAPE:
                    pause()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    move_right=False
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    move_left=False

        fall = True
        on_platform=False
        platform_now = []
        for platform in everything:
            if platform in all_platforms:
                if platform not in platform_now:
                    platform_now.append(platform)
                for i in range(platform.rect.x-25,platform.rect.x+190):
                    if player.rect.x==i:
                        if player.rect.y==platform.rect.y-64:
                            if not jump:
                                on_platform=True
                                fall=False
                                jump_time = 0
                            
                            
        for anything in everything:
            if anything.rect.y > 800:
                everything.remove(anything)
                
            if anything in all_platforms and anything.rect.y>=600:
                if len(anything.new_platforms_list)<1:
                    new_x=random.randint(0,500)
                    
                    new_y=-50
                    new_platform = Platform(new_x,new_y)
                    sprite = random.randint(1,3)
                    if sprite == 2:
                        new_platform.image = pygame.image.load('images/platform 2.png')
                    elif sprite ==3:
                        new_platform.image = pygame.image.load('images/platform 3.png')
                    anything.new_platforms_list.append(new_platform)
                    for collide in platform_now:
                        while new_platform.rect.colliderect(collide.rect):
                            new_platform.rect.x = random.randint(0,500)
                    # while new_platform.rect.x - (all_platforms[all_platforms.index(new_platform-1)]).rect.x >= 160 or new_platform.rect.x - (all_platforms[all_platforms.index(new_platform-1)]).rect.x >= 160:
                    #     new_platform.rect.x = random.randint(0,500)
                    new_thing_chance = random.randint(0,100)
                    for chance in range(0,10):
                        if new_thing_chance == chance:
                            hp_or_jump = random.randint(1,3)
                            if hp_or_jump==1:
                                new_item = Item(new_platform,'images/hp_fruit.png','hp')
                            elif hp_or_jump==2:
                                new_item = Item(new_platform,'images/jump_boost.png','jump')
                            elif hp_or_jump==3:
                                new_item = Item(new_platform,'images/speed up.png','speed')
                    for chance in range(15,45):
                        if new_thing_chance== chance:
                            enemy= Item(new_platform,'images/spikeball 1.png','hit')

        if on_platform:
            if direction_right:
                player.image = pygame.image.load('images/stand animation right.png')
            elif not direction_right:
                player.image = stand_left

        if move_right:
            player.rect.x+=player.move_speed
            direction_right=True
            if not fall and not jump:
                if animate_walk==1 or animate_walk==2 or animate_walk==3 or animate_walk==4:
                    player.image = walk_right_1
                    animate_walk+=1
                elif animate_walk==5 or animate_walk==6 or animate_walk==7 or animate_walk==8:
                    player.image = walk_right_2
                    animate_walk+=1
                elif animate_walk==9 or animate_walk==10 or animate_walk==11 or animate_walk==12:
                    player.image = walk_right_3
                    animate_walk+=1
                    if animate_walk==13:
                        animate_walk = 1
        if move_left:
            player.rect.x-=player.move_speed
            direction_right=False
            if not fall and not jump:
                if animate_walk==1 or animate_walk==2 or animate_walk==3 or animate_walk==4:
                    player.image = walk_left_1
                    animate_walk+=1
                elif animate_walk==5 or animate_walk==6 or animate_walk==7 or animate_walk==8:
                    player.image = walk_left_2
                    animate_walk+=1
                elif animate_walk==9 or animate_walk==10 or animate_walk==11 or animate_walk==12:
                    player.image = walk_left_3
                    animate_walk+=1
                    if animate_walk==13:
                        animate_walk = 1
        
        
        
        if fall:
            if direction_right:
                player.image = pygame.image.load('images/fall animation.png')
            elif not direction_right:
                player.image = fall_left
            for object in everything:
                object.rect.y-=fall_speed
            
        if jump :
            # max_sounds = pygame.mixer.Sound.get_num_channels(jump_sound)
            # if int(max_sounds)==0:
            #     pygame.mixer.Sound.play(jump_sound)
            #     max_sounds = 1
            if direction_right:
                player.image = pygame.image.load('images/jump animation.png')
            elif not direction_right:
                player.image = jump_left
            jump_time+=1
            for jump_object in everything:
                jump_object.rect.y+=jump_speed
        if jump_time==max_jump_time:
            jump=False
        
        for buff in everything:
            if player.rect.colliderect(buff.rect):
                if buff.buff == 'hp':
                    if health.hp<14:
                        pygame.mixer.Sound.play(power_up)
                        health.hp+=1
                        everything.remove(buff)
                elif buff.buff == 'jump':
                    pygame.mixer.Sound.play(power_up)
                    jump_boosts+=1
                    max_jump_time+=5    
                    everything.remove(buff)
                elif buff.buff == 'speed':
                    pygame.mixer.Sound.play(power_up)
                    player.move_speed+=1
                    everything.remove(buff)
                elif buff.buff == 'hit' and not hitted:
                    health.hp-=1
                    pygame.mixer.Sound.play(hit_sound)
                    hitted = True
                    hit_cooldown= pygame.time.get_ticks()

        for spikeball in everything:
            if spikeball.buff == 'hit':
                if animate_round <= 2:
                    spikeball.image = pygame.image.load('images/spikeball 1.png')
                    animate_round+=1
                elif animate_round <= 4:
                    spikeball.image = pygame.image.load('images/spikeball 2.png')
                    animate_round+=1
                elif animate_round <= 6:
                    spikeball.image = pygame.image.load('images/spikeball 3.png')
                    animate_round+=1
                    if animate_round == 6:
                        animate_round=1
                if spikeball.ground.rect.x - spikeball.rect.x <= -150 or spikeball.ground.rect.x - spikeball.rect.x >= 0:
                    spikeball.speed*=-1
                spikeball.rect.x+=spikeball.speed
                

        now = pygame.time.get_ticks()
        if hitted:
            health.image = pygame.image.load('images/hitted bar.png')
            if now - hit_cooldown > 2000:
                hitted = False
                health.image = pygame.image.load('images/healthbar.png')

        if player.rect.x >= 700:
            player.rect.x = 0
        elif player.rect.x <= -48:
            player.rect.x = 652 
        if everything[-1].rect.y < -1200 or health.hp <= 1:
            cursor.execute('''Insert Into runs(points, jump, speed,runner_name) Values(?,?,?,?)''',(points.point-7,jump_boosts,player.move_speed-2,usernick))
            connect.commit()
            lose()

        pygame.display.update()  
        clock.tick(60)
        window_1.fill(bg)

def start_menu():
    menu=True
    username=''
    while menu:
        window_1.blit(pygame.image.load('images/background 1.png'),(0,0))  
        window_1.blit(pygame.font.SysFont('', 70).render('нікнейм', True, (0,0,0)),(250,250))        
        userx=250
        # nam=''
        # for n in username:
        #     nam+=n
        window_1.blit(pygame.font.SysFont('', 50).render(username, True, (0,0,0)),(250,300))
        enter_rect = pygame.Rect(250,350,200,50)
        pygame.draw.rect(window_1,(0,0,0),enter_rect)
        window_1.blit(pygame.font.SysFont('', 40).render('підтвердити', True, (250,250,250)),(265,360))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if len(username)>=1:
                        username=username.rstrip(username[-1])

                elif len(username)<14:
                    username+=event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if enter_rect.collidepoint(pygame.mouse.get_pos()):
                    main_game(username)
                    print('da')
                

        pygame.display.update() 
        clock.tick(60)
        window_1.fill(bg)
    

start_menu()