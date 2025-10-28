# Name: Warren Roberts

# Description: Porting A4/A6 to Python:
# In poting this game, I started implementing the sprite class and 
# the model class. After this, moved on to the view and controller classes.
# I then implemented the luigi class and the brick class. I then,
# implemented the mushroom class and the drybones class. After that,
# I implemented the goomba class and the fireball class. For all of
# these classes I had my assignment 6 code pulled up and would copy
# the code over and then modify it to work in python. I then implemented
# the collision detection and correction. Implementing the collioson
# correction took the longest because there was a lot of code to change
# including changning this to self, and from camel case to snake case.
# I had trouble getting the images to load at first, but I figured it out
# using pygame to load and scale the images

# Date: May 1st, 2025


import pygame
import time
import json
import math

from pygame.locals import*
from time import sleep

# Constants
WORLD_W = 4000 # width of the world
WORLD_H = 600 # height of the world
SCREEN_W = 600 # width of the screen
SCREEN_H = 600 # height of the screen
GROUND_H = 550 # height of the ground


class Sprite():
    COLLAPSE_TIME = 80 # TIME ELAPSED AS COLLAPSED

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.direction = 1
        self.lastX = x
        self.lastY = y
        self.speed = 1

        self.collapsed = False
        self.removed = False
        self.num_frames_in_air = 0
        self.collapse_timer = 0
        self.vert_velocity = 0.0
        
    def get_x(self):
        return self.x
        
    def get_y(self):
        return self.y
        
    def get_w(self):
        return self.w

    def get_h(self):
        return self.h
    
    def set_x(self, x):
        self.x = x
    
    def set_y(self, y):
        self.y = y
    
    def set_w(self, w):
        self.w = w
    
    def set_h(self, h):
        self.h = h
    
    def get_left(self):
        return self.x
    
    def get_right(self):
        return self.x + self.w
    
    def get_top(self):
        return self.y
    
    def get_bottom(self):
        return self.y + self.h
    
    def is_brick(self):
        return False
    
    def is_luigi(self):
        return False
    
    def is_goomba(self):
        return False
    
    def is_fireball(self):
        return False
    
    def is_mushroom(self):
        return False
    
    def is_drybones(self):
        return False
    
    def get_last_x(self):
        return self.last_x
    
    def get_last_y(self):
        return self.last_y

    def set_last_x(self, x):
        self.last_x = x
    
    def set_last_y(self, y):
        self.last_y = y
    
    def set_last_xy(self):
        self.last_x = self.x
        self.last_y = self.y
    
    def reset_frames_in_air(self):
        self.num_frames_in_air = 0
    
    def reset_vert_velocity(self):
        self.vert_velocity = 0.0
    
    def set_collapsed(self, collapsed):
        self.collapsed = collapsed
    
    def get_collapsed(self):
        return self.collapsed
    
    def collision_detection(self, sprite):
        if (self.get_right() <= sprite.get_left()):
            return False
        if (self.get_left() >= sprite.get_right()):
            return False
        if (self.get_bottom() <= sprite.get_top()):
            return False
        if (self.get_top() >= sprite.get_bottom()):
            return False

        return True
    
    def remove(self):
        self.removed = True
    
    def is_removed(self):
        return self.removed
    
    def flip_direction(self):
        self.direction *= -1
    
    def set_direction(self, direction):
        self.direction = direction
    
    def get_direction(self):
        return self.direction

    def marshal(self):
        print("marshal() needs to be implemented")

    def draw(self, view):
        print("draw() needs to be implemented")

    def update(self):
        print("update() needs to be implemented")

