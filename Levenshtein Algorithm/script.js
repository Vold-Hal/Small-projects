

const inputElement1 = document.getElementById("str1");
const inputElement2 = document.getElementById("str2");

const resultsP = document.getElementById("results");
const tableDiv = document.getElementById("table-div");
const button = document.getElementById("start-btn");
button.addEventListener("click", controller);

var dp;

var startTime;
var endTime;

function controller(){
    var dist = levenshteinDistance(inputElement1.value, inputElement2.value);
    var elapsedTime = endTime - startTime;
    elapsedTime = Math.ceil(elapsedTime * 10 ** 3) / 10 ** 3;
    resultsP.innerHTML = `Result distance: ${dist}, elapsed time: ${elapsedTime} milliseconds`;
    tableDiv.removeChild(tableDiv.firstChild);
    tableDiv.appendChild(generateDPTable());
}


function levenshteinDistance(str1, str2) {
    console.log()
    startTime = performance.now();    

    const m = str1.length;
    const n = str2.length;

    // Create a 2D array to store the distances
    dp = new Array(m + 1).fill().map(() => new Array(n + 1).fill(0));

    // Initialize the first row and column of the array
    for (let i = 0; i <= m; i++) {
        dp[i][0] = i;
    }

    for (let j = 0; j <= n; j++) {
        dp[0][j] = j;
    }

    // Calculate the Levenshtein Distance
    for (let i = 1; i <= m; i++) {
        for (let j = 1; j <= n; j++) {
            if (str1[i - 1] === str2[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1];
            } else {
                dp[i][j] = Math.min(
                    dp[i - 1][j] + 1, // deletion
                    dp[i][j - 1] + 1, // insertion
                    dp[i - 1][j - 1] + 1 // substitution
                );
            }
        }
    }


    endTime = performance.now();   
    return dp[m][n];
}


function generateDPTable() {
    const m = dp.length;
    const n = dp[0].length;
  
    str1 = padString(inputElement1.value, m);
    str2 = padString(inputElement2.value, n);
    // Create a table element
    const table = document.createElement("table");
  
    // Create the header row with the input words
    const headerRow = document.createElement("tr");
  
    // Create an empty cell at the top-left corner
    const emptyCell = document.createElement("th");
    headerRow.appendChild(emptyCell);
  
    // Create header cells for the second word
    for (let j = 0; j < n; j++) {
      const headerCell = document.createElement("th");
      headerCell.textContent = str2[j];
      headerRow.appendChild(headerCell);
    }
  
    // Append the header row to the table
    table.appendChild(headerRow);
  
    // Iterate through each row of the matrix
    for (let i = 0; i < m; i++) {
      // Create a table row
      const row = document.createElement("tr");
  
      // Create the first column with the characters from the first word
      const firstColCell = document.createElement("th");
      firstColCell.textContent = str1[i];
      row.appendChild(firstColCell);
  
      // Iterate through each cell in the row
      for (let j = 0; j < n; j++) {
        // Create a table cell
        const cell = document.createElement("td");
        cell.textContent = dp[i][j];
  
        // Append the cell to the row
        row.appendChild(cell);
      }
  
      // Append the row to the table
      table.appendChild(row);
    }
    
    table.className = "table";
    // Return the generated table
    return table;
  }
  



  function padString(str, length, char = ' ') {
    if (str.length >= length) {
      return str; // No need to modify the string if it's already equal to or longer than the desired length
    }
  
    const diff = length - str.length; // Calculate the difference in length
  
    // Create a new string by repeating the specified character 'char' for 'diff' times and concatenate it with the original string
    const paddedString = char.repeat(diff) + str;
  
    return paddedString;
  }