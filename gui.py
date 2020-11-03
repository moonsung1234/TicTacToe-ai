import pygame as pg

class Gui :
    def __init__(self, width, height) :
        self.width = width
        self.height = height
        self.table = list()

        pg.init()

        self.screen = pg.display.set_mode((self.width, self.height))
        self.clock = pg.time.Clock()
        
        self.default_rgb = (255, 255, 255)
        self.button_rgb = (100, 100, 100)
        self.player1_rgb = (10, 10, 10)
        self.player2_rgb = (255, 0, 0)

        self.game_state = True

        pg.display.set_caption("tic-tac-toe")

    def setTable(self, player_order, index) :
        btn_x = self.table[index][0]
        btn_y = self.table[index][1]
        btn_width = self.table[index][3]
        btn_height = self.table[index][4]
        btn_rgb = None

        if player_order == 0 :
            self.table[index][2] = btn_rgb = self.player1_rgb

        elif player_order == 1 :
            self.table[index][2] = btn_rgb = self.player2_rgb

        pg.draw.rect(self.screen, btn_rgb, (btn_x, btn_y, btn_width, btn_height))
        pg.display.update()

    def getTable(self) :
        return self.table

    def start(self) :
        while self.game_state :
            for event in pg.event.get() :
                if event.type == pg.KEYDOWN :
                    if event.key == pg.K_SPACE :
                        self.game_state = False
                        print("종료")

            self.screen.fill(pg.color.Color(self.default_rgb))

            x, y = 0, 0

            for i in range(9) :
                pg.draw.rect(self.screen, self.button_rgb, (x, y, self.width/3, self.height/3), 2)
                self.table.append([x, y, self.button_rgb, self.width/3, self.height/3])
                
                x += self.width / 3

                if i == 2 or i == 5:
                    x = 0
                    y += self.height / 3

            pg.display.update()

            self.setTable(0, 0)
            self.clock.tick(30)

        pg.quit()


    
    
