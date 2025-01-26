import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

# Parameters
ROWS, COLS = 30, 30  # Grid dimensions
EPISODES = 1000
ALPHA = 0.1  # Learning rate
GAMMA = 0.9  # Discount factor
EPSILON = 0.3  # Exploration rate (initial)
DECAY_RATE = 0.99  # Epsilon decay rate
ACTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Movement directions: Up, Down, Left, Right

# Create grid
def create_grid():
    return [[0 for _ in range(COLS)] for _ in range(ROWS)]

# Choose action based on epsilon-greedy policy
def choose_action(state, q_table):
    if np.random.uniform(0, 1) < EPSILON:
        return random.randint(0, len(ACTIONS) - 1)  # Explore
    else:
        return np.argmax(q_table[state])  # Exploit

# Train the rover using Q-learning
def train_rover(grid, start, goal):
    global EPSILON
    q_table = np.zeros((ROWS * COLS, len(ACTIONS)))
    for episode in range(EPISODES):
        state = start[0] * COLS + start[1]
        done = False
        while not done:
            action = choose_action(state, q_table)
            new_pos = (state // COLS + ACTIONS[action][0], state % COLS + ACTIONS[action][1])

            if 0 <= new_pos[0] < ROWS and 0 <= new_pos[1] < COLS:  # Check bounds
                if grid[new_pos[0]][new_pos[1]] == 0:  # Valid move
                    new_state = new_pos[0] * COLS + new_pos[1]
                    reward = 100 if new_pos == goal else -1  # Reward for reaching goal or moving
                    q_table[state, action] += ALPHA * (reward + GAMMA * np.max(q_table[new_state]) - q_table[state, action])
                    state = new_state
                    if new_pos == goal:
                        done = True
                else:  # Obstacle
                    reward = -100
                    q_table[state, action] += ALPHA * (reward - q_table[state, action])
            else:  # Out of bounds
                reward = -100
                q_table[state, action] += ALPHA * (reward - q_table[state, action])
        
        # Decay epsilon
        EPSILON = max(0.1, EPSILON * DECAY_RATE)
    return q_table

# Test the rover with backtracking
def test_rover(grid, start, goal, q_table):
    state = start[0] * COLS + start[1]
    path = [start]
    visited = set()
    rover_position = list(start)

    while tuple(rover_position) != goal:
        visited.add(tuple(rover_position))
        action = np.argmax(q_table[state])
        new_pos = (rover_position[0] + ACTIONS[action][0], rover_position[1] + ACTIONS[action][1])

        if 0 <= new_pos[0] < ROWS and 0 <= new_pos[1] < COLS and grid[new_pos[0]][new_pos[1]] == 0 and tuple(new_pos) not in visited:
            # Valid move
            rover_position = list(new_pos)
            path.append(tuple(rover_position))
            state = new_pos[0] * COLS + new_pos[1]
        else:
            # Backtracking: Explore other possible actions
            found_alternative = False
            for alt_action in range(len(ACTIONS)):
                new_pos = (rover_position[0] + ACTIONS[alt_action][0], rover_position[1] + ACTIONS[alt_action][1])
                if 0 <= new_pos[0] < ROWS and 0 <= new_pos[1] < COLS and grid[new_pos[0]][new_pos[1]] == 0 and tuple(new_pos) not in visited:
                    rover_position = list(new_pos)
                    path.append(tuple(rover_position))
                    state = new_pos[0] * COLS + new_pos[1]
                    found_alternative = True
                    break
            
            if not found_alternative:
                print(f"Dead end at {rover_position}. Backtracking.")
                if len(path) > 1:
                    path.pop()  # Remove the last position
                    rover_position = list(path[-1])  # Move back to the previous position
                    state = rover_position[0] * COLS + rover_position[1]
                else:
                    print("No path to goal. Terminating.")
                    break

    return path

# Visualize the grid and path
def visualize(grid, path, start, goal):
    fig, ax = plt.subplots()
    ax.set_xlim(0, COLS)
    ax.set_ylim(0, ROWS)
    ax.set_aspect('equal')
    ax.invert_yaxis()
    
    # Draw grid
    for x in range(ROWS):
        for y in range(COLS):
            color = 'white'
            if grid[x][y] == 1:  # Obstacle
                color = 'black'
            elif (x, y) == start:
                color = 'green'
            elif (x, y) == goal:
                color = 'red'
            ax.add_patch(plt.Rectangle((y, x), 1, 1, color=color, edgecolor='gray'))
    
    rover_marker, = ax.plot([], [], 'yo', markersize=8)  # Rover marker

    def update(frame):
        if frame < len(path):
            rover_marker.set_data([path[frame][1] + 0.5], [path[frame][0] + 0.5])  # Ensure data is a sequence
        return rover_marker,

    ani = animation.FuncAnimation(fig, update, frames=len(path), interval=200, blit=True)
    plt.show()

# Main function
def main():
    # Create training grid
    training_grid = create_grid()
    for _ in range(100):  # Add obstacles
        x, y = random.randint(0, ROWS - 1), random.randint(0, COLS - 1)
        training_grid[x][y] = 1
    start_train = (1, 1)
    goal_train = (ROWS - 2, COLS - 2)

    print("Training the rover...")
    q_table = train_rover(training_grid, start_train, goal_train)
    print("Training complete!")

    # Create testing grid
    testing_grid = create_grid()
    for _ in range(100):  # Add obstacles
        x, y = random.randint(0, ROWS - 1), random.randint(0, COLS - 1)
        testing_grid[x][y] = 1
    start_test = (5, 5)
    goal_test = (ROWS - 5, COLS - 5)

    print("Testing the rover...")
    test_path = test_rover(testing_grid, start_test, goal_test, q_table)
    print("Testing complete!")
    print("Path:", test_path)

    # Visualize the rover's path during testing
    visualize(testing_grid, test_path, start_test, goal_test)

if __name__ == "__main__":
    main()
