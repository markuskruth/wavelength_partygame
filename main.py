import GUI, Game
import pygame, keyboard


win_size = (800, 600)
player_names = ["Markus", "Tyko", "Otso"]
colors = [(255, 0, 255), (0, 255, 255), (0, 0, 255)]
player_colors = {name: color for name, color in zip(player_names, colors)}

if __name__ == "__main__":
    gui = GUI.GUI(win_size)
    game = Game.Game(len(player_names), player_names)
    question = game.next_question()
    target_angle = game.next_target_angle()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if keyboard.is_pressed("q"):
            running = False
        
        gui.render(target_angle, question, game, player_colors)

        if game.new_round:
            question = game.next_question()
            target_angle = game.next_target_angle()
            game.new_round = False
        
    
    pygame.quit()