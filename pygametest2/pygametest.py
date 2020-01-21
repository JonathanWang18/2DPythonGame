import pygame

pygame.init() #initializes pygame library

win = pygame.display.set_mode((638, 361)) #sets boundaries for game window

pygame.display.set_caption("PIXEL KNIGHT") #name of game
#arrays holding images for attack animation
attack1 = [pygame.image.load('NewImages/attack1_1.png'), pygame.image.load('NewImages/attack1_2.png'),
             pygame.image.load('NewImages/attack1_3.png'), pygame.image.load('NewImages/attack1_4.png'),
             pygame.image.load('NewImages/attack1_5.png'), pygame.image.load('NewImages/attack1_6.png')]
attack2 = [pygame.image.load('NewImages/lattack1_1.png'), pygame.image.load('NewImages/lattack1_2.png'),
             pygame.image.load('NewImages/lattack1_3.png'), pygame.image.load('NewImages/lattack1_4.png'),
             pygame.image.load('NewImages/lattack1_5.png'), pygame.image.load('NewImages/lattack1_6.png')]
#arrays holding images for jump animation
jump1 = [pygame.image.load('NewImages/jump_1.png'), pygame.image.load('NewImages/jump_2.png'),
             pygame.image.load('NewImages/jump_3.png'), pygame.image.load('NewImages/jump_4.png'),
             pygame.image.load('NewImages/jump_5.png')]
jump2 = [pygame.image.load('NewImages/ljump_1.png'), pygame.image.load('NewImages/ljump_2.png'),
             pygame.image.load('NewImages/ljump_3.png'), pygame.image.load('NewImages/ljump_4.png'),
             pygame.image.load('NewImages/ljump_5.png')]
#arrays holding images for walk animation
walkRight = [pygame.image.load('NewImages/ready_1.png'), pygame.image.load('NewImages/run_1.png'),
             pygame.image.load('NewImages/run_2.png'), pygame.image.load('NewImages/run_3.png'),
             pygame.image.load('NewImages/run_4.png'), pygame.image.load('NewImages/run_5.png'),
             pygame.image.load('NewImages/run_6.png'),]
walkLeft = [pygame.image.load('NewImages/lready_1.png'), pygame.image.load('NewImages/lrun_1.png'),
            pygame.image.load('NewImages/lrun_2.png'), pygame.image.load('NewImages/lrun_3.png'),
             pygame.image.load('NewImages/lrun_4.png'), pygame.image.load('NewImages/lrun_5.png'),
            pygame.image.load('NewImages/lrun_6.png'),]

bg = pygame.image.load('NewImages/bg.gif').convert() #background image
bgx = 0
bgx2 = bg.get_width()

char = pygame.image.load('NewImages/ready_1.png') #player

clock = pygame.time.Clock() #initializes clock