class Model():
    def __init__(self):
        self.sprites = []
        self.items_i_can_add = [Brick(0, 0), Mushroom(0, 0), Drybones(0, 0), Goomba(0, 0)]
        self.luigi = Luigi(100, 100)
        self.sprites.append(self.luigi)
        self.item_num = 0
        self.screen_x = 0
        
        #open the json map and pull out the individual lists of sprite objects
        with open("map.json") as file:
            data = json.load(file)
            self.load_map(data)
        file.close()

    def get_sprites(self):
        return self.sprites
    
    def marshal(self):
        # first we need to setup our list of objects to be saved
        data = { "bricks": [], "mushrooms": [], "drybones": [], "goombas": [], }
        for s in self.sprites:
            if s.is_brick():
                data["bricks"].append(s.marshal())
            elif s.is_mushroom():
                data["mushrooms"].append(s.marshal())
            elif s.is_drybones():
                data["drybones"].append(s.marshal())
            elif s.is_goomba():
                data["goombas"].append(s.marshal())
        return data
    
    def load_map(self, map):
        # clear the current list of sprites except luigi
        self.sprites = [self.luigi]
        # load the map data into the model
        for b in map.get("bricks", []):
            x = math.floor(b["x"] / 50) * 50
            y = math.floor(b["y"] / 50) * 50
            self.sprites.append(Brick(x, y))
        for m in map.get("mushrooms", []):
            self.sprites.append(Mushroom(m["x"], m["y"]))
        for d in map.get("drybones", []):
            self.sprites.append(Drybones(d["x"], d["y"]))
        for g in map.get("goombas", []):
            self.sprites.append(Goomba(g["x"], g["y"]))

    def increment_item_num(self):
        self.item_num += 1
        if (self.item_num >= len(self.items_i_can_add)):
            self.item_num = 0

    def get_luigi(self):
        return self.luigi
    
    def get_item_num(self):
        return self.item_num
    
    def add_sprite(self, x, y):
        placeable = self.items_i_can_add[self.get_item_num()]
        if (placeable.is_brick()):
            x = math.floor(x / 50) * 50 # this snaps to a 50x50 so that they arent just spawned anywhere
            y = math.floor(y / 50) * 50 # may make this logic only follow if it is a brick
            # now I want to make sure that bricks arent place in or under the ground
            if (y + 50 > GROUND_H):
                return
        for s in self.sprites:
            if (s.get_x() == x and s.get_y() == y):
                return
        if (placeable.is_brick()):
            self.sprites.append(Brick(x, y))
        elif (placeable.is_mushroom()):
            self.sprites.append(Mushroom(x, y))
        elif (placeable.is_drybones()):
            self.sprites.append(Drybones(x, y))
        elif (placeable.is_goomba()):
            self.sprites.append(Goomba(x, y))
 
    def remove_sprite(self, x, y):
        placeable = self.items_i_can_add[self.get_item_num()]
        for s in self.sprites:
            mouse_on_sprite = x >= s.get_x() and x <= s.get_x() + s.get_w() and y >= s.get_y() and y <= s.get_y() + s.get_h()
            if (mouse_on_sprite):
                if (placeable.is_brick() and s.is_brick()):
                    self.sprites.remove(s)
                    return
                elif (placeable.is_mushroom() and s.is_mushroom()):
                    self.sprites.remove(s)
                    return
                elif (placeable.is_drybones() and s.is_drybones()):
                    self.sprites.remove(s)
                    return
                elif (placeable.is_goomba() and s.is_goomba()):
                    self.sprites.remove(s)
                    return

    def set_screen_x(self, position):
        if (position < 0): #invalid
            self.screen_x = 0 #set valid
        elif (position > WORLD_W - SCREEN_W): # if off map
            self.screen_x = WORLD_W - SCREEN_W
        else:     # if not invalid, (valid), keep position
            self.screen_x = position

    def get_screen_x(self):
        return self.screen_x
    
    def move_luigi(self, direction):
        if (direction > 0):
            self.luigi.move_right()
            self.luigi.set_moving(True)
        elif (direction < 0):
            self.luigi.move_left()
            self.luigi.set_moving(True)

    def set_moving(self, moving):
        self.luigi.set_moving(moving)
        
    def jump_luigi(self):
        self.luigi.jump_up()

    def throw_fireball(self):
        fireball_direction = self.luigi.get_direction()
        fireball = self.luigi.throw_fireball(fireball_direction)
        self.sprites.append(fireball)
        # collision correction generalized for any sprites!

    def collision_correction(self):
        for s1 in self.sprites: # loop1 to setup comparison for our new general purpose collisons
            for s2 in self.sprites: # loop2 for comparison with loop1's sprites
                if (s1 == s2): #brick runs into brick?????????????? 
                    continue # skip self if a sprite collides with itself (because that's not possible)
                if (s1.collision_detection(s2)):  #if a collision between any two sprites is detected
                    if (s1.is_luigi() and s2.is_brick()): #luigi and brick interaction 
                        #Luigi runs into and stops movement against bricks. Bricks exist
                        collide_right = (s1.get_x() + s1.get_w()) - s2.get_left() 
                        collide_left = s2.get_right() - s1.get_x()
    
                        if (s1.get_last_y() + s1.get_h() <= s2.get_top()): #lugi comes from above
                            #System.out.println("Collision (above): " + luigi.toString() + " with " + s.toString());
                            s1.set_y(s2.get_top() - s1.get_h());
                            s1.reset_vert_velocity()
                            s1.reset_frames_in_air()
                        elif (s1.get_last_y() >= s2.get_bottom()):  #luigi comes from below
                            #System.out.println("Collision (below): " + luigi.toString() + " with " + s.toString());
                            s1.set_y(s2.get_bottom())
                            s1.reset_vert_velocity()
                            s1.reset_frames_in_air()
                        elif (collide_right > 0 and collide_right < collide_left): #luigi comes from righ
                            #System.out.println("Collision (left): " + luigi.toString() + " with " + brick.toString());
                            s1.set_x(s2.get_left() - s1.get_w())
                        elif (collide_left > 0 and collide_left < collide_right):
                            #System.out.println("Collision (right): " + luigi.toString() + " with " + brick.toString());
                            s1.set_x(s2.get_right());
                    if(s1.is_luigi() and s2.is_drybones()): #if luigi and drybones interact
                        #Luigi runs into Dry Bones and it does not affect his movement. The Dry Bones should 
                        #collapse to a pile of bones, wait for a period of time, then reanimate and continue walking.
                        s2.set_collapsed(True)
                    if (s1.is_luigi() and s2.is_mushroom()): #if luigi and mushroom interact
                        #Luigi runs into a mushroom and changes size, no collision fixing. Mushroom gets 
                        #eaten and is removed from Sprites. 
                        s1.set_big(not s1.get_big())
                        s2.remove();        
                    if (s1.is_drybones() and s2.is_brick()): #if drybones and brick interact
                        #Dry Bones gets out of the brick and reverses direction. Brick exists
                        collide_right = (s1.get_x() + s1.get_w()) - s2.get_left(); 
                        collide_left = s2.get_right() - s1.get_x();

                        if (s1.get_last_y() + s1.get_h() <= s2.get_top()):
                            s1.set_y(s2.get_top() - s1.get_h());
                            s1.reset_vert_velocity();
                        elif (s1.get_last_y() >= s2.get_bottom()):
                            s1.set_y(s2.get_bottom())
                            s1.reset_vert_velocity()
                        elif (collide_right > 0 and collide_right < collide_left):
                            s1.set_x(s2.get_left() - s1.get_w())
                            s1.flip_direction()
                            #System.out.println("Collision (left): " + drybones.toString() + " with " + brick.toString());
                        elif (collide_left > 0 and collide_left < collide_right):
                            s1.set_x(s2.get_right())
                            s1.flip_direction()
                            #System.out.println("Collision (right): " + drybones.toString() + " with " + brick.toString());
                            #move drybones to the right or left based on his last collision with a brick by 3 units
                    if (s1.is_goomba() and s2.is_brick()): #if goomba and brick interact
                        #Goomba gets out of the brick and reverses direction. Brick exists.
                        collide_right = (s1.get_x() + s1.get_w()) - s2.get_left()
                        collide_left = s1.get_right() - s1.get_x()

                        if (s1.get_last_y() + s1.get_h() <= s2.get_top()): 
                            s1.set_y(s2.get_top() - s1.get_h());
                            s1.reset_vert_velocity();

                        elif (s1.get_last_y() >= s2.get_bottom()):
                            s1.set_y(s2.get_bottom());
                            s1.reset_vert_velocity();
                        elif (collide_right > 0 and collide_right < collide_left):
                            s1.set_x(s2.get_left() - s1.get_w());
                            s1.flip_direction();
                            #System.out.println("Collision (left): " + goomba.toString() + " with " + brick.toString());
                        elif (collide_left > 0 and collide_left < collide_right):
                            s1.set_x(s2.get_right());
                            s1.flip_direction();
                            #System.out.println("Collision (right): " + goomba.toString() + " with " + brick.toString());
                    if (s1.is_mushroom() and s2.is_brick()): #if mushroom and brick interact
                        #Mushroom can sit on top of a Brick (collision fixing in the y-direction). Brick exists.
                        collide_right = (s1.get_x() + s1.get_w()) - s2.get_left(); 
                        collide_left = s2.get_right() - s1.get_x();

                        if (s1.get_last_y() + s1.get_h() <= s2.get_top()):
                            s1.set_y(s2.get_top() - s1.get_h());
                            s1.reset_vert_velocity();
                            s1.reset_frames_in_air()
                        elif (s1.get_last_y() >= s2.get_bottom()):
                            s1.set_y(s2.get_bottom())
                            s1.reset_vert_velocity()
                            s1.reset_frames_in_air()
                        elif (collide_right > 0 and collide_right < collide_left):
                            s1.set_x(s2.get_left() - s1.get_w())
                            s1.flip_direction()
                            #System.out.println("Collision (left): " + mushroom.toString() + " with " + brick.toString());
                        elif (collide_left > 0 and collide_left < collide_right):
                            s1.set_x(s2.get_right())
                            s1.flip_direction()
                            #System.out.println("Collision (right): " + mushroom.toString() + " with " + brick.toString());
                    if (s1.is_drybones() and s2.is_fireball()):
                        #Fireball runs into Dry Bones and is consumed (removed from Sprites). The Dry Bones 
                        #should collapse to a pile of bones, wait for a period of time, then reanimate and 
                        #continue walking
                        if (not s1.get_collapsed()):
                            s1.set_collapsed(True)
                            s2.remove()
                    if (s1.is_goomba() and s2.is_fireball()):
                        #Fireball runs into Goomba and is consumed (removed from Sprites). The Goomba is set
                        #on fire, stops moving, burns for a few frames, then is removed from Sprites
                        if (not s1.get_collapsed()):
                            s1.set_collapsed(True)
                            s2.remove()

    def update(self):
        for sprite in self.sprites:
            sprite.update()
        self.collision_correction()
        for sprite in self.sprites:
            if (sprite.is_luigi()):
                self.set_screen_x(self.luigi.get_x() - SCREEN_W / 2)
        for sprite in self.sprites:
            if (sprite.is_removed()):
                self.sprites.remove(sprite)
                print("Removed sprite: " + str(sprite))


    
