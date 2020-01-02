import pygame,sys

# [piano simulator]
# version: 2.0
# author: Candice Zhang
# date: 2016.12.18

def read_music_file(filename, sep):
    try:
        with open(filename,'r') as f:
            lines = f.readlines()
    except:
        return []
    data = []
    for line in lines:
        lineData = line.strip().split(sep)
    if lineData != '':
        data.append(lineData)
    music_data_list = []
    for i in range(len(data)//2):
        music_data_list.append((data[i*2],eval(data[i*2+1])))
    return music_data_list

def play_note(pitch, length):
    global sound_list
    length_32 = 80 # length of a 32nd note, in milliseconds
    n0 = pitch[0]
    if n0 == 'c' or n0 == 'C':
        k2 = 0
    elif n0 == 'd' or n0 == 'D':
        k2 = 2
    elif n0 == 'e' or n0 == 'E':
        k2 = 4
    elif n0 == 'f' or n0 == 'F':
        k2 = 5
    elif n0 == 'g' or n0 == 'G':
        k2 = 7
    elif n0 == 'a' or n0 == 'A':
        k2 = 9
    elif n0 == 'b' or n0 == 'B':
        k2 = 11
    else:
        return False
    if pitch[1] == '#':
        k2 += 1
    elif pitch[1] == 'b':
        k2 -= 1
    if ord('1') <= ord(pitch[-1]) <= ord('7'):
        k1 = eval(pitch[-1]) - 1
        sound_list[k1*12+k2].play()
        if length == 0:
            pygame.time.wait(1 )
        else:
            pygame.time.wait(length_32 * length )
        return True
    else:
        return False

def play_melody(melody_list):
    t0 = pygame.time.get_ticks()
    for m in melody_list:
        #print(m)
        while True:
            if pygame.time.get_ticks() - t0 >= m[1]:
                play_note(m[0],0)
                break
            pygame.time.wait(1)
        

def draw(screen, pic, x0, y0, size ):
    color = [ (255,255,255),(0,0,0),(255,0,0),(0,255,0),(0,0,255),(128,64,0)]
    for y in range(len(pic)):
        s = pic[y]
        for x in range(len(s)):
            try:
                c = color[eval(s[x])]
                pygame.draw.rect(screen, c, \
                    (x*size+x0,y*size+y0,size,size), 0)
            except:
                pass
    

pianoKey = pygame.image.load('keyboard.bmp')
SCREENSIZE =(pianoKey.get_width(), pianoKey.get_height())

pygame.init()
screen = pygame.display.set_mode(SCREENSIZE)
pygame.display.set_caption("piano")
clock = pygame.time.Clock()
font = pygame.font.Font(None,32)

screen.blit(pianoKey,(0,0))
     
key_list = (('1','C4'),('2','D4'),('3','E4'),('4','F4'),('5','G4'),('6','A4'),('7','B4'),\
            ('q','C5'),('w','D5'),('e','E5'),('r','F5'),('t','G5'),('y','A5'),('u','B5'),\
            ('a','C6'),('s','D6'),('d','E6'),('f','F6'),('g','G6'),('h','A6'),('j','B6'))
key_size = 2

sound_list = []
for k_level in range(7):
    for k_name in ['c','cm','d','dm','e','f','fm','g','gm','a','am','b']:
        if len(k_name)==2:
            s = k_name[0] + str(k_level+1) + k_name[1]
        else:
            s = k_name + str(k_level+1)
        s += '.ogg'
        ogg = pygame.mixer.Sound("notes/"+s)
        sound_list.append(ogg)

picKey = []
picKey.append('000010')
picKey.append('000010')
picKey.append('0000110')
picKey.append('00001010')
picKey.append('000010')
picKey.append('000010')
picKey.append('000010')
picKey.append('001110')
picKey.append('011110')
picKey.append('011110')
picKey.append('011110')
picKey.append('001100')

rec_status = 0
t0 = 0


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if rec_status == 0:
                    rec_status = 1
                    rec_t0 = pygame.time.get_ticks()
                    t0 = rec_t0
                    rec_n = 0
                    melody_list = []
                else:
                    rec_status = 0
                    pygame.draw.circle(screen,(255,255,255),(10,10),5,0)
            elif event.key == pygame.K_RETURN:
                play_melody(melody_list)
            for i in range(len(key_list)):
                k = key_list[i]
                if k[0] == chr(event.key):
                    play_note(k[1],0)
                    screen.blit(pianoKey,(0,0))
                    draw(screen, picKey, i * 30 + 6, 90, key_size )
                    if rec_status == 1:
                        melody_list.append((k[1],pygame.time.get_ticks() - rec_t0))
    if rec_status == 1:
        if pygame.time.get_ticks() - t0 > 200:
            rec_n += 1
            t0 = pygame.time.get_ticks()
        if rec_n % 2 == 0:
            pygame.draw.circle(screen,(255,0,0),(10,10),5,0)
        else:
            pygame.draw.circle(screen,(255,255,255),(10,10),5,0)

    pygame.display.update()

