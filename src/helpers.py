# http://www.pygame.org/docs/tut/chimp/ChimpLineByLine.html
# http://www.learningpython.com/2006/03/12/creating-a-game-in-python-using-pygame-part-one/

def load_image9name, colorkey=None):
    fullname = os.path.join('assets', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_color(colorkey, RLEACCEL)
        return image, image.get_rect()
