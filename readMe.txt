CNG 462 - Artificial Intelligence - Assignment 1
Berke Diler - 2401503
Bedirhan Ozkan - 2453470
-Program Description-
This program implements the A* search algorithm to find the shortest path between points on a map.
The map and the points (nodes) are defined in separate files.
The program also includes Depth First Search and Uniform Cost Search algorithms for traversing a graph created from the distances between nodes calculated using A*.
There are two .txt files that are necessary for the program to run, nodes.txt and map.txt, format to these are given below. The path to these files should be given in the code.

-File Formats-

nodes.txt: Defines the locations with their names and map coordinates.

Format: Name,X,Y
Example:
A,8,2
B,1,3
C,3,7
D,8,7

map.txt: Represents the map where 1 indicates a block area and 0 indicates an free to move area.

Format: 1 for obstacle, 0 for passable, separated by commas, the map should be surrounded by 1s in order to work properly.
Example map:
1,1,1,1,1,1,1,1,1
1,1,1,0,0,0,0,0,1
1,0,0,0,0,0,1,1,1
1,0,1,1,1,0,0,0,1
1,0,0,0,0,0,1,0,1
1,0,0,1,1,0,1,0,1
1,1,0,1,0,0,1,0,1
1,1,0,1,0,1,1,0,1
1,0,0,0,0,0,0,0,1
1,1,1,1,1,1,1,1,1

-How to Compile and Run-

Only following the necessary formats for the files, the program can be compiled and run using the command line terminal with Python 3.11

The program may cause error if any unexpected prompt to the menu is given, so it is recommended to follow the instructions given by the program.