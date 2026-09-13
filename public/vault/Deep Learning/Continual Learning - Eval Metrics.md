---
title: "Continual Learning - Eval Metrics"
lastmod: 2026-05-21
---

### Overall Performance
Evaluated by **average accuracy** (AA) and **average incremental accuracy**(AIA). Let $a_{k,j}$ be the classification accuracy evaluated on the j-th task's test data after the incremental learning of the k-th task ($j\leq k$) 
![](/vault/papers/attachments/pasted-image-20260504183054.png)

### Memory Stability
Evaluated by **Forgetting Measure(FM)** and **Backward Transfer(BWT)**
![](/vault/papers/attachments/pasted-image-20260504183534.png)


