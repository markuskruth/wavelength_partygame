import GUI, Game
import pygame, keyboard, random, math


win_size = (800, 600)
if __name__ == "__main__":
    gui = GUI.GUI(win_size)
    target_angle = random.randint(20, 160) * math.pi / 180  # Random target angle in radians

    player_names = ["Markus", "Tyko", "Otso"]
    game = Game.Game(len(player_names), player_names)
    question = game.next_question()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if keyboard.is_pressed("q"):
            running = False
        
        gui.render(target_angle, question, game)

        if game.new_round:
            question = game.next_question()
            target_angle = random.randint(20, 160) * math.pi / 180
            game.new_round = False
        
    
    pygame.quit()