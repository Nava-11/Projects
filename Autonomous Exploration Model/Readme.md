This Python script is designed to simulate a rover's autonomous navigation in a grid environment using Q-learning. The rover is trained to move from a start point to a goal while avoiding obstacles. The main components of the script are:

1. **Grid Setup**: A 30x30 grid is created, with random obstacles placed.
2. **Q-learning**: The rover learns the optimal path to the goal through exploration and exploitation, adjusting its movement based on rewards and penalties.
3. **Testing & Backtracking**: Once trained, the rover is tested in a new grid. If it encounters dead ends, it backtracks to find an alternative path.
4. **Visualization**: The grid and the rover’s path are visualized using Matplotlib.

This project demonstrates the application of reinforcement learning for autonomous exploration and pathfinding, suitable for robotics or AI-driven navigation systems.


![image](https://github.com/user-attachments/assets/82177d85-c380-4a9d-9d95-6105a5ada2cd)
