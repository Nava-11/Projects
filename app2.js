// script.js

const boxes = Array.from(document.querySelectorAll(".box"));
const msg = document.getElementById("msg");
const resetButton = document.getElementById("resetButton");
const pvpButton = document.getElementById("pvpButton");
const pvaiButton = document.getElementById("pvaiButton");

let turnX = true; // true for 'X', false for 'O'
let isPvP = true; // Default mode is Player vs Player

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

// Switch to Player vs Player mode
pvpButton.addEventListener("click", () => {
    isPvP = true;
    resetGame();
    msg.innerText = "Mode: Player vs Player";
});

// Switch to Player vs AI mode
pvaiButton.addEventListener("click", () => {
    isPvP = false;
    resetGame();
    msg.innerText = "Mode: Player vs AI";
});

// Handle Player Move
boxes.forEach((box, index) => {
    box.addEventListener("click", () => {
        if (box.innerText === "") {
            if (turnX) {
                box.innerText = "X"; // Player X
            } else if (isPvP) {
                box.innerText = "O"; // Player O in PvP mode
            }
            
            if (checkWinner(turnX ? "X" : "O")) return;

            if (!isPvP && !turnX) {
                setTimeout(aiMove, 500); // AI move
            }

            turnX = !turnX;
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
    const emptyBoxes = boxes.filter((box) => box.innerText === "");
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
            boxes[a].style.backgroundColor = "#4CAF50";
            boxes[b].style.backgroundColor = "#4CAF50";
            boxes[c].style.backgroundColor = "#4CAF50";
            msg.innerText = `Winner: ${player}`;
            boxes.forEach((box) => (box.style.pointerEvents = "none"));
            return true;
        }
    }

    if (boxes.every((box) => box.innerText !== "")) {
        msg.innerText = "It's a Draw!";
        return true;
    }

    return false;
};

// Reset Game
const resetGame = () => {
    boxes.forEach((box) => {
        box.innerText = "";
        box.style.backgroundColor = "";
        box.style.pointerEvents = "auto";
    });
    msg.innerText = "";
    turnX = true;
};

// Attach reset button event
resetButton.addEventListener("click", resetGame);
