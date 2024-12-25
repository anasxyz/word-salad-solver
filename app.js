document.addEventListener('DOMContentLoaded', () => {
    const gridContainer = document.getElementById('grid-container');
    const solveButton = document.getElementById('solve-button');
    const resultsList = document.getElementById('results-list');
  
    // Create a 4x4 grid
    const gridSize = 4;
    gridContainer.style.gridTemplateColumns = `repeat(${gridSize}, 1fr)`;
    gridContainer.style.gridTemplateRows = `repeat(${gridSize}, 1fr)`;
  
    for (let i = 0; i < gridSize * gridSize; i++) {
      const cell = document.createElement('input');
      cell.classList.add('grid-cell');
      cell.setAttribute('maxlength', 1);
      gridContainer.appendChild(cell);
    }
  
    // Solve button handler
    solveButton.addEventListener('click', () => {
      const letters = Array.from(gridContainer.children).map(cell => cell.value.toLowerCase());
      const grid = [];
      for (let i = 0; i < gridSize; i++) {
        grid.push(letters.slice(i * gridSize, (i + 1) * gridSize));
      }
  
      // Log the grid to check its structure
      console.log('Sending grid to backend:', grid);
  
      // Call backend API
      fetch('http://127.0.0.1:5000/solve', {  // Update to your local Flask server URL
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ grid })
      })
        .then(response => {
          console.log('Response received:', response);  // Log the response object
          if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
          }
          return response.json();
        })
        .then(data => {
          console.log('Data from backend:', data);  // Log the response data
          // Clear and display results
          resultsList.innerHTML = '';
          if (data.words && data.words.length > 0) {
            data.words.forEach(word => {
              const li = document.createElement('li');
              li.textContent = word;
              resultsList.appendChild(li);
            });
          } else {
            resultsList.innerHTML = '<li>No words found.</li>';
          }
        })
        .catch(err => {
          console.error('Error:', err);
          resultsList.innerHTML = '<li>Error solving the puzzle. Please try again.</li>';
        });
    });
  });
  