class View():
    def __init__(self, model):
        screen_size = (800,600)
        self.screen = pygame.display.set_mode(screen_size, 32)
        self.model = model
        self.ground_image = pygame.image.load("images/ground.png")

    def update(self):
        self.screen.fill([50,50,50]) # dark gray background
        
        # now we gotta draw the ground and have it spaced out covering the whole screen
        for i in range(0, WORLD_W, self.ground_image.get_width()):
            self.screen.blit(self.ground_image, (i - self.model.get_screen_x(), GROUND_H))
        # now draw each sprite
        for sprite in self.model.sprites:
            sprite.draw(self)
        # lastly we will implement the edit mode
        if (Controller.get_edit_mode()):
            # edit indicator, change color based on add mode on / off
            if (Controller.get_add_mode()):
                color = [0, 255, 0] # green
            else:
                color = [255, 0, 0] # red
            pygame.draw.rect(self.screen, color, (0, 0, 200, 200))
            # now we have to draw the current item to be placed
            item_num = self.model.get_item_num()
            match item_num:
                case 0:
                    # draw brick
                    self.screen.blit(pygame.transform.scale(Brick.brick_image, (160, 160)), (20, 20))
                case 1:
                    # draw mushroom
                    self.screen.blit(pygame.transform.scale(Mushroom.mushroom_images[0], (160, 160)), (20, 20))
                case 2:
                    # draw drybones
                    self.screen.blit(pygame.transform.scale(Drybones.drybones_images[0], (160, 160)), (20, 20))
                case 3:
                    # draw goomba
                    self.screen.blit(pygame.transform.scale(Goomba.goomba_images[0], (160, 160)), (20, 20))

        pygame.display.flip()

