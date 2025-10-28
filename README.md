# platform_game
This platform game was worked on throughout the Programming Paradigms course at the University of Arkansas. The implementation of this project demonstrates the usage of MVC architecture, game design, Polymorphism, object-oriented programming, and basic game physics and graphics.


Instructions:
------------------
Setup:
1) Install zip of project folder
2) Unzip project folder
3) Ensure python is installed on device
4) Run program using: python game.py in terminal
------------------
KeyBinds:
W: Traverse Vertically (jumps)
A: Traverse right
S: Throws fireball
D: Traverse left
E: Opens edit mode
Q: Enters add mode (within edit mode)
R: Enters remove mode (within edit mode)
ESCAPE: Closes application
------------------

Final Implementation Report:
Porting my project over from Java to Python has been fun and taught me a lot about programming in Python as well as the style of the language. The syntax is a bit more forgicing by not requiring semicolons or braces, but it means that as the programmer you need to pay extra attention to what you are doing. From translating it, I feel like I gained more knowledge of exactly how my code and classes interact with each other to make the game functional as a whole. Specifically in learning how to properly use the MVC or model, view, controller style of making a game. Converting most of my code was easy, involving a lot of adding “self” before variable usage to ensure we are in the right scope, rather than this in Java and JavaScript. I like the fact that you do not have to use semicolons in Python, but you still can, giving more choice to the user and their coding syntax. Rewriting the graphics was probably the most challenging part, just looking into what functions I needed to call to render and flip the images. In Java all you had to do was negate the width value while drawing to flip the image, but in Python, you used pygame.transform.flip() which was much easier than in Java and JavaScript. Making a constructor was weird because you used __init__ which I'm not certain on what this means. Another interesting thing about using Python was that in functions you need to pass self as a parameter to be able to make certain changes due to encapsulation.
