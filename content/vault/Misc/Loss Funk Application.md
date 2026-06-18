---
title: "Loss Funk Application"
---

|                                                                   |                                                                                                                                                                                                                                                                                     |
| ----------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Create learning algorithms that are as sample efficient as humans | What can we study from the nature of data to drive sample efficiency? How can we use data to create new data (are world models involved?) ? What kinds of abstractions lead to sample efficient learning?  <br>  <br>Explore tradeoff between compute, parameters and data samples. |

[Research Internship](https://binary.so/Cx8u9Uj)

Diffusion Language Model(ongoing) - Trying to implement a diffusion based small language model inspired by the seminal paper "Diffusion LM".
AlphaZero for Black Hole Game(ongoing) - Implementing the AlphaZero framework for training an AI agent to win in the game of Black Hole.
Monocular Depth Estimation - Reproduced and trained a monocular depth estimation model from scratch from an ICPR paper.


Here is a more detailed list of your publications and projects, synthesized from your background and research experience:

- Safe Indoor Exploration and Sparse Topological Mapping: Developed a framework for safe kinodynamically  feasible exploration and navigation with an integrated planner and control as part of my intern work at ARMS Lab, IIT Bombay. The work was presented at the IEEE Indian Control Conference (ICC) 2025.

- BAS-Enabled Navigation for Omnidirectional AGVs: Published in EAI Endorsed Trans AI Robotics, this work implemented Beetle Antennae Search (BAS) for optimizing PID controls and A* path planning in unknown environments with a focus on obstacle avoidance. This was part of a remote work I did under Prof. Moshayedi and Prof. Shuai Li.

- Diffusion Language Model from Scratch(ongoing): Tried implementing a 90M parameter BERT-style diffusion SLM from scratch following the seminal paper "Diffusion-LM". Got mediocre results on the e2e dataset. Currently working on improving the training stability, dealing with false convergence and implementing improved pipelines from other works.

- AlphaZero for BlackHole (ongoing) - Working on implementing the Alphazero framework to train an agent to excel in the game of black hole. Tried out simple self-play  RL training and the agent currently outperforms random policies. Currently integrating MCTS algorithm to enhance the decision making capabilities.
   
- Monocular Depth Estimation for Edge Devices: Tried re-implementing a lightweight encoder-decoder model following an ICPR paper. It was done from scratch building upon the MobileNetV2 encoder as given in the paper. Achieved moderate results after training on a sparse dataset of KiTTi and CityScapes depth images due to computational bottlenecks.

- F1Tenth/RoboRacer : Designed and evaluated Pure Pursuit and Stanley controllers for high-speed autonomous racing simulations for F1tenth/Roboracer. Worked on the localization and control modules for the Roboracer Sim Challenge at ICRA 2025 where we got 1st in the prelims and 9th in the finals worldwide.

- Robust Visual Foraging Challenge - Designed a visual encoder for guiding a mouse agent to target in a black and white environment with disturbances. We got 2nd place in this workshop challenge hosted at NeurIPS 2025.

- IITB Research Intern: I worked at the ARMS Lab under Prof. Leena Vachhani. I worked on curated Human trajectory datasets to replicate human like crowd behaviours on Gazebo simulations, recording possible social evaluation metrics and establishing benchmarks for different scenarios . 

- Object Tracking Aim Bot: Created an Aim Bot using computer vision based hand-tracking. Part of 1st year DIY course.



I went through the listed topics and found a few that really match what I’m interested in right now, especially the more mathematical and theoretical side of machine learning. I’m particularly curious about the **[The Manifold Hypothesis](/vault/deep-learning/the-manifold-hypothesis/)**. I’d like to understand whether the structures deep networks learn are actually properties of the data itself, or if they mainly come from the way we design the loss functions and training objectives.

I’m also interested in how learned representations help models generalize well. This connects closely to my previous work in autonomous driving, where good representations are very important for reliable performance.

Apart from this, I find [Continual Learning](/vault/deep-learning/continual-learning/) and sample-efficient learning very exciting. Both seem like open and challenging problems, and I would really like to explore them further.