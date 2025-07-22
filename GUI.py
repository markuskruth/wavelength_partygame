import pygame, math, time

class GUI:
    def __init__(self, win_size):
        pygame.init()
        self.win_size = win_size
        self.win = pygame.display.set_mode(win_size)

        self.arrow_x = win_size[0] // 2
        self.curved_arrow_size = 50
        self.curved_arrow = pygame.transform.scale(pygame.image.load("./images/curved_arrow.png").convert_alpha(), (self.curved_arrow_size, self.curved_arrow_size))
    
    def draw_game_wheel(self):
        center_x = self.win_size[0] // 2

        big_circle_radius = self.win_size[0] // 1.9
        # Outline for the half-circle
        pygame.draw.circle(self.win, (0, 0, 0), (center_x, self.win_size[1]), self.win_size[0] // 1.85)
        # The half-circle
        pygame.draw.circle(self.win, (255, 255, 255), (center_x, self.win_size[1]), big_circle_radius)

    def draw_arrow(self):
        big_circle_radius = self.win_size[0] // 1.9
        center_x = self.win_size[0] // 2
        small_circle_radius = self.win_size[0] // 12

        # Small circle for the arrow
        pygame.draw.circle(self.win, (255, 0, 0), (center_x, self.win_size[1] - small_circle_radius // 2), small_circle_radius)

        # Arrow line
        funcion_y = self.win_size[1] - math.sqrt(
                                        (max( 
                                            (big_circle_radius-small_circle_radius)**2 - (self.arrow_x - center_x)**2,
                                            0)
                                        ))
        pygame.draw.line(self.win, (255, 0, 0), 
                         (center_x, self.win_size[1] - small_circle_radius // 2), 
                         (self.arrow_x, funcion_y), 
                         width=10)


    def rotate_arrow(self, direction):
        arrow_x_bound = 60
        if direction == "left":
            self.arrow_x = max(self.arrow_x - 1, arrow_x_bound)
        elif direction == "right":
            self.arrow_x = min(self.arrow_x + 1, self.win_size[0]-arrow_x_bound)
        else:
             print("Direction must be either 'left' or 'right'")
             

    def render(self):
        self.win.fill((200, 200, 200))

        center_x = self.win_size[0] // 2
        bottom_y = self.win_size[1]

        # Draw the game wheel
        self.draw_game_wheel()

        # Draw the arrow
        self.draw_arrow()

        # Arrow rotate buttons
        right_arrow_topleft_coords = (center_x-60, bottom_y-60)
        left_arrow_topleft_coords = (center_x+10, bottom_y-60)
        right_arrow = self.curved_arrow
        left_arrow = pygame.transform.flip(pygame.transform.rotate(self.curved_arrow, 180), flip_x=False, flip_y=True)
        self.win.blit(right_arrow, left_arrow_topleft_coords)
        self.win.blit(left_arrow, right_arrow_topleft_coords)


        # Track mouse clicks
        mouse = pygame.mouse
        mouse_x,mouse_y = mouse.get_pos()
        if mouse.get_pressed()[0]:
            if ((mouse_x > right_arrow_topleft_coords[0] and mouse_x < right_arrow_topleft_coords[0] + self.curved_arrow_size) and
                (mouse_y > right_arrow_topleft_coords[1] and mouse_y < right_arrow_topleft_coords[1] + self.curved_arrow_size)):
                    self.rotate_arrow("left")
                    time.sleep(0.005)

            elif ((mouse_x > left_arrow_topleft_coords[0] and mouse_x < left_arrow_topleft_coords[0] + self.curved_arrow_size) and
                (mouse_y > left_arrow_topleft_coords[1] and mouse_y < left_arrow_topleft_coords[1] + self.curved_arrow_size)):
                    self.rotate_arrow("right")                
                    time.sleep(0.005)

        
        pygame.event.get() 
        pygame.display.update()
    
