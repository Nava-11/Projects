// script.js

const boxes = Array.from(document.querySelectorAll(".box"));
const msg = document.getElementById("msg");
const resetButton = document.getElementById("reset");
let turnX = true; // true for 'X', false for 'O'

const winningCombos = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
];
const showwinner=(winner)=>{
    msg.innerText=`Congratulations Winner is ${winner}`;
    msgc.classList.remove("hide");
    disable();

}
// Handle Player Move
boxes.forEach((box, index) => {
    box.addEventListener("click", () => {
        if (box.innerText === "" && turnX) {
            box.innerText = "X";
            turnX = false;
            if (checkWinner("X")) return;
            setTimeout(aiMove, 500);
        }
    });
});

// AI Move Logic
const aiMove = () => {
    for (let combo of winningCombos) {
        const [a, b, c] = combo;
        if (boxes[a].innerText === "O" && boxes[b].innerText === "O" && boxes[c].innerText === "") {
            boxes[c].innerText = "O";
            if (checkWinner("O")) return;
            turnX = true;
            return;
        }
        if (boxes[a].innerText === "O" && boxes[c].innerText === "O" && boxes[b].innerText === "") {
            boxes[b].innerText = "O";
            if (checkWinner("O")) return;
            turnX = true;
            return;
        }
        if (boxes[b].innerText === "O" && boxes[c].innerText === "O" && boxes[a].innerText === "") {
            boxes[a].innerText = "O";
            if (checkWinner("O")) return;
            turnX = true;
            return;
        }
    }

    // Block Player's Winning Move
    for (let combo of winningCombos) {
        const [a, b, c] = combo;
        if (boxes[a].innerText === "X" && boxes[b].innerText === "X" && boxes[c].innerText === "") {
            boxes[c].innerText = "O";
            turnX = true;
            return;
        }
        if (boxes[a].innerText === "X" && boxes[c].innerText === "X" && boxes[b].innerText === "") {
            boxes[b].innerText = "O";
            turnX = true;
            return;
        }
        if (boxes[b].innerText === "X" && boxes[c].innerText === "X" && boxes[a].innerText === "") {
            boxes[a].innerText = "O";
            turnX = true;
            return;
        }
    }

    // Choose Center
    if (boxes[4].innerText === "") {
        boxes[4].innerText = "O";
        if (checkWinner("O")) return;
        turnX = true;
        return;
    }

    // Random Move
    const emptyBoxes = boxes.filter(box => box.innerText === "");
    if (emptyBoxes.length > 0) {
        const randomIndex = Math.floor(Math.random() * emptyBoxes.length);
        emptyBoxes[randomIndex].innerText = "O";
    }
    turnX = true;
};

// Check Winner
const checkWinner = (player) => {
    for (let combo of winningCombos) {
        const [a, b, c] = combo;
        if (
            boxes[a].innerText === player &&
            boxes[b].innerText === player &&
            boxes[c].innerText === player
        ) {
            // Highlight the winning combination
            boxes[a].style.backgroundColor = "#4CAF50";
            boxes[b].style.backgroundColor = "#4CAF50";
            boxes[c].style.backgroundColor = "#4CAF50";

            // Display the winner message
            msg.innerText = `Winner: ${player}`;
            msg.style.color = "#4CAF50";

            // Disable further clicks
            boxes.forEach(box => (box.style.pointerEvents = "none"));
            return true;
        }
    }

    // Check for a draw
    if (boxes.every(box => box.innerText !== "")) {
        msg.innerText = "It's a Draw!";
        msg.style.color = "#555";
        return true;
    }

    return false;
};


// Reset Game
resetButton.addEventListener("click", () => {
    boxes.forEach((box) => {
        box.innerText = "";               // Clear all box content
        box.style.pointerEvents = "auto"; // Re-enable pointer events
        box.style.backgroundColor = "";   // Reset any winning highlights
    });
    msg.innerText = "";                   // Clear winner message
    turnX = true;                         // Reset turn to Player X
});

