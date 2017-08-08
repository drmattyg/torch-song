try:
    import pygame
except Execption as e:
    print('failed to load pygame')


class Sound:
    def __init__(self):
        try:
            pygame.init()
            pygame.mixer.init()
        except Exception as e:
            logging.error('failed to initialize sound module:')

    def play(self, filename):
        try:
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
        except Exception as e:
            logging.error('failed to play music:' + filename)

    def stop(self):
        try:
            pygame.mixer.music.fadeout(2)
        except Exception as e:
            pass

    def kill(self):
        try:
            pygame.mixer.quit()
            pygame.quit()
        except Exception as e:
            pass

    def __del__(self):
        self.kill()