score = 0 #score
#class holds the functionality of the player's movement and attacks || Cred: Lac-Phong Nguyen
class player(object):
    def __init__(self, x, y, width, height): #constructor for player
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 0
        self.isJump = False
        self.left = False
        self.right = False
        self.attackCount = 0
        self.walkCount = 0
        self.jumpCount = 10
        self.jumpCount1 = 0
        self.standing = True
        self.hitbox = (self.x + 38, self.y + 24, 32, 60)
        self.health = 10
        self.visible = True
        self.attacking = False

    def hit(self): #function for when player is hit by the goblin
        if self.health > 0: #when health is above 0 the player will lose health when he is hit by the goblin
            self.health -= 1
        else: #if the player's health is 0 he disappears
            self.visible = False

    def draw(self, win): #function for animations
        if self.health > 0: #when the player is not dead
            if self.attackCount + 1 >= 12: #plays through attack animation once then stops
                self.visible = True
                self.attackCount = 0
                self.attacking = False
            if self.attacking: #plays actual animation of attacking
                if self.right: #plays right-facing attack
                    self.visible = False
                    win.blit(attack1[self.attackCount // 2], (self.x - 30, self.y - 30)) #runs through animation
                    self.attackCount += 1
                    self.hitbox = (self.x + 70, self.y + 24, 32, 60) #extends player's initial hitbox when he attacks
                else: #plays left-facing attack
                    self.visible = False
                    win.blit(attack2[self.attackCount // 2], (self.x - 80, self.y - 35))
                    self.attackCount += 1
                    self.hitbox = (self.x - 10, self.y + 24, 32, 60)
            if self.jumpCount1 + 1 >= 15: #plays through jump animation once then stops
                self.visible = True
                self.jumpCount1 = 0
            if self.isJump: #plays actual jump animation
                if self.left: #plays left-facing jump
                    self.visible = False
                    win.blit(jump2[self.jumpCount1 // 3], (self.x, self.y))
                    self.jumpCount1 += 1
                    self.hitbox = (self.x + 38, self.y + 24, 32, 60) #makes hitbox follow player when jumping
                else: #plays right-facing jump
                    self.visible = False
                    win.blit(jump1[self.jumpCount1 // 3], (self.x, self.y))
                    self.jumpCount1 += 1
                    self.hitbox = (self.x + 38, self.y + 24, 32, 60)
            #when player is visible (had to do this because the jumping and attacking animations would play while the
            #normal walking animation was playing)
            if self.visible:
                if self.walkCount + 1 >= 21: #runs through all the walking animations and loops
                    self.walkCount = 0
                if not self.standing:
                    if self.left: #plays left-facing walk
                        win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                        self.walkCount += 1
                    elif self.right: #plays right-facing walk
                        win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                        self.walkCount += 1
                else: #checks last key pressed and makes player face that direction
                    if self.right:
                        win.blit(walkRight[0], (self.x, self.y))
                    else:
                        win.blit(walkLeft[0], (self.x, self.y))
                if not self.attacking: #default hitbox
                    self.hitbox = (self.x + 38, self.y + 24, 32, 60)
            #health bars
            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0] - 10, self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0] - 10, self.hitbox[1] - 20, 50 - ((50 / 10) * (10 - self.health)), 10))

#class for functionality of enemy movement and hitbox || Cred: Lac-Phong Nguyen
class enemy(object):
    #arrays for images for walking animation
    walkRight = [pygame.image.load('Images/R1E.png'), pygame.image.load('Images/R2E.png'),
                 pygame.image.load('Images/R3E.png'), pygame.image.load('Images/R4E.png'),
                 pygame.image.load('Images/R5E.png'), pygame.image.load('Images/R6E.png'),
                 pygame.image.load('Images/R7E.png'), pygame.image.load('Images/R8E.png'),
                 pygame.image.load('Images/R9E.png'), pygame.image.load('Images/R10E.png'),
                 pygame.image.load('Images/R11E.png')]
    walkLeft = [pygame.image.load('Images/L1E.png'), pygame.image.load('Images/L2E.png'),
                pygame.image.load('Images/L3E.png'), pygame.image.load('Images/L4E.png'),
                pygame.image.load('Images/L5E.png'), pygame.image.load('Images/L6E.png'),
                pygame.image.load('Images/L7E.png'), pygame.image.load('Images/L8E.png'),
                pygame.image.load('Images/L9E.png'), pygame.image.load('Images/L10E.png'),
                pygame.image.load('Images/L11E.png')]

    def __init__(self, x, y, width, height, end): #constructor
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True


    def draw(self, win): #draws out goblin and his functionalities
        self.move()
        if self.visible: #while he's alive
            if self.walkCount + 1 >= 33: #plays through walk animation
                self.walkCount = 0
            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            #healthbars
            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - ((50/10) * (10 - self.health)), 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57) #hitbox

    def move(self): #moves the goblin back and forth
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self): #hit function for when player hits goblin with attack
        if self.health > 0: #takes damage
            self.health -= 1
        else: #when health drops to 0 or below dies
            self.visible = False

def redrawGameWindow(): #generates all sprites and backgrounds needed for game
    win.blit(bg, (bgx, 0))
    win.blit(bg, (bgx2, 0))
    text = font.render('Score: ' + str(score), 1, (255, 255, 255))
    win.blit(text, (10, 5))
    goblin.draw(win)
    man.draw(win)
    pygame.display.update()

# mainloop
font = pygame.font.SysFont('arialblack', 15, True) #sets font for score
man = player(250, 215, 64, 64) #creates instances of objects player and enemy
goblin = enemy(0, 235, 64, 64, 450)
currentnbgxpos = 0 - bg.get_width()
currentbgxpos = 0
currentbgx2pos = bg.get_width()
run = True #runs game
while run: #Cred: Lac-Phong Nguyen, Jonathan Wang
    keys = pygame.key.get_pressed() #allows you to delegate executions based on player inputs
    clock.tick(30) #frames per second
    if man.y == 215: #when player is on the ground he is alive
        man.visible = True
    if goblin.health > 0: #while goblin is alive
        if not man.attacking: #if the player is not attacking allow goblin to damage him
            if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] > goblin.hitbox[1]:
                if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                    if man.health > 0: #allows player to take damage and get hit and makes player lose points
                        man.hit()
                        score -= 5
                if man.health == 0: #kills player and displays game over screen
                    score += 0
                    goblin.visible = False
                    bg = pygame.image.load('gameover.jpg')
    if man.attacking: #while the player is attacking
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] > goblin.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                if goblin.health > 0: #goblin loses health if he is hit and player gets points
                    goblin.hit()
                    score += 5
                else:
                    goblin.visible = False #goblin dies when he hits 0 health
    for event in pygame.event.get(): #ends game when player clicks red X button
        if event.type == pygame.QUIT:
            run = False
    if keys[pygame.K_SPACE]: #player attacks when spacebar is hit
        man.attacking = True
    if man.health > 0: #when the player is alive he can move around (left, right, jump)
        if keys[pygame.K_LEFT]: #moves player left when player presses left arrow key
            man.vel = -5
            man.left = True
            man.right = False
            man.standing = False
        elif keys[pygame.K_RIGHT]: #moves player left when player presses right arrow key
            man.vel = 5
            man.right = True
            man.left = False
            man.standing = False
        else:
            man.standing = True
            man.walkCount = 0
            man.vel = 0

        if not (man.isJump): #player jumps
            if keys[pygame.K_UP]:
                man.isJump = True
                man.walkCount = 0
        else:
            if man.jumpCount >= -10:
                neg = 1
                if man.jumpCount < 0:
                    neg = -1
                man.y -= (man.jumpCount ** 2) * 0.5 * neg
                man.jumpCount -= 1
            else:
                man.isJump = False
                man.jumpCount = 10
        #Adds velocity values to man.x to change player position accordingly to movement key activity
        man.x += man.vel

        if man.x < 5:
            man.x = 5
        if man.x > 318:
            man.x = 319
        #makes it so that when the player hits the x-coordinate of 318 the background moves with him
        #Cred: Jonathan Wang
        if man.x > 318 and (keys[pygame.K_RIGHT]):
            man.x = 319
            bgx -= 4
            bgx2 -= 4
            #saves the values of bgx and bgx2 to global variables to update
            currentbgxpos = bgx
            currentbgx2pos = bgx2

    #Cred: Jonathan Wang
    #sets the x position of both backgroundss to the newly modified values from the conditional above
    bgx = currentbgxpos
    bgx2 = currentbgx2pos
    #once bg x position is at negative width x of bg, reset the bg x to the positive width x coordinate so it can move leftwards
    if bgx < bg.get_width() * -1:
        bgx = bg.get_width()
    if bgx2 < bg.get_width() * -1:
        bgx2 = bg.get_width()
    redrawGameWindow()
#terminate the program if run is set to False
pygame.quit()
