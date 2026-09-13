---
title: "MAP vs MLE"
lastmod: 2026-02-20
---

	"The logic that f* cks your mind"
To make the distinction crystal clear, let’s use the medical test example with concrete numbers. This will show you exactly why the **ML** and **MAP** detectors can sometimes pick different "winners" based on the same data.

### **The Scenario**

Imagine a rare disease that only **1%** of the population has.

- **Prior ($P(M)$):** $P(\text{Sick}) = 0.01$ and $P(\text{Healthy}) = 0.99$.
    
- **The Channel (The Test):** The test is very good but not perfect.
    
    - If you are sick, it's positive **90%** of the time ($P(y|\text{sick}) = 0.9$).
        
    - If you are healthy, it's negative **90%** of the time—meaning it gives a "False Positive" **10%** of the time ($P(y|\text{healthy}) = 0.1$).
        

**The Observation ($y$):** You just got a **Positive Test Result**.

---

### **1. The ML Detector (Maximum Likelihood)**

The ML detector asks: _"Which hypothesis ($m$) makes the positive result ($y$) most likely according to the 'physics' of the test?"_

- **Likelihood if Sick:** $P(y|\text{sick}) = \mathbf{0.9}$
    
- **Likelihood if Healthy:** $P(y|\text{healthy}) = \mathbf{0.1}$
    

**The Decision:** Since $0.9 > 0.1$, the **ML detector** ignores how rare the disease is and chooses **Sick**. It picks the $m$ that has the highest "compatibility" with the result.

---

### **2. The MAP Detector (Maximum A Posteriori)**

The MAP detector asks: _"Taking into account both the test and the rarity of the disease, what is the actual probability I am sick?"_

We use **Bayes' Rule** (as seen in your notes) to find the Posterior $P(m|y) = P(y|m) \cdot P(m)$. (We can ignore the denominator $P(y)$ because it's the same for both calculations).

- **Posterior Score for Sick:** $P(y|\text{sick}) \cdot P(\text{sick}) = 0.9 \cdot 0.01 = \mathbf{0.009}$
    
- **Posterior Score for Healthy:** $P(y|\text{healthy}) \cdot P(\text{healthy}) = 0.1 \cdot 0.99 = \mathbf{0.099}$
    

**The Decision:** Since $0.099 > 0.009$, the **MAP detector** chooses **Healthy**. Even with a positive test, the "Prior" (the fact that 99% of people are healthy) is so strong that it's more likely the test made a mistake.

---

### **Summary of Results**

|**Detector**|**Decision**|**Logic**|
|---|---|---|
|**ML**|**Sick**|"The test says positive, and sick people get positive results most often."|
|**MAP**|**Healthy**|"The test is positive, but the disease is so rare that it's probably just a false alarm."|

This is exactly what your notes mean when they say the **MAP Rule** becomes the **ML Rule** if the messages are uniform. If the disease was 50/50 (uniform prior), both detectors would have picked "Sick."

- looking at it from a geometric perspective maybe