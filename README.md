# Maze Explorer Game


## Student Questions

### Question 1 (10 points)
Explain how the automated maze explorer works.

**1.1. The algorithm used by the explorer** 

The explorer solves the maze using the Right-Hand Rule algorithm, which will prioritize turning right at first, then forward, and then left. The algorithm operates in the following order: 
- The explorer turns to the right using the "turn_right()" method and then tries to move forward.
- It then calls the "can_move_forward()" method to check whether it can move forward in this direction. 
- If it returns true, then it will move forward and add the current position (x and y coordinates) to the visited positions set. 
- If the "can_move_forward()" method returns false, that means it is a blocked way (is facing a wall), therefore, it will face forward again (technically left) and tries again. 
- If the forward side is blocked as well, it will turn to the left and again try moving forward. 
- If it is blocked as well, the explorer will turn to the left this time facing backward from the perspective of the first direction, and moves in that direction.

**1.2. How it handles getting stuck in loops** 

To prevent getting stuck in loops, the explorer uses a deque "move_history" containing the last 3 positions visited and the "is_stuck()" method. 
- The method will check if the "moves_history" deque contains less that three values.
- If yes the function will return "False" indicating the explorer is not stuck in a loop.
- Otherwise, it will return "True" if all three values (moves) are the same, and "False" if they are not.

**1.3. The backtracking strategy it employs**

If the explorer finds itself stuck it will try backtracking using "self.backtrack()", which will take the following steps: 
- Check if there is a backtrack path using the "backtrack_path" attribute. If the "backtrack_path" list is empty, it will call the "find_backtrack_path()" method, which will:
   - First add the current position to the "visited" set.
   - Then it will iterate over the positions in the "self.moves" list, and add the visited node to the "path" list.
   - It will then return the list of reversed path to the "backtrack()" method as a backtrack_path. 
- The "backtrack()" method will recieve the list and for each position, it will count the number of cells adjacent to it that are not walls, and thats by checking the "self.count_available_choices()" for the current position.
- for each iteration the function will increment the "self.backtrack_count" and visualize the taken step.
- When the explorer finds a cell connected to a path that has not yet been explored, it will then stop backtracking and start exploring this path. 

**1.4. The statistics it provides at the end of exploration**

When the explorer reaches the end point, the "print_statistics()" method is called to display detailed performance statistics inclusing: 
- The time it took the explorer to solve the maze (by subtracting the start_time from the end_time).
- The total number of moves (using "len(self.moves)").
- The amount of times the explorer backtracked (from the "self.backtrack_count" variable).
- The average number of moves per second (by dividing the number of moves by the time it took to find the goal).


### Question 2 (30 points)
Modify the main program to run multiple maze explorers simultaneously. This is because we want to find the best route out of the maze. Your solution should:
1. Allow running multiple explorers in parallel
2. Collect and compare statistics from all explorers
3. Display a summary of results showing which explorer performed best

I used Celery with Redis as a broker and backend to run tasks in parallel. Each explorer ran separately and returned its results to the main function where it will be analyzed and displayed. Using Celery will allow us to offload heavy computation like maze solving to background workers, which can run on multiple machines or processes.

Parallel Exploration Steps: 
- First, I created a Celery worker in the tasks.py file. This worker will recieve a maze-solving tasks and returns results.
- The main function will send 4 tasks to the Celery worker ("result = run_explorer_task.delay(strategy, type)"
- Tasks get executed concurrently on available worker processes.


### Question 3 (10 points)
Analyze and compare the performance of different maze explorers on the static maze. Your analysis should:

1. Run multiple explorers (at least 4 ) simultaneously on the static maze
2. Collect and compare the following metrics for each explorer:
   - Total time taken to solve the maze
   - Number of moves made
   - *Optional*:
     - Number of backtrack operations
3. What do you notice regarding the performance of the explorers? Explain the results and the observations you made.

After running 4 explorers simultaneously in the static mode,I found that:
- All explorers had the same moves count, which was 1279. 
- The time metric also had the same value for each explorer, likely due to fast execution and rounding. 
This indicates that the maze is static and deterministic, with the same solving strategy, number of explored nodes, etc. 


### Question 4 (20 points)
Based on your analysis from Question 3, propose and implement enhancements to the maze explorer to overcome its limitations. Your solution should:

1. Identify and explain the main limitations of the current explorer:

2. Propose specific improvements to the exploration algorithm:

3. Implement at least two of the proposed improvements:

Your answer should include:
4.1. A detailed explanation of the identified limitations
The current explorer uses the Right-Hand Rule strategy to explore and solve the maze, which might not be the best approach to solving a maze, and its limitations include: 
- Inefficient moves: The Right-Hand Rule does not consider the position of the goal or which path is the shortest, leading to unnecessary moves that will only increase the amount of time taken by the explorer and the number of moves.
- The Right-Hand Rule's strategy to avoid getting stuck in loops is simple and would not prevent getting stuck in circular paths. 
- Its approach does not consider any heuristics to prioritize one path over the other based on how likely it is to lead to the goal, and it spends time exploring irrelevent paths.
- The current explorer is not advanced enough to handle more complex maps and would require an excessive amount of time to explore a maze with a large number of possible paths.

4.2. Documentation of your proposed improvements
Some enhancements that could improve the explorer's performance are: 
- Using a search algorithm would enhance the performance alot since search algorithms are built to lead and improve search processes. A* for instance uses heuristic values to prioritize one path over the other, reducing the search space and time in larger or more complex mazes.
- Marking dead ends could help avoid or reduce unnecessary exploration and imrove the explorer's efficiency.
- Implementing a more advanced startegy to prevent getting stuck in loops. An example of this would be the BFS strategy approach of using a visited set to record all visited nodes which is much better in comparison to the Right-Hand Rule.


4.3. The modified code with clear comments explaining the changes
I added the BFSExplorer class in a new file "bfs_explorer.py" and integrated it in the main.py and tasks.py files. This approach will make the explorer find the shortest path and not only a random path.

### Question 5 (20 points)

Compare the performance of your enhanced explorer with the original:
   - Run both versions on the static maze
   - Collect and compare all relevant metrics
   - Create visualizations showing the improvements
   - Document the trade-offs of your enhancements
Your answer should include:
1. Performance comparison results and analysis
2. Discussion of any trade-offs or new limitations introduced

The BFS explorer was much better than the Right-Hand Rule explorer and have improved the model performance immediatly even before applying any more enhancements.

### Final points 6 (10 points)
1. Solve the static maze in 150 moves or less to get 10 points.
2. Solve the static maze in 135 moves or less to get 15 points.
3. Solve the static maze in 130 moves or less to get 100% in your assignment.

### Bonus points
1. Fastest solver to get top  10% routes (number of moves)
2. Finding a solution with no backtrack operations
3. Least number of moves.
