import GUI
import pygame, keyboard

if __name__ == "__main__":
    gui = GUI.GUI((800, 600))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if keyboard.is_pressed("q"):
            running = False
        
        gui.render()
    
    pygame.quit()