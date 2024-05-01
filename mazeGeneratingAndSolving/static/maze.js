$(document).ready(function() {
    const canvasPrim = document.getElementById('mazeCanvasPrim');
    const ctxPrim = canvasPrim.getContext('2d');
    const cellSize = 20;
    let start = null;
    let end = null;
    let knowsGoal = false;
    let solving = false;
    let solutionPath = [];
    let currentStep = -1;
    let mazeData = null;

    function drawMaze(ctx, maze, title) {
        const width = maze[0].length * cellSize;
        const height = maze.length * cellSize;
        ctx.canvas.width = width;
        ctx.canvas.height = height;
        ctx.clearRect(0, 0, width, height);

        // Clear maze area
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(1, 1, width - 2, height - 2);



        // Draw maze walls
        for (let y = 0; y < maze.length; y++) {
            for (let x = 0; x < maze[y].length; x++) {
                if (maze[y][x] === 1) {
                    ctx.fillStyle = '#000000';
                    ctx.fillRect(x * cellSize, y * cellSize, cellSize, cellSize);
                }
            }
        }

        // Draw title
        ctx.fillStyle = '#d7663a';
        ctx.font = 'bold 16px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(title, width / 2, 20);
        // Draw starting point
        if (start !== null) {
            ctx.fillStyle = 'green';
            ctx.fillRect(start[0] * cellSize, start[1] * cellSize, cellSize, cellSize);
        }

        // Draw ending point
        if (end !== null) {
            ctx.fillStyle = 'red';
            ctx.fillRect(end[0] * cellSize, end[1] * cellSize, cellSize, cellSize);
        }
    }

    function handleClick(canvas, event, maze, ctx, title) {
        const rect = canvas.getBoundingClientRect();
        const x = Math.floor((event.clientX - rect.left) / cellSize);
        const y = Math.floor((event.clientY - rect.top) / cellSize);

        if (start === null) {
            start = [x, y];
        } else if (end === null) {
            end = [x, y];
        } else {
            // Clear previous start and end points if both are already set
            start = null;
            end = null;
            // Set current clicked block as the new start point
            start = [x, y];
        }

        // Redraw maze with updated starting and ending points
        drawMaze(ctx, maze, title);
    }

    $('#generateButton').click(function() {
        const width = parseInt($('#widthInput').val());
        const height = parseInt($('#heightInput').val());
        $.ajax({
            url: '/generate_maze',
            method: 'POST',
            data: { width: width, height: height },
            success: function(response) {
                mazeData = response;
                drawMaze(ctxPrim, response.maze_prim, 'Prim Maze');

                // Add click event listeners to mazes
                canvasPrim.addEventListener('click', function(event) {
                    handleClick(canvasPrim, event, mazeData.maze_prim, ctxPrim, 'Prim\'s Maze');
                });
            }
        });
    });

    $('#solveMazeAStarButton').click(function() {
        if (start === null || end === null) {
            alert('Please set starting and ending points.');
            return;
        }
        $.ajax({
            url: '/solve_maze_a_star',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ maze: mazeData.maze_prim, start: start, end: end }),
            success: function(response) {
                solutionPath = response.path;
                currentStep = 0;
                drawNextStep();
            }
        });
    });

    $('#solveMazeDFSButton').click(function() {
        if (start === null || end === null) {
            alert('Please set starting and ending points.');
            return;
        }
        $.ajax({
            url: '/solve_maze_dfs',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ maze: mazeData.maze_prim, start: start, end: end }),
            success: function(response) {
                solutionPath = response.path;
                currentStep = 0;
                drawNextStep();
            }
        });
    });

    function drawNextStep() {
        if (currentStep >= 0 && currentStep < solutionPath.length) {
            const step = solutionPath[currentStep];

            // Clear previous step

            drawMaze(ctxPrim, mazeData.maze_prim, 'Prim\'s Maze');

            // Draw current step
            for (let i = 0; i <= currentStep; i++) {
                const pathStep = solutionPath[i];
                ctxPrim.fillStyle = 'blue';
                ctxPrim.fillRect(pathStep[0] * cellSize, pathStep[1] * cellSize, cellSize, cellSize);
            }

            currentStep++;
            setTimeout(drawNextStep, 300); // Adjust timeout as needed for animation speed
        } else {
            solving = false;
        }
    }

});