class Controller():
    edit_mode = False
    add_mode = True

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.keep_going = True
        self.key_left = False
        self.key_right = False
        self.key_space = False
        self.key_down = False
    
    @staticmethod
    def get_edit_mode():
        return Controller.edit_mode
    
    @staticmethod
    def get_add_mode():
        return Controller.add_mode

    def update(self):
         # first check for keys being held down 
    
        if (self.key_right):
            self.model.move_luigi(25)
        if (self.key_left):
            self.model.move_luigi(-25)
        if (self.key_space):
            self.model.jump_luigi()
        if (self.key_down):
            self.model.throw_fireball()

         # then check for keys being pressed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_going = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_going = False
                elif event.key == pygame.K_a:
                    self.key_left = True
                    self.model.set_moving(True)
                elif event.key == pygame.K_d:
                    self.key_right = True
                    self.model.set_moving(True)
                elif event.key == pygame.K_w:
                    self.key_space = True
                elif event.key == pygame.K_s:
                    self.key_down = True

            elif event.type == pygame.KEYUP: #this is keyReleased!
                match event.key:
                    case pygame.K_a:
                        self.key_left = False
                        self.model.set_moving(False)
                    case pygame.K_d:
                        self.key_right = False
                        self.model.set_moving(False)
                    case pygame.K_w:
                        self.key_space = False
                    case pygame.K_ESCAPE:
                        self.keep_going = False
                    case pygame.K_s:
                        self.key_down = False
                    case pygame.K_e:
                        Controller.edit_mode = not Controller.edit_mode
                        if Controller.edit_mode:
                            Controller.add_mode = True
                    case pygame.K_q:
                        Controller.add_mode = True
                    case pygame.K_r:
                        Controller.add_mode = False
                    case pygame.K_k:
                        #save the map to a json file 
                        with open("map.json", "w") as file:
                            json.dump(self.model.marshal(), file, indent=4)
                            file.close()
                    case pygame.K_l:
                        #load the map from a json file
                        if Controller.edit_mode:
                            with open("map.json") as file:
                                data = json.load(file)
                                self.model.load_map(data)
                                file.close()
                    case pygame.K_c:
                        #clear the map
                        if Controller.edit_mode:
                            new_sprites = []
                            for sprite in self.model.get_sprites():
                                if (sprite.is_luigi()):
                                    new_sprites.append(sprite)
                            self.model.sprites = new_sprites

            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # fetches the position for mouse click
                # gets relative position to the screen
                world_x = mouse_x + self.model.get_screen_x()
                if Controller.edit_mode:
                    if (mouse_x < 200 and mouse_y < 200):
                        # if the mouse is in the edit mode area, do nothing
                        self.model.increment_item_num()
                    elif (Controller.add_mode):
                        # if we are in add mode, add a sprite
                        if not (mouse_x < 200 and mouse_y < 200):
                            # if the mouse is outside the edit mode area, add a sprite
                            self.model.add_sprite(world_x, mouse_y)
                    else:
                        # if we are in remove mode, remove a sprite
                        self.model.remove_sprite(world_x, mouse_y)


