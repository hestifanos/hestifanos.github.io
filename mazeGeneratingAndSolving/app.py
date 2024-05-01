from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/generate_maze', methods=['POST'])
def generate_maze():
    width = int(request.form['width'])
    height = int(request.form['height'])

    # Generate maze using Randomized Prim's algorithm
    maze_prim = generate_maze_prim(width, height)

    return jsonify({ 'maze_prim': maze_prim})


# 
# Maze generation functions
# def generate_maze_dfs(width, height):
#     maze = []
#     for y in range(height):
#         row = [1] * width  # Initialize all cells as walls
#         maze.append(row)

#     stack = []
#     visited = set()

#     start_x, start_y = 0, 0
#     end_x, end_y = width - 1, height - 1

#     stack.append((start_x, start_y))
#     visited.add((start_x, start_y))

#     while stack:
#         current_x, current_y = stack.pop()

#         maze[current_y][current_x] = 0  # Mark cell as empty

#         if (current_x, current_y) == (end_x, end_y):
#             break  # Stop once end point is reached

#         directions = [(current_x + 2, current_y), (current_x - 2, current_y),
#                       (current_x, current_y + 2), (current_x, current_y - 2)]

#         random.shuffle(directions)
#         for next_x, next_y in directions:
#             if 0 <= next_x < width and 0 <= next_y < height and (next_x, next_y) not in visited:
#                 maze[(current_y + next_y) // 2][(current_x + next_x) // 2] = 0  # Remove wall between current and next
#                 stack.append((next_x, next_y))
#                 visited.add((next_x, next_y))

#     return maze

def generate_maze_prim(width, height):
    maze = []
    for y in range(height):
        row = [0] * width  # Initialize all cells as empty
        maze.append(row)

    start_x, start_y = 0, 0
    visited = set()
    visited.add((start_x, start_y))

    walls = []
    for x in range(0, width, 2):  # Adjusted range for columns
        for y in range(0, height, 2):  # Adjusted range for rows
            walls.append((x, y))

    while walls:
        wall_index = random.randint(0, len(walls) - 1)
        x, y = walls[wall_index]
        walls.pop(wall_index)
        maze[y][x] = 1  # Set the cell as part of the path
        visited.add((x, y))

        neighbors = []
        if x >= 2 and (x - 2, y) in visited:
            neighbors.append((x - 2, y))
        if x <= width - 3 and (x + 2, y) in visited:
            neighbors.append((x + 2, y))
        if y >= 2 and (x, y - 2) in visited:
            neighbors.append((x, y - 2))
        if y <= height - 3 and (x, y + 2) in visited:
            neighbors.append((x, y + 2))

        if neighbors:
            neighbor_x, neighbor_y = random.choice(neighbors)
            maze[(y + neighbor_y) // 2][(x + neighbor_x) // 2] = 1  # Set the cell between as part of the path
            visited.add((neighbor_x, neighbor_y))

    return maze


# # Maze solving algorithms
# def flood_fill(maze, start, end):
#     queue = [(start, [])]
#     visited = set()

#     while queue:
#         current, path = queue.pop(0)
#         if current == end:
#             return path + [current]
        
#         visited.add(current)
#         x, y = current
#         for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
#             nx, ny = x + dx, y + dy
#             if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze) and maze[ny][nx] == 0 and (nx, ny) not in visited:
#                 queue.append(((nx, ny), path + [current]))

    return None

def heuristic(current, end):
    return abs(current[0] - end[0]) + abs(current[1] - end[1])

def a_star(maze, start, end):
    queue = [(heuristic(start, end), start, [])]
    visited = set()

    while queue:
        _, current, path = min(queue)
        queue.remove((_, current, path))
        if current == end:
            return path + [current]
        
        visited.add(current)
        x, y = current
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze) and maze[ny][nx] == 0 and (nx, ny) not in visited:
                queue.append((heuristic((nx, ny), end) + len(path) + 1, (nx, ny), path + [current]))

    return None

@app.route('/solve_maze_a_star', methods=['POST'])
def solve_maze_a_star():
    maze_data = request.json.get('maze')
    start = tuple(request.json.get('start'))
    end = tuple(request.json.get('end'))

    # Calculate heuristics using A* algorithm
    path = a_star(maze_data, start, end)

    if path:
        return jsonify({'path': path})
    else:
        return jsonify({'path': []})


def solve_maze_dfs(maze, start, end):
    def is_valid_move(x, y):
        return 0 <= x < len(maze[0]) and 0 <= y < len(maze) and maze[y][x] == 0

    def dfs(x, y, path):
        if (x, y) == end:
            return path + [(x, y)]

        visited.add((x, y))

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if is_valid_move(nx, ny) and (nx, ny) not in visited:
                result = dfs(nx, ny, path + [(x, y)])
                if result:
                    return result

        return None

    visited = set()
    return dfs(start[0], start[1], [])
    
@app.route('/solve_maze_dfs', methods=['POST'])
def solve_maze_dfs_route():
    maze_data = request.json.get('maze')
    start = tuple(request.json.get('start'))
    end = tuple(request.json.get('end'))

    # Solve maze using DFS algorithm
    solution_path = solve_maze_dfs(maze_data, start, end)
    
    return jsonify({'path': solution_path})

if __name__ == '__main__':
    app.run(debug=True)
