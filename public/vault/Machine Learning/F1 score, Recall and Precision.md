---
title: "F1 score, Recall and Precision"
lastmod: 2026-08-13
---

In classification, recall and F1 are two of the standard metrics alongside precision and accuracy.

#### **Recall (a.k.a. sensitivity, true positive rate)**

$$\text{Recall} = \frac{TP}{TP + FN}$$

Of all the actual positives in the data, what fraction did your model correctly catch? High recall means few false negatives — you're not missing positive cases. This matters most when missing a positive is costly (e.g. disease screening, fraud detection).

#### **Precision** (needed to define F1)

$$\text{Precision} = \frac{TP}{TP + FP}$$

Of everything your model flagged as positive, what fraction actually was positive?

There's usually a tradeoff: push the decision threshold to catch more positives (higher recall) and you'll typically pick up more false positives too (lower precision).

#### **F1 score**

$$F_1 = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$$

It's the harmonic mean of precision and recall, not the arithmetic mean. The harmonic mean punishes imbalance — if either precision or recall is low, F1 stays low, unlike a simple average which would be more forgiving. This makes F1 useful when you want a single number that doesn't let a model game the score by being extreme on just one axis (e.g. predicting everything positive gives recall = 1 but tanks precision, and F1 correctly reflects that this is bad).

## **Why these over plain accuracy:** 
Accuracy is misleading under class imbalance. If 99% of your data is negative, a model that always predicts negative gets 99% accuracy but 0 recall on the positive class — useless. Recall/precision/F1 are computed per-class and expose this.

**Generalization: $F_\beta$ score**

$$F_\beta = (1+\beta^2) \cdot \frac{\text{Precision} \cdot \text{Recall}}{\beta^2 \cdot \text{Precision} + \text{Recall}}$$

$\beta > 1$ weights recall more heavily, $\beta < 1$ weights precision more. F1 is just the $\beta=1$ case.

**For multi-class:** you get per-class precision/recall/F1, then aggregate via macro-average (unweighted mean across classes — treats rare classes equally), micro-average (pool all TP/FP/FN globally — dominated by frequent classes), or weighted-average (weight by class support).

One subtlety worth knowing: precision-recall curves (and the area under them, PR-AUC) are often more informative than ROC curves when the positive class is rare, since ROC-AUC can look deceptively good under severe imbalance.