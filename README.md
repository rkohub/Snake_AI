# Snake_AI
I made a simulation of the common game snake and coded an AI to collect the pellets.

This program uses the Genetic Algorithm Style of AI to teach the snake to collect the food pellets through trial and error and darwinian evolution.

Each bot's mind is a collection of weights of edges for a neural network. The input/or senses being the distance in each of the 8 cardinal directions from the pellet, and the output being a direction in which to move

Then Each bot is shoved into the simulation and given a fitness score based on how far they move without hitting the wall or themselves and how many pellets they successfully collect

Then the next generation is created by taking copies of the best scorers from the previous generation as well as making new bots by combinding the brains of the top scorers and mutating them slightly

In the end I successfully got inteligent behavior of moving away from walls and towards pellets!!

Important Files
- GeneticAlgo.py
   - Where all the genetic breeding and mutating takes place
- RunSnake.py
   - THe Script that makes the visual, finds the senses and runs the bot
- MAIN.py
   - The 1 combinde file that combinds the previous 2 and runs the code generation by generation and prints informative output

- The rest of the files are testing or insignifigant


Addendum:
- My origional fitness function had no limit to how many points it gave to movement without colliding into walls or self, so the bots learned to move in infinite loops or circles. I would call this intellingent, but not intended, so I capped the fitness gained from moving at 1 point which is equivalent to 1 pellet collection.