class Luigi(Sprite):
    luigi_images = [] # array of images of luigi for animation
    def __init__(self, x, y):
        super().__init__(x, y, 50, 50)
        self.w = 40
        self.h = 70
        self.num_frames_in_air = 0
        self.image_num = 0
        self.image_delay = 0
        self.image_max_delay = 2
        self.moving = False
        self.speed = 12
        self.direction = 1
        self.jump_height = 0
        self.jump_speed = 10
        self.is_big = False
        # now load images for luigi
        if len(self.luigi_images) == 0: #if lloading images hasnt occured yet
            self.luigi_images.append(pygame.image.load("images/luigi1.png"))
            self.luigi_images.append(pygame.image.load("images/luigi2.png"))
            self.luigi_images.append(pygame.image.load("images/luigi3.png"))
            self.luigi_images.append(pygame.image.load("images/luigi4.png"))
            self.luigi_images.append(pygame.image.load("images/luigi5.png"))

        self.image = Luigi.luigi_images[0] # default image


    def is_luigi(self):
        return True
    
    def set_big(self, big):
        self.is_big = big
    
    def get_big(self):
        return self.is_big

    def set_moving(self, moving):
        self.moving = moving
    
    def get_moving(self):
        return self.moving

    def move_left(self):
        self.set_last_xy()
        self.direction = -1
        #if (self.sprinting):
        #    self.set_x(self.get_x() - self.sprinting_speed)
        self.set_x(self.get_x() - self.speed)
        self.set_moving(True)

    def move_right(self):
        self.set_last_xy()
        self.direction = 1
        #if (self.sprinting):
        #    self.set_x(self.get_x + self.sprinting_speed)
        self.set_x(self.get_x() + self.speed)
        self.set_moving(True)

    def jump_up(self):
        if (self.num_frames_in_air < 5): # only jump if not in the air already
            self.vert_velocity -= 5
            self.num_frames_in_air += 1

    def throw_fireball(self, direction):
        fireball_x = self.x + (self.w / 2)
        fireball_y = self.y + (self.h / 2)
        return Fireball(fireball_x, fireball_y, direction)        

    def animation_helper(self):
        if (self.moving):
            self.image_delay += 1
            if (self.image_delay >= self.image_max_delay):
                self.image_num += 1
                if (self.image_num >= len(self.luigi_images)):
                    self.image_num = 0
                self.image_delay = 0
        else:
            self.image_num = 0
 
    def draw(self, view):
        # now we need to draw luigi
        view.screen.blit(self.image, (self.x - view.model.get_screen_x(), self.y))
        self.animation_helper()
        if (self.moving): #moving
            if (self.direction == 1): # right
                self.image = pygame.transform.scale(self.luigi_images[self.image_num], (self.w, self.h))
            else: # left
                self.image = pygame.transform.flip(pygame.transform.scale(self.luigi_images[self.image_num], (self.w, self.h)), True, False)
        else: # standing still
            if (self.direction == 1): # right
                self.image = pygame.transform.scale(self.luigi_images[self.image_num], (self.w, self.h))
            else: # left
                self.image = pygame.transform.flip(pygame.transform.scale(self.luigi_images[self.image_num], (self.w, self.h)), True, False)

    def update(self):
        self.set_last_xy()
        self.vert_velocity += 1.2 # gravity
        self.y += self.vert_velocity # apply gravity
        # check if luigi is big, if so increase size if not normal size
        if (self.is_big): #big
            self.h = 90
            self.w = 60
        else: #normal
            self.h = 70
            self.w = 40
        # now we need to snap luigi to the ground while he is on it
        if (self.y + self.h >= GROUND_H):
            self.y = GROUND_H - self.h
            self.reset_frames_in_air()
            self.reset_vert_velocity()
        # now if luigi is walking outside the world on the left 
        if (self.x < 0):
            self.x = 0
        # if luigi is walking outside the world on the right
        if (self.x + self.w > WORLD_W):
            self.x = WORLD_W - self.w
        

