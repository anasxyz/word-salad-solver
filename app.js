document.addEventListener('DOMContentLoaded', () => {
    const gridContainer = document.getElementById("grid-container");
    const themeInput = document.getElementById("theme");
    const loadingSpinner = document.getElementById("loading");
    const responseContainer = document.getElementById("response");

    // Function to create the empty grid
    function createGrid() {
        gridContainer.innerHTML = ''; // Clear any existing grid

        // Create a 4x4 grid
        for (let i = 0; i < 4; i++) {
            const row = document.createElement('div');
            row.classList.add('grid-row');
            for (let j = 0; j < 4; j++) {
                const cell = document.createElement('input');
                cell.type = 'text';
                cell.id = `cell${i * 4 + j + 1}`;  // Unique ID for each cell
                cell.maxLength = 1;  // Only allow one letter per cell
                cell.classList.add('grid-cell');
                row.appendChild(cell);

                // Add event listeners for keydown and input
                cell.addEventListener('keydown', (e) => handleKeyDown(e, i, j));
                cell.addEventListener('input', () => handleInput(i, j)); // Handle the input event for typing
            }
            gridContainer.appendChild(row);
        }

        // Reset the theme input field
        themeInput.value = '';  // Clear the theme input field
    }

    // Call the function to create the grid on page load (refreshes the grid)
    createGrid();

    // Reset Button functionality
    const resetButton = document.getElementById('reset-btn');
    resetButton.addEventListener('click', () => {
        createGrid();  // Re-create the empty grid and reset the theme input
        responseContainer.innerHTML = '';  // Clear the response area
    });

    // Handle keydown events for moving between cells
    function handleKeyDown(event, row, col) {
        const key = event.key;

        if (key === "Backspace") {
            // Move to the previous cell if the current one is empty
            if (document.getElementById(`cell${row * 4 + col + 1}`).value === "") {
                moveToPreviousCell(row, col);
            }
        } else if (key.length === 1 && /[a-zA-Z]/.test(key)) {
            // Do nothing here, input event will handle typing behavior
        }
    }

    // Handle input (when a letter is typed in the cell)
    function handleInput(row, col) {
        // Automatically move to the next cell when a letter is typed
        moveToNextCell(row, col);
    }

    // Function to move focus to the next cell
    function moveToNextCell(row, col) {
        const nextCellIndex = (row * 4 + col + 1);
        const nextCell = document.getElementById(`cell${nextCellIndex + 1}`);
        if (nextCell) {
            nextCell.focus();
        }
    }

    // Function to move focus to the previous cell
    function moveToPreviousCell(row, col) {
        const prevCellIndex = (row * 4 + col - 1);
        const prevCell = document.getElementById(`cell${prevCellIndex + 1}`);
        if (prevCell) {
            prevCell.focus();
        }
    }

    // Function to solve the word salad puzzle
    function solve() {
        // Get the theme and min/max length input values
        const theme = themeInput.value.trim();
        const minLength = document.getElementById('min_length').value;
        const maxLength = document.getElementById('max_length').value;

        // Check if any required fields are empty
        if (!theme || !minLength || !maxLength) {
            alert("Please fill in all required fields.");
            return;  // Prevent proceeding if any field is empty
        }

        // Check if any grid cell is empty
        let gridComplete = true;
        for (let i = 1; i <= 16; i++) {
            const cellValue = document.getElementById(`cell${i}`).value.trim();
            if (!cellValue) {
                gridComplete = false;
                break;  // Exit the loop early if any cell is empty
            }
        }

        // If any grid cell is empty, show an alert and stop the function
        if (!gridComplete) {
            alert("Please fill in all the grid cells.");
            return;
        }

        // Show the loading spinner
        loadingSpinner.style.display = 'block';
        responseContainer.innerHTML = ''; // Clear previous response

        // Collect the letters from all 16 input boxes
        let grid = [];
        for (let i = 1; i <= 16; i++) {
            let cellValue = document.getElementById(`cell${i}`).value.toUpperCase();
            grid.push(cellValue);
        }

        // Send the grid letters and theme to the backend for word solving
        fetch('http://127.0.0.1:5000/solve', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ grid: grid, theme: theme, maxLength: maxLength, minLength: minLength })
        })
        .then(response => response.json())
        .then(data => {
            // Hide the loading spinner after response
            loadingSpinner.style.display = 'none';

            // Check if any words were found
            if (data.words && data.words.length > 0) {
                let wordsList = data.words.join('<br>');
                responseContainer.innerHTML = "<br>" + wordsList;
            } else {
                responseContainer.innerHTML = "<br><strong>No words found</strong>";
            }
        })
        .catch(error => {
            // Hide the loading spinner in case of error
            loadingSpinner.style.display = 'none';
            console.error('Error:', error);
        });
    }

    // Solve Button functionality
    const solveButton = document.getElementById('solve-btn');
    solveButton.addEventListener('click', solve);
});

// Toggle dark mode on or off
function toggleDarkMode() {
    const body = document.body;
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    
    // Toggle the dark mode class on the body
    body.classList.toggle('dark-mode');
    
    // Save the current preference in localStorage
    if (body.classList.contains('dark-mode')) {
        localStorage.setItem('dark-mode', 'enabled');
    } else {
        localStorage.setItem('dark-mode', 'disabled');
    }
}

// Check the saved preference on page load and apply the dark mode if enabled
window.addEventListener('DOMContentLoaded', (event) => {
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    
    // Retrieve the saved dark mode preference from localStorage
    const darkModePreference = localStorage.getItem('dark-mode');
    
    if (darkModePreference === 'enabled') {
        document.body.classList.add('dark-mode');
        darkModeToggle.checked = true;
    } else {
        document.body.classList.remove('dark-mode');
        darkModeToggle.checked = false;
    }
});