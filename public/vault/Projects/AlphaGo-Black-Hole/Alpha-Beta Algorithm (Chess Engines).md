---
title: "Alpha-Beta Algorithm (Chess Engines)"
lastmod: 2026-06-02
---

Traditional chess engines, such as Stockfish and Deep Blue, utilize a highly optimized **alpha-beta search** algorithm to navigate the game's vast complexity. This method is a variation of the minimax algorithm that improves efficiency by "pruning" or cutting off branches of the search tree that are provably inferior to others, meaning they need not be evaluated to find the optimal move.

Key components and enhancements of this traditional search include:

- **Iterative Deepening and Move Ordering:** The efficiency of alpha-beta search relies heavily on the order in which moves are considered. Engines use **iterative deepening**, where they perform a shallow search to rank moves, then use that order to guide a deeper search. Specific heuristics help order these moves, such as the **killer heuristic** (moves that caused a cutoff at the same tree depth previously) and the **history heuristic**.
- **Pruning Strategies:** Beyond standard alpha-beta pruning, engines employ domain-specific techniques to reduce the search space.
    - **Null Move Pruning:** Assumes that passing the turn (a null move) would result in a worse position than any valid move; if the position is still good after a null move, the branch is cut.
    - **Futility Pruning:** Cuts branches where even a beneficial outcome is unlikely to raise the evaluation above a certain threshold.
    - **Principal Variation Search (PVS):** A technique often used alongside **aspiration windows** to narrow the search window around expected values.
- **Search Extensions and Reductions:** The algorithm does not search all paths to the same depth. It extends the search depth for promising or critical variations ("extensions"), such as check moves or "singular moves" that have no clear alternative. Conversely, it reduces the depth for unpromising lines ("reductions") based on heuristics like the static exchange evaluation (SEE).
- **Quiescence Search:** Because static evaluation functions are inaccurate during tactical exchanges (like captures), engines use a specialized quiescence search at leaf nodes. This resolves ongoing tactical sequences until a "quiet" position is reached before applying the evaluation function.
- **Transposition Tables and Databases:** Engines utilize **transposition tables** to store and reuse evaluations for positions that are reached via different move orders. They also rely on pre-calculated **opening books** and **endgame tablebases** (which contain optimal moves for positions with few pieces) to bypass search in specific game phases.

Unlike AlphaZero's MCTS, which averages evaluations over a subtree, alpha-beta search computes an explicit minimax, which tends to propagate approximation errors from the leaves up to the root.