class Brick(Sprite):
    brick_image = pygame.transform.scale(pygame.image.load("images/brick.png"), (50, 50))
    def __init__(self, x, y):
        super().__init__(x, y, 50, 50)
        self.image = Brick.brick_image # default image

    def is_brick(self):
        return True
    
    def marshal(self):
        return { "x": self.x, "y": self.y }
    
    def to_string(self):
        return "Brick: " + str(self.x) + ", " + str(self.y)

    def draw(self, view):
        view.screen.blit(self.image, (self.x - view.model.get_screen_x(), self.y))
        
    def update(self):
        pass


class Mushroom(Sprite):
    mushroom_images = []

    def __init__(self, x, y):
        super().__init__(x, y, 50, 50)
        if len(Mushroom.mushroom_images) == 0:
            Mushroom.mushroom_images.append(pygame.image.load("images/mushroom.png"))
        self.image = pygame.transform.scale(Mushroom.mushroom_images[0], (self.w, self.h))

    def is_mushroom(self):
        return True
    
    def marshal(self):
        return { "x": self.x, "y": self.y }
    
    def to_string(self):
        return "Mushroom: " + str(self.x) + ", " + str(self.y)

    def draw(self, view):
        view.screen.blit(self.image, (self.x - view.model.get_screen_x(), self.y))

    def update(self):
        self.set_last_xy()
        self.vert_velocity += 1.2 # gravity
        self.y += self.vert_velocity # apply gravity
        # now we need to snap the mushroom to the ground while he is on it
        if (self.y + self.h >= GROUND_H):
            self.y = GROUND_H - self.h
            self.reset_vert_velocity()


