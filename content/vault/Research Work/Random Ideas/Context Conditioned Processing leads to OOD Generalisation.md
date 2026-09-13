---
title: "Context Conditioned Processing leads to OOD Generalisation"
lastmod: 2026-09-02
---

#to-ponder 

If we look at a cup and a bottle randomly they will have some arbitrary semantic meaning. This meaning can be similar or dissimilar based on the context/task of the setup.

For example a red cup and a green bottle, if the task is to label color then both of them are semantically very different. But if the task is to drink water, then they are semantically very similar and considering they are semantically very similar, a robot should be able to under the context of the task with respect to the objects. Then if it has been trained on a dataset of Cups for drinking task, it should be able to extrapolate the actions to an OOD scenario with a bottle too.

While it might appear OOD in the object space, it is probably ID in the semantic space of the task conditioned actions. Hence, my hypothesis is that true OOD generalisation happens when we are able to map ideas from the OOD space to something in the ID , solve it there and then map it back .