---
title: "Personal Notes on the Implementation"
lastmod: 2026-07-30
---

I think at for each game both the trainable model and the frozen opponent  go through mcts simulation guided move selection for each move step. At each move step they save the game state , and the mcts policy obtained after 800 simulations from that state. Finally after all the valid move steps, the game results in a win or loss and the corresponding z value of the game is also stored with the state, action probability data for each step.

Basically if there are 40 moves - 20 for player and 20 for opponent then the buffer gets 40 entries per game where each entry has format:
- (current_game_state, action_prob, final_win_result)
- final win result is -1 or 1.