class Drybones(Sprite):
    drybones_images = []
    def __init__(self, x, y):
        super().__init__(x, y, 50, 50)
        self.direction = 1
        self.speed = 6
        self.frame = 0
        self.animation_timer = 0

        if len(Drybones.drybones_images) == 0: #if lloading images hasnt occured yet
            Drybones.drybones_images.append(pygame.image.load("images/drybones1.png"))
            Drybones.drybones_images.append(pygame.image.load("images/drybones2.png"))
            Drybones.drybones_images.append(pygame.image.load("images/drybones3.png"))
            Drybones.drybones_images.append(pygame.image.load("images/drybones4.png"))
            Drybones.drybones_images.append(pygame.image.load("images/drybones5.png"))
            Drybones.drybones_images.append(pygame.image.load("images/drybones6.png"))
            Drybones.drybones_images.append(pygame.image.load("images/drybones7.png"))
            Drybones.drybones_images.append(pygame.image.load("images/drybones8.png"))
            Drybones.drybones_images.append(pygame.image.load("images/drybones9.png"))
            Drybones.drybones_images.append(pygame.image.load("images/drybones10.png"))
            Drybones.drybones_images.append(pygame.image.load("images/drybones11.png")) # on ground / collapsed

        self.image = pygame.transform.scale(Drybones.drybones_images[0], (50, 50)) # default image

    def is_drybones(self):
        return True

    def to_string(self):
        return "Drybones: " + str(self.x) + ", " + str(self.y)
    
    def marshal(self):
        return { "x": self.x, "y": self.y }

    def draw(self, view):
        # now we need to draw drybones
        view.screen.blit(self.image, (self.x - view.model.get_screen_x(), self.y))
        if (self.collapsed): #if drybones is collapsed from fireball
            self.image = pygame.transform.scale(self.drybones_images[10], (50, 50)) #draw the collapsed image
        else: #not collapsed, so just walking
            if (self.direction == -1): #if drybones goes left, it flips his image to the left as well as fixing the offset
                self.image = pygame.transform.scale(self.drybones_images[self.frame], (50, 50))
            else:
                self.image = pygame.transform.flip(pygame.transform.scale(self.drybones_images[self.frame], (50, 50)), True, False)
                

    def update(self):
        # if drybones is removed, do nothing
        if (self.is_removed()):
            return;
    
        # if drybones is not removed, we need to update his position and animation
        if (self.collapsed): #if drybones is collapsed
            self.collapse_timer += 1 #increment the timer
            if (self.collapse_timer >= Sprite.COLLAPSE_TIME): #if time waiting collapsed is done
                self.collapsed = False; #drybones is no longer collapsed
                self.collapse_timer = 0; #reset timer
            return;
    
        # if drybones is not collapsed, we need to update his animation
        self.animation_timer += 1 #incremement per itteraiton
        if (self.animation_timer >= 6): #if time for animation is done
            self.frame += 1 #move to next frame
            if (self.frame > 9): #if at the end of the animation
                self.frame = 0 #reset to the beginning
            self.animation_timer = 0; #reset timer for nect itteration
        
        #now to make our drybones move either left or right
        self.set_last_xy()
        self.x += self.direction * 2; #move drybones to the right or left based on his last collision with a brick by 3 units
        self.vert_velocity += 1.2 #gravity
        self.y += self.vert_velocity
        if(self.y + self.h >= GROUND_H): #if drybones is on the ground
            self.y = GROUND_H - self.h; # snap  to the ground
            self.vert_velocity = 0.0; #stop falling
        # now if drybones is walking outside the world on the left 
        if (self.x < 0):
            self.x = 0
            self.flip_direction() #drybones flips direction if he hits the wall

        # if drybones is walking outside the world on the right
        if (self.x + self.w > WORLD_W):
            self.x = WORLD_W - self.w
            self.flip_direction() #drybones flips direction if he hits the wall




class Goomba(Sprite):
    goomba_images = []
    def __init__(self, x, y):
        super().__init__(x, y, 50, 50)
        self.direction = 1
        self.speed = 1
        if len(self.goomba_images) == 0:
            self.goomba_images.append(pygame.image.load("images/goomba.png"))
            self.goomba_images.append(pygame.image.load("images/goomba_fire.png"))
        self.image = pygame.transform.scale(self.goomba_images[0], (50, 50))


    def is_goomba(self):
        return True
    
    def to_string(self):
        return "Goomba: " + str(self.x) + ", " + str(self.y)
    
    def marshal(self):
        return { "x": self.x, "y": self.y }

    def draw(self, view):
        # now we need to draw goomba
        view.screen.blit(self.image, (self.x - view.model.get_screen_x(), self.y))
        if (self.collapsed):
            self.image = pygame.transform.scale(self.goomba_images[1], (50, 50))
        else:
            if(self.direction == 1):
                self.image = pygame.transform.flip(pygame.transform.scale(self.goomba_images[0], (50, 50)), True, False)
            else:
                self.image = pygame.transform.scale(self.goomba_images[0], (50, 50))

    def update(self):
        if (self.is_removed()):
            return
        if (self.collapsed): #//if goomba is collapsed
            self.collapse_timer += 1 #incrementing timer
            if (self.collapse_timer >= Sprite.COLLAPSE_TIME): #if time waiting is done
                self.remove() #remove goomba from the game
            return;
        #now to make our drybones move either left or right
        self.set_last_xy()
        self.x += self.direction * 3; #move goomba to the right or left based on his last collision with a brick by 3 units
        self.vert_velocity += 1.2; #gravity
        self.y += self.vert_velocity; #apply gravity

        if(self.y + self.h >= GROUND_H): #if goomba is on the ground
            self.y = GROUND_H - self.h; # snap  to the ground
            self.vert_velocity = 0.0; #stop falling
        # now if goomba is walking outside the world on the left 
        if (self.x < 0):
            self.x = 0
            self.flip_direction() #goomba flips direction if he hits the wall
        # if goomba is walking outside the world on the right
        if (self.x + self.w > WORLD_W):
            self.x = WORLD_W - self.w
            self.flip_direction() #goomba flips direction if he hits the wall

class Fireball(Sprite):
    fireball_images = []
    def __init__(self, x, y, direction):
        super().__init__(x, y, 25, 25)
        self.direction = direction
        self.speed = 15
        if len(Fireball.fireball_images) == 0:
            Fireball.fireball_images.append(pygame.image.load("images/fireball.png"))
        self.image = pygame.transform.scale(Fireball.fireball_images[0], (25, 25))

    def draw(self, view):
        if (self.direction == -1): #if facing left direction
            view.screen.blit(pygame.transform.flip(self.image, True, False), (self.x - view.model.get_screen_x(), self.y))
        else:  #if facing right direction
            view.screen.blit(self.image, (self.x - view.model.get_screen_x(), self.y))
            
    def is_fireball(self):
        return True
    
    def to_string(self):
        return "Fireball: " + str(self.x) + ", " + str(self.y)

    def update(self):
        self.set_last_xy()
        self.vert_velocity += 1.2 #gravity
        self.y += self.vert_velocity
        self.x += self.speed * self.direction
        if (self.y + self.h >= GROUND_H): #if fireball is on the ground
            self.y = GROUND_H - self.h; # snap  to the ground
            self.vert_velocity = -15 #now to launch off the ground
        if (self.x > WORLD_W or self.x < 0): #remove fireball if gone off the screen to save memory
            self.remove();


print("Use the arrow keys to move. Press Esc to quit.")
pygame.init()
m = Model()
v = View(m)
c = Controller(m, v)
while c.keep_going:
    c.update()
    m.update()
    v.update()
    sleep(0.04)
print("Goodbye")