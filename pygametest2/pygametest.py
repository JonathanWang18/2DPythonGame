import pygame

pygame.init()

win = pygame.display.set_mode((500, 480))

pygame.display.set_caption("First Game")

walkRight = [pygame.image.load('Images/R1.png'), pygame.image.load('Images/R2.png'), pygame.image.load('Images/R3.png'),
             pygame.image.load('Images/R4.png'), pygame.image.load('Images/R5.png'), pygame.image.load('Images/R6.png'),
             pygame.image.load('Images/R7.png'), pygame.image.load('Images/R8.png'), pygame.image.load('Images/R9.png')]
walkLeft = [pygame.image.load('Images/L1.png'), pygame.image.load('Images/L2.png'), pygame.image.load('Images/L3.png'),
            pygame.image.load('Images/L4.png'), pygame.image.load('Images/L5.png'), pygame.image.load('Images/L6.png'),
            pygame.image.load('Images/L7.png'), pygame.image.load('Images/L8.png'), pygame.image.load('Images/L9.png')]
bg = pygame.image.load('bg.jpg').convert()
bgx = 0
bgx2 = bg.get_width()


char = pygame.image.load('Images/standing.png')

clock = pygame.time.Clock()


class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 0
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not (self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))


class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


def redrawGameWindow():
    win.blit(bg, (bgx, 0))
    win.blit(bg, (bgx2,0))
    man.draw(win)
    for bullet in bullets:
        bullet.draw(win)

    pygame.display.update()


# mainloop
man = player(20, 410, 64, 64)
bullets = []
run = True
while run:
    clock.tick(27)
    bgx -= 1.4
    bgx2 -= 1.4
    if bgx < bg.get_width() * -1:
        bgx = bg.get_width()
    if bgx2 < bg.get_width() * -1:
        bgx2 = bg.get_width()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        if man.left:
            facing = -1
        else:
            facing = 1

        if len(bullets) < 5:
            bullets.append(
                projectile(round(man.x + man.width // 2), round(man.y + man.height // 2), 6, (0, 0, 0), facing))

    if keys[pygame.K_LEFT]:
        man.vel = -5
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT]:
        man.vel = 5
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0
        man.vel = 0

    if not (man.isJump):
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
    man.x += man.vel

    redrawGameWindow()

pygame.quit()