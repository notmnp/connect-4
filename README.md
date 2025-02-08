# **Python Connect 4 - Minimax AI Implementation**

This is a **text-based Connect 4 game** implemented in Python, featuring an **intelligent AI opponent**. The AI leverages the **Minimax algorithm with Alpha-Beta Pruning** to analyze the game state and make optimal moves. It **prioritizes winning moves** while **blocking the human player's threats**, ensuring a challenging and competitive gameplay experience.

---

## **🔹 Features:**

### ✅ **Interactive Gameplay**
- The game presents a **clear and structured UI**, displaying the **current game board** after each move.
- The human player can **input their moves** by selecting a column number.
- The AI responds with an **intelligent move**.

### ✅ **Intelligent AI Opponent (Minimax Algorithm)**
- The AI uses the **Minimax algorithm with Alpha-Beta pruning** to search the best possible move.
- It **maximizes** its chances of winning while **blocking** the opponent's potential victories.
- The AI evaluates the board by:
  - **Prioritizing four-in-a-row wins**.
  - **Blocking the human's three-in-a-row threats**.
  - **Maximizing its own board position strategically**.

### ✅ **Game Result Determination**
- The program **automatically checks for a winner** after each move.
- If the board is full without a winner, it **declares a stalemate**.

### ✅ **Replay Feature**
- After the game ends, the user can **choose to play again** without restarting the program.

---

## **🔹 Algorithm Implementation**
### **⚡ Minimax Algorithm with Alpha-Beta Pruning**
The AI's decision-making is powered by the **Minimax algorithm** with **Alpha-Beta pruning** to improve efficiency.

### **How Minimax Works:**
1. The algorithm **simulates** all possible future board states up to a certain depth.
2. It assigns a **score** to each board state based on the **evaluation function**:
   - **Winning Move:** +1000
   - **Blocking Opponent's Win:** +100
   - **Three-in-a-row (AI):** +10
   - **Three-in-a-row (Human):** -50
   - **Other strategic placements**.
3. The AI selects the **move with the highest score**.

### **Optimizations:**
- **Depth-Limited Search:** The algorithm searches up to **4 moves ahead** for efficiency.
  - 🔹 *You can modify this by changing the `depth` global variable in the code.*
- **Alpha-Beta Pruning:** Eliminates unnecessary moves to reduce computation time.

---

## **🔹 How to Play**
1. **Run the Python script** to start the game.
2. Choose the **board size**:
   - **Rows:** Between **5 and 7**.
   - **Columns:** Between **6 and 8**.
3. Choose **who starts first** (Human or AI).
4. The **game board is displayed**, and the player selects a **column** (1-`column count`).
5. The **AI makes its move**, and the board updates.
6. The game continues until:
   - A **player wins** (four in a row).
   - The **board is full** (stalemate).
7. The game **announces the result** and asks if you want to **play again**.

---