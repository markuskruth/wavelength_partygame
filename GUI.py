import pygame, math, time

class GUI:
    def __init__(self, win_size):
        pygame.init()
        self.win_size = win_size
        self.win = pygame.display.set_mode(win_size)
        pygame.display.set_caption("Wavelength Party Game")

        self.big_circle_radius = win_size[0] // 1.9
        self.arrow_circle_radius = win_size[0] // 12
        self.arrow_angle = 90  # Initial angle for the arrow in degrees
        self.curved_arrow_size = 50
        self.curved_arrow = pygame.transform.scale(pygame.image.load("./images/curved_arrow_button.png").convert_alpha(), (self.curved_arrow_size, self.curved_arrow_size))
        
        self.button_size = (150, 40)
        self.button_text_padding = (5, 10)
        self.center_x = self.win_size[0] // 2
        self.bottom_y = self.win_size[1]

        self.hide_state = False
        self.round_ended = False
        self.disable_submit = False

    
    def draw_game_wheel(self):
        outline_circle_radius = self.big_circle_radius + 10
        # Outline for the half-circle
        pygame.draw.circle(self.win, (0, 0, 0), (self.center_x, self.bottom_y), outline_circle_radius)
        # The half-circle
        pygame.draw.circle(self.win, (255, 255, 255), (self.center_x, self.bottom_y), self.big_circle_radius)

    def draw_arrow(self, rotate_right_button_coords, rotate_left_button_coords):
        # Small circle for the arrow
        pygame.draw.circle(self.win, (255, 0, 0), (self.center_x, self.bottom_y - self.arrow_circle_radius // 2), self.arrow_circle_radius)

        # Arrow line
        pygame.draw.line(self.win, (255, 0, 0), 
                         (self.center_x, self.bottom_y - self.arrow_circle_radius // 2), 
                         (self.center_x + math.cos(math.radians(self.arrow_angle)) * self.big_circle_radius, self.bottom_y - math.sin(math.radians(self.arrow_angle)) * self.big_circle_radius),
                         width=10)

        left_arrow = pygame.transform.rotate(pygame.transform.flip(self.curved_arrow, flip_x=False, flip_y=True), 90)
        right_arrow = pygame.transform.rotate(self.curved_arrow, 90)
        self.win.blit(right_arrow, rotate_right_button_coords)
        self.win.blit(left_arrow, rotate_left_button_coords)

    def draw_guess_arrows(self, guesses, player_colors):
        names = guesses.keys()
        for name in names:
            guess_angle = guesses[name]
            pygame.draw.line(self.win, player_colors[name], 
                         (self.center_x, self.bottom_y - self.arrow_circle_radius // 2), 
                         (self.center_x + math.cos(math.radians(guess_angle)) * self.big_circle_radius, self.bottom_y - math.sin(math.radians(guess_angle)) * self.big_circle_radius),
                         width=10)

    def rotate_arrow(self, direction):
        if direction == "right":
            self.arrow_angle = max(self.arrow_angle - 0.5, 0)  # Limit to 0 degrees
        elif direction == "left":
            self.arrow_angle = min(self.arrow_angle + 0.5, 180)  # Limit to 180 degrees
        else:
             print("Direction must be either 'left' or 'right'")
             

    # Draw the scoring range areas using polar coordinates
    def draw_scoring_range(self, target_angle):
        angle = math.radians(10)

        # Middle section
        theta1 = target_angle
        theta2 = target_angle + angle

        x1 = self.center_x + math.cos(theta1) * self.big_circle_radius
        y1 = self.bottom_y - math.sin(theta1) * self.big_circle_radius

        x2 = self.center_x + math.cos(theta2) * self.big_circle_radius
        y2 = self.bottom_y - math.sin(theta2) * self.big_circle_radius

        pygame.draw.polygon(self.win, (0, 255, 0), [
            (x1, y1), 
            (x2, y2),
            (self.center_x, self.bottom_y - self.arrow_circle_radius // 2)
        ])

        for i in range(1,3):
            # Left side
            theta1 = target_angle + angle * i
            theta2 = target_angle + angle * (i + 1)

            x1 = self.center_x + math.cos(theta1) * self.big_circle_radius
            y1 = self.bottom_y - math.sin(theta1) * self.big_circle_radius

            x2 = self.center_x + math.cos(theta2) * self.big_circle_radius
            y2 = self.bottom_y - math.sin(theta2) * self.big_circle_radius

            pygame.draw.polygon(self.win, (0, 255-i*50, 0), [
                (x1, y1), 
                (x2, y2),
                (self.center_x, self.bottom_y - self.arrow_circle_radius // 2)
            ])

            # Right side
            theta1 = target_angle - angle * (i-1)
            theta2 = target_angle - angle * i

            x1 = self.center_x + math.cos(theta1) * self.big_circle_radius
            y1 = self.bottom_y - math.sin(theta1) * self.big_circle_radius

            x2 = self.center_x + math.cos(theta2) * self.big_circle_radius
            y2 = self.bottom_y - math.sin(theta2) * self.big_circle_radius
            pygame.draw.polygon(self.win, (0, 255-i*50, 0), [
                (x1, y1), 
                (x2, y2),
                (self.center_x, self.bottom_y - self.arrow_circle_radius // 2)
            ])


    def draw_players(self, game, player_colors):
        font = pygame.font.Font(None, 36)
        text_y = 10
        text_width = 130
        for name in (game.player_names):
            name_surface = font.render(f"{name}: {game.player_scores[name]}", True, player_colors[name])
            pygame.draw.rect(self.win, (255, 255, 255), (10, text_y, text_width, 30))
            self.win.blit(name_surface, (10, text_y))
            if name == game.hint_giver:
                hint_giver_surface = font.render("HINT GIVER", True, (255, 150, 0))
                self.win.blit(hint_giver_surface, (text_width + 20, text_y))
            
            elif name == game.turn and game.turn_index < len(game.possible_turns):
                pygame.draw.circle(self.win, (255,0,0), (text_width + 30, text_y + 15), 10)
            text_y += 40

    def hide_wheel(self):
        # Draw a white circle to cover the game wheel
        pygame.draw.circle(self.win, (255, 255, 255), (self.center_x, self.win_size[1]), self.big_circle_radius)

    def draw_question(self, question):
        font = pygame.font.Font(None, 36)
        question_left = font.render(question[0], True, (0, 0, 0))
        question_right = font.render(question[1], True, (0, 0, 0))
        question_left_rect = question_left.get_rect(center=(len(question[0]) + self.win_size[0] // 6, self.win_size[1] - 50))
        question_right_rect = question_right.get_rect(center=(5 * self.win_size[0] // 6 - len(question[1]), self.win_size[1] - 50))
        self.win.blit(question_left, question_left_rect)
        self.win.blit(question_right, question_right_rect)



    def render(self, target_angle, question, game, player_colors):
        self.win.fill((200, 200, 200))

        # Draw player names
        self.draw_players(game, player_colors)

        # Draw the game wheel
        self.draw_game_wheel()

        if self.hide_state:
            self.hide_wheel()
        else:
            # Draw scoring range
            self.draw_scoring_range(target_angle)
        
        if self.round_ended:
            self.draw_guess_arrows(game.guesses, player_colors)
        
        # Draw the question
        self.draw_question(question)

        # Draw the arrow
        rotate_left_button_coords = (self.center_x-60, self.win_size[1]-60)
        rotate_right_button_coords = (self.center_x+10, self.win_size[1]-60)
        self.draw_arrow(rotate_right_button_coords, rotate_left_button_coords)


        # Hide wheel button
        hide_wheel_button_coords = (self.win_size[0] - (self.button_size[0] + 20), 20)
        pygame.draw.rect(self.win, (255, 0, 0), (*hide_wheel_button_coords, *self.button_size))
        hide_wheel_text = pygame.font.Font(None, 36).render("Hide", True, (255, 255, 255))
        self.win.blit(hide_wheel_text, (hide_wheel_button_coords[0] + self.button_text_padding[0], hide_wheel_button_coords[1] + self.button_text_padding[1]))

        # Submit guess button
        submit_guess_button_coords = (hide_wheel_button_coords[0], hide_wheel_button_coords[1] + self.button_size[1]+10)
        if self.disable_submit:
            pygame.draw.rect(self.win, (150, 150, 150), (*submit_guess_button_coords, *self.button_size))
        else:
            pygame.draw.rect(self.win, (255, 0, 0), (*submit_guess_button_coords, *self.button_size))
        submit_guess_text = pygame.font.Font(None, 36).render("Submit", True, (255, 255, 255))
        self.win.blit(submit_guess_text, (submit_guess_button_coords[0] + self.button_text_padding[0], submit_guess_button_coords[1] + self.button_text_padding[1]))

        # End round button
        end_round_button_coords = (submit_guess_button_coords[0], submit_guess_button_coords[1] + self.button_size[1] + 10)
        pygame.draw.rect(self.win, (255, 0 ,0), (*end_round_button_coords, *self.button_size))
        if self.round_ended:
            end_round_text = pygame.font.Font(None, 36).render("Next round", True, (255, 255, 255))
        else:
            end_round_text = pygame.font.Font(None, 36).render("End round", True, (255, 255, 255))
        self.win.blit(end_round_text, (end_round_button_coords[0] + self.button_text_padding[0], end_round_button_coords[1] + self.button_text_padding[1]))

        # Track mouse clicks
        mouse = pygame.mouse
        mouse_x,mouse_y = mouse.get_pos()

        # Hide wheel button
        if mouse_x > hide_wheel_button_coords[0] and mouse_x < hide_wheel_button_coords[0] + self.button_size[0] and \
           mouse_y > hide_wheel_button_coords[1] and mouse_y < hide_wheel_button_coords[1] + self.button_size[1]:
            pygame.draw.rect(self.win, (255, 100, 0), (*hide_wheel_button_coords, *self.button_size))
            self.win.blit(hide_wheel_text, (hide_wheel_button_coords[0] + self.button_text_padding[0], hide_wheel_button_coords[1] + self.button_text_padding[1]))
            if mouse.get_pressed()[0]:
                self.hide_state = not self.hide_state
                time.sleep(0.1)
        
        # Submit guess button
        elif mouse_x > submit_guess_button_coords[0] and mouse_x < submit_guess_button_coords[0] + self.button_size[0] and \
           mouse_y > submit_guess_button_coords[1] and mouse_y < submit_guess_button_coords[1] + self.button_size[1]:
            if self.disable_submit:
                pygame.draw.rect(self.win, (150, 150, 150), (*submit_guess_button_coords, *self.button_size))
            else:
                pygame.draw.rect(self.win, (255, 100, 0), (*submit_guess_button_coords, *self.button_size))
            self.win.blit(submit_guess_text, (submit_guess_button_coords[0] + self.button_text_padding[0], submit_guess_button_coords[1] + self.button_text_padding[1]))
            if mouse.get_pressed()[0] and not self.disable_submit:
                game.guesses[game.turn] = self.arrow_angle
                self.disable_submit = not game.next_turn()
                time.sleep(0.5)
        
        # End / Start round button
        elif mouse_x > end_round_button_coords[0] and mouse_x < end_round_button_coords[0] + self.button_size[0] and \
           mouse_y > end_round_button_coords[1] and mouse_y < end_round_button_coords[1] + self.button_size[1]:
            pygame.draw.rect(self.win, (255, 100, 0), (*end_round_button_coords, *self.button_size))
            self.win.blit(end_round_text, (end_round_button_coords[0] + self.button_text_padding[0], end_round_button_coords[1] + self.button_text_padding[1]))
            if mouse.get_pressed()[0]:
                self.round_ended = not self.round_ended
                self.arrow_angle = 90
                if self.round_ended:
                    game.end_round(target_angle, game.guesses)
                    self.hide_state = False
                else:
                    self.disable_submit = False
                    game.start_round()
                time.sleep(0.5)


        if mouse.get_pressed()[0]:
            if ((mouse_x > rotate_left_button_coords[0] and mouse_x < rotate_left_button_coords[0] + self.curved_arrow_size) and
                (mouse_y > rotate_left_button_coords[1] and mouse_y < rotate_left_button_coords[1] + self.curved_arrow_size)):
                    self.rotate_arrow("left")
                    time.sleep(0.01)

            elif ((mouse_x > rotate_right_button_coords[0] and mouse_x < rotate_right_button_coords[0] + self.curved_arrow_size) and
                (mouse_y > rotate_right_button_coords[1] and mouse_y < rotate_right_button_coords[1] + self.curved_arrow_size)):
                    self.rotate_arrow("right")                
                    time.sleep(0.01)

        
        pygame.event.get() 
        pygame.display.update()
    
