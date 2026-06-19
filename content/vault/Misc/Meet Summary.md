---
title: "Meet Summary"
lastmod: 2026-03-17
---

Objective: Work on a framework for robot learning which has interpretable results or explainable guarantees.

Currently looking at works involving Normalising Flows, it is recently popular ML framework which essentially tries to models the transformation function which converts(transforms) a known prior distribution into the required optimal expert distribution.

Some papers for inspiration:
- RESPO(NeurIPS 23) - Used a reachability indicator in their RL Value(objective) function to ensure safety focus and induce recovering maneuvars back to safe zones from unsafe regions.
- [\[2011.00072\] Learning Stable Normalizing-Flow Control for Robotic Manipulation](https://arxiv.org/abs/2011.00072) - Transformed the complex manipulator space into simple pendulam type control setup , got optimality there and then transformed back to the manipulator space employing normalizing flow based training.
- MaxEnRL via Energy-based Normalising Flows - Uses Energy-Based Normalizing Flows to calculate the soft value function **exactly** via the determinant of the Jacobian, eliminating the need for Monte Carlo approximation typically used in RL training.
