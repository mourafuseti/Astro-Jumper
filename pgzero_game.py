"""
Astro Jumper - Jogo de Plataforma com Pygame Zero
Criado por Leonardo de Moura Fuseti
Copyright 2025 - All Rights Reserved
"""
import random
from pygame import Rect

WIDTH = 1920
HEIGHT = 1080
TITLE = "Astro Jumper - Jogo de Plataforma com Pygame Zero"

# Jogo de Plataforma com Pygame Zero
# Controles:
# - Setas Esquerda/Direita ou A/D: Mover o personagem
# - Espaço ou Seta para Cima ou W: Pular        
# Voltado para encinoar conceitos basicos de programacao e desenvolvimento de jogos.
# Divirta-se jogando e aprendendo!
# Definição dos estados do jogo

class GameState:
    MENU = 0
    PLAYING = 1
    GAME_OVER = 2

current_state = GameState.MENU
score = 0
high_score = 0
music_on = True
sound_on = True
mouse_pos = (0, 0)

# Definição dos botões do menu
class Button:
    def __init__(self, x, y, w, h, text, callback):
        self.rect = Rect(x, y, w, h)
        self.text = text
        self.callback = callback
        self.hovered = False

    def draw(self):
        color = (100, 200, 255) if self.hovered else (50, 150, 255)
        screen.draw.filled_rect(self.rect, color)
        screen.draw.text(self.text, center=self.rect.center, fontsize=60, color="white")

    def update(self):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def click(self):
        if self.hovered:
            try: sounds.click.play()
            except: pass
            self.callback()

# Funções de controle do jogo
def start_game():
    global current_state, score, player, enemies
    current_state = GameState.PLAYING
    score = 0
    player.reset()
    enemies = [Enemy(400,800), Enemy(1400,750), Enemy(400,450), Enemy(1400,350), Enemy(600,250)]
    generate_level()

def toggle_music():
    global music_on
    music_on = not music_on
    if music_on:
        try: music.play("bg_music")
        except: pass
    else:
        music.stop()

def toggle_sound():
    global sound_on
    sound_on = not sound_on

def exit_game():
    exit()

