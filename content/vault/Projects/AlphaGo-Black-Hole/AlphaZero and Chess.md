---
title: "AlphaZero and Chess"
---

### Contributions
- Superhuman level chess
- no prior human chess data used.
- Blank-slate RL , entirely Self Play

### Core Methodology
NN Architecture:
- network took into state(current position) and output 2 vectors
	- move probabilities of different moves
	- value estimate: estimating the expected outcome of the game from that position

Monte Carlo Tree Search
- Used this instead of the traditional alpha-beta search used by chess engines
- Search is guided by the NN predictions
	- explores future moves by selecting those with high move probability and estimated value
- Allowed MCTS to search significantly fewer positions(80k) than Stochfish (70M) while making superior choices.

Training Details: 

### Surprising Results
With the self-play training, AlphaZero independently rediscovered and played many of the popular human chess openings. Remember it was never provided data to do this. It discovered them simply by FAFO(fuck around find out). Some openings it used:
- Sicillian Defense
- Queen's Gambit
- Ruy Lopez
- English Opening
- Caro-Kann Defence
It then went on to defeat Stockfish with these!