import pygame, math, time, random

class GUI:
    def __init__(self, win_size):
        pygame.init()
        self.win_size = win_size
        self.win = pygame.display.set_mode(win_size)

        self.arrow_x = 90  # Initial angle for the arrow in degrees
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
        center_y = self.win_size[1]
        small_circle_radius = self.win_size[0] // 12

        # Small circle for the arrow
        pygame.draw.circle(self.win, (255, 0, 0), (center_x, self.win_size[1] - small_circle_radius // 2), small_circle_radius)

        # Arrow line
        pygame.draw.line(self.win, (255, 0, 0), 
                         (center_x, self.win_size[1] - small_circle_radius // 2), 
                         (center_x + math.cos(math.radians(self.arrow_x)) * big_circle_radius, center_y - math.sin(math.radians(self.arrow_x)) * big_circle_radius),
                         width=10)


    def rotate_arrow(self, direction):
        if direction == "right":
            self.arrow_x = max(self.arrow_x - 0.5, 0)  # Limit to 0 degrees
        elif direction == "left":
            self.arrow_x = min(self.arrow_x + 0.5, 180)  # Limit to 180 degrees
        else:
             print("Direction must be either 'left' or 'right'")
             

    # Draw the scoring range areas using polar coordinates
    def draw_scoring_range(self, target_angle):
        big_circle_radius = self.win_size[0] // 1.9
        center_x = self.win_size[0] // 2
        center_y = self.win_size[1]
        small_circle_radius = self.win_size[0] // 12

        angle = math.radians(10)

        # Middle section
        theta1 = target_angle
        theta2 = target_angle + angle

        x1 = center_x + math.cos(theta1) * big_circle_radius
        y1 = center_y - math.sin(theta1) * big_circle_radius

        x2 = center_x + math.cos(theta2) * big_circle_radius
        y2 = center_y - math.sin(theta2) * big_circle_radius

        pygame.draw.polygon(self.win, (0, 255, 0), [
            (x1, y1), 
            (x2, y2),
            (center_x, self.win_size[1] - small_circle_radius // 2)
        ])

        for i in range(1,3):
            # Left side
            theta1 = target_angle + angle * i
            theta2 = target_angle + angle * (i + 1)

            x1 = center_x + math.cos(theta1) * big_circle_radius
            y1 = center_y - math.sin(theta1) * big_circle_radius

            x2 = center_x + math.cos(theta2) * big_circle_radius
            y2 = center_y - math.sin(theta2) * big_circle_radius

            pygame.draw.polygon(self.win, (0, 255-i*50, 0), [
                (x1, y1), 
                (x2, y2),
                (center_x, self.win_size[1] - small_circle_radius // 2)
            ])

            # Right side
            theta1 = target_angle - angle * (i-1)
            theta2 = target_angle - angle * i

            x1 = center_x + math.cos(theta1) * big_circle_radius
            y1 = center_y - math.sin(theta1) * big_circle_radius

            x2 = center_x + math.cos(theta2) * big_circle_radius
            y2 = center_y - math.sin(theta2) * big_circle_radius
            pygame.draw.polygon(self.win, (0, 255-i*50, 0), [
                (x1, y1), 
                (x2, y2),
                (center_x, self.win_size[1] - small_circle_radius // 2)
            ])

        

    def render(self, target_angle):
        self.win.fill((200, 200, 200))

        center_x = self.win_size[0] // 2
        bottom_y = self.win_size[1]

        # Draw the game wheel
        self.draw_game_wheel()

        # Draw scoring range
        self.draw_scoring_range(target_angle)

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
                    time.sleep(0.01)

            elif ((mouse_x > left_arrow_topleft_coords[0] and mouse_x < left_arrow_topleft_coords[0] + self.curved_arrow_size) and
                (mouse_y > left_arrow_topleft_coords[1] and mouse_y < left_arrow_topleft_coords[1] + self.curved_arrow_size)):
                    self.rotate_arrow("right")                
                    time.sleep(0.01)

        
        pygame.event.get() 
        pygame.display.update()
    