# Criação dos botões do menu
buttons = [
    Button(WIDTH//2-250,350,500,110,"START GAME",start_game),
    Button(WIDTH//2-250,500,500,100,"Music: ON",toggle_music),
    Button(WIDTH//2-250,630,500,100,"Sound: ON",toggle_sound),
    Button(WIDTH//2-250,760,500,100,"Exit",exit_game),
]

# Definição dos elementos do jogo
platforms = []
coins = []

# Geração do nível
def generate_level():
    platforms[:] = [Rect(200,980,900,100),Rect(1020,980,900,100),Rect(600,850,300,50),Rect(100,700,300,50),Rect(1400,850,600,50),Rect(1000,650,300,50),Rect(500,500,300,50),Rect(1400,450,300,50),Rect(50,350,300,50),Rect(1000,250,300,50),Rect(500,150,300,50)]
    coins[:] = []
    for _ in range(18):
        while True:
            x = random.randint(150,WIDTH-200)
            y = random.randint(100,900)
            r = Rect(x,y,70,70)
            if not any(r.colliderect(p.inflate(100,100)) for p in platforms):
                coins.append(r)
                break

# Definição das classes do jogo
class Player:
    def __init__(self): self.reset()
    def reset(self):
        self.x = 250; self.y = 820; self.vx = 0; self.vy = 0; self.on_ground = True
        self.facing_right = True; self.idle_frame = 0; self.run_frame = 0; self.anim_timer = 0
    def update(self):
        self.vx = 0
        if keyboard.left or keyboard.a: self.vx = -8; self.facing_right = False
        if keyboard.right or keyboard.d: self.vx = 8; self.facing_right = True
        if (keyboard.space or keyboard.up or keyboard.w) and self.on_ground:
            self.vy = -20; self.on_ground = False
            if sound_on:
                try: sounds.jump.play()
                except: pass
        self.vy += 0.9; self.x += self.vx
        pr = Rect(self.x,self.y,100,150)
        for p in platforms:
            if pr.colliderect(p):
                if self.vx > 0: self.x = p.left - 100
                if self.vx < 0: self.x = p.right
        self.y += self.vy; self.on_ground = False
        pr = Rect(self.x,self.y,100,150)
        for p in platforms:
            if pr.colliderect(p):
                if self.vy > 0: self.y = p.top - 150; self.vy = 0; self.on_ground = True
                elif self.vy < 0: self.y = p.bottom; self.vy = 0
        if self.x < 0: self.x = 0
        if self.x > WIDTH-100: self.x = WIDTH-100
        if self.y > HEIGHT + 300: game_over()
        self.anim_timer += 1
        if self.on_ground:
            if self.vx != 0 and self.anim_timer % 5 == 0: self.run_frame = (self.run_frame + 1) % 6
            elif self.vx == 0 and self.anim_timer % 10 == 0: self.idle_frame = (self.idle_frame + 1) % 4
    def draw(self):
        if not self.on_ground: img = "hero_jump" if self.vy <= 0 else "hero_fall"
        elif self.vx != 0: img = f"hero_run_{self.run_frame}"
        else: img = f"hero_idle_{self.idle_frame}"
        try: screen.blit(img,(self.x,self.y))
        except: screen.draw.filled_rect(Rect(self.x,self.y,100,150),(0,200,255))

# Definição da classe inimigo
class Enemy:
    def __init__(self,x,y):
        self.x = x; self.y = y-100; self.start_x = x
        self.patrol = random.choice([250,350,450])
        self.speed = random.choice([-2.5,2.5])
        self.frame = 0; self.timer = 0
    def update(self):
        self.timer += 1
        if self.timer % 8 == 0: self.frame = (self.frame + 1) % 4
        self.x += self.speed
        if abs(self.x - self.start_x) > self.patrol: self.speed *= -1
        if Rect(self.x,self.y,120,120).colliderect(Rect(player.x,player.y,100,150)): game_over()
    def draw(self):
        img = f"alien_walk_{self.frame}" if abs(self.speed)>0.1 else f"alien_idle_{self.frame}"
        try: screen.blit(img,(self.x,self.y))
        except: screen.draw.filled_rect(Rect(self.x,self.y,120,120),(220,50,50))

# Funções de coleta e fim de jogo
def game_over():
    global current_state, high_score
    if sound_on:
        try: sounds.hurt.play()
        except: pass
    music.stop()
    current_state = GameState.GAME_OVER
    if score > high_score: high_score = score

# Coleta de moedas
def collect_coin(c):
    global score
    if sound_on:
        try: sounds.coin.play()
        except: pass
    coins.remove(c)
    score += 20

# Inicialização do jogo
player = Player()
enemies = []
generate_level()

def on_mouse_move(pos): global mouse_pos; mouse_pos = pos
def on_mouse_down(pos):
    global current_state
    if current_state == GameState.MENU:
        for b in buttons: b.click()
    elif current_state == GameState.GAME_OVER:
        current_state = GameState.MENU
        if music_on:
            try: music.play("bg_music")
            except: pass

# Loop principal do jogo
def update():
    if current_state == GameState.PLAYING:
        player.update()
        for e in enemies: e.update()
        pr = Rect(player.x,player.y,100,150)
        for c in coins[:]:
            if pr.colliderect(c): collect_coin(c)
        if not coins: generate_level(); score += 200
    elif current_state == GameState.MENU:
        for b in buttons:
            b.update()
            if "Music" in b.text: b.text = f"Music: {'ON' if music_on else 'OFF'}"
            if "Sound" in b.text: b.text = f"Sound: {'ON' if sound_on else 'OFF'}"

# Desenho dos elementos do jogo
def draw():
    screen.clear()
    try: screen.blit("bg",(0,0))
    except: screen.draw.filled_rect(Rect(0,0,WIDTH,HEIGHT),(5,5,30))
    if current_state == GameState.MENU:
        screen.draw.text("ASTRO JUMPER",center=(WIDTH//2,150),fontsize=140,color="white")
        for b in buttons: b.draw()
    elif current_state == GameState.PLAYING:
        for p in platforms:
            try: screen.blit("platform",p.topleft)
            except: screen.draw.filled_rect(p,(130,130,130))
        for c in coins:
            try: screen.blit("coin",c.topleft)
            except: screen.draw.filled_circle(c.center,35,(255,220,0))
        player.draw()
        for e in enemies: e.draw()
        screen.draw.text(f"SCORE: {score}",topleft=(60,40),fontsize=60,color="white")
    elif current_state == GameState.GAME_OVER:
        screen.draw.text("GAME OVER",center=(WIDTH//2,HEIGHT//2-120),fontsize=160,color=(255,50,50))
        screen.draw.text(f"Score: {score}   Best: {high_score}",center=(WIDTH//2,HEIGHT//2+30),fontsize=90,color="white")
        screen.draw.text("Clique para voltar",center=(WIDTH//2,HEIGHT//2+180),fontsize=70,color="white")

# Início da música de fundo
if music_on:
    try: music.play("bg_music"); music.set_volume(0.6)
    except: pass

    # Fim do código do jogo Astro Jumper
    # Divirta-se jogando e aprendendo!
    # Créditos:
    # Desenvolvido por Leonardo de Moura Fuseti
# Recursos de áudio e imagem obtidos de fontes gratuitas online
# Imagens e sons podem ser substituídos conforme desejado
