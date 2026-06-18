---
title: "AlphaZero"
---

This is a 3 min recap of my implementation of Google's Alpha Zero framework on the game of black hole.

1. Black Hole Rules
This is a recap of how I implemented Google's AlphaZero framework for the game of Black-Hole. But first let us understand the rules of the game. You have a 9 layer triangle of hexagonal cells. Both players are supposed to play by alternating filling up the cells with values from 1 to 22 in ascending  order. At the end of their play, a single cell remains - THE BLACK HOLE. The score gets computed as the sum of the points in the immediately adjascent cells of the black-hole and whoever gets the lower score wins.
2. Alphazero Framework
	1. Model definition/Architecture
			The state of the board was defined using a square lower triangular matrix, with values to indicate player's moves and empty cells.
		1. This was fed to the ConvNet models for the Policy and  Value Networks(similar to the AlphaZero Architecture)
	2. MCTS Tree formation and usage:
		1. The most crucial part of the framework was the Monte Carlo Tree Search which guided the learning.
		2. 
3. Training Plot and observations
4. Other Attempts
	1. The original rendition of the game had a much smaller state-space and although the model outperformed the random policy it found trouble is finding dominating strategies against humans due to the small state space.
5. Live Demo(~2sec)