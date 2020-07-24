PAC MAN 3D 

Video Description: https://youtu.be/PM4WyIsWJ_8

Description: 	This game is Pac-Man, but in 3D. There are 2 modes: Play and Debug.
		Debug mode is a 2D view with of the model of the game. It allows
		for viusalization of the AI of the ghosts eaiser. Use arrow keys
		to play.

How to Run:	1. Run main.py, with ai.py, character.py, cmu_112_graphics.py, helper.py, and rayCast.py in the same folder
		2. Press [s] to play in Play modde. Press [d] to play in Debug mode.

Libraries: 	cmu_112_graphics.py

Debug Mode Legend:

[G] 		--> Ghosts

[T] 		--> Target Cell

[?] 		--> Possible cells for next move

[I] 		--> Intermediate Cell (Inky Only)

Red Line 	--> Blinky to Inky's Target Cell visualization

Orange Circle	--> Clyde's Zone visualization

Frightened Mode: Ghosts move in their direction until an intersection, then they choose a random direction and continue.
Scatter Mode: Ghosts each have a specific target cell off screen.
Chase Mode:

	Blinky(Red): 	Target cell is Pac Man's cell
		     	If <20 pellets left, Scatter Mode target cell is also Pac Man's cell

	Pinky(Pink): 	Target cell is 4 cells infront of Pacman (in the direction he is facing)
		     	Due to a bug in the orginal PacMan, when Pac Man is facing up, Pinky's target cell will be 4 up and 4 left of pacman

	Inky(Teal):  	Intermediate cell is 2 cells infront of Pac Man
		     	The intermediate cell is the midpoint between Inky's target cell and Blinky's occupied cell

	Clyde(Orange): 	If Clyde is outside an 8 tile circular radius centered at Pac Man
				Target cell is Pac Man's cell
			If Clide is inside this radius
				Target cell is Clyde's Scatter Mode target cell in the bototm left corner

*For more imformation on the AI of the ghosts, consult writeUp.txt in the folder Demo_for_tp2*


