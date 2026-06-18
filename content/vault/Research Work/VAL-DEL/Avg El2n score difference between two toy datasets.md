---
title: "Avg El2n score difference between two toy datasets"
---

#### Case 1: Fixed Vector Summed + Noise  as Input
![](/vault/attachments/pasted-image-20260615183754.png)

#### Case 2: Multi-Hot Vector as Input
![](/vault/attachments/pasted-image-20260615183800.png)


As can be seen the 2nd toy el2n scores(above) are much higher than the one below(multi-hot vector toy dataset)

**Case II: Multi-Hot Vector Input**
If the input is easy to untangle, then the model directly tries to get biased towards the more frequent quanta, but due to the polygenic nature, the $Y$ label varies quite a bit and hence more frequent quanta lead to more errors (High EL2N).

**Case I: Fixed Vector Summed up as Input**
In this case, the input is more difficult to untangle, that is unlike the previous one , the model cannot read isolated bits and is forced to target the heaviest geometric signatures first. 
Because the frequent quanta are additively present across almost all samples, they create a massive, clear trail in the continuous space that the model aligns with instantly (leading to fewer errors for frequent quanta). Meanwhile, the rare quanta are completely buried inside this difficult-to-untangle geometric pile and drowned out by noise. 

Hence when the model tries to learn, it learns to recognise the more frequent quantas contribution first. However I suppose that just like before there will be label mis-match due to the setup of voting being the same, hence EL2n score of more frequent quanta will be affected by this mismatch a lot more. 
But there is another part of the EL2N in this case, which is the loss due to the mis-indentification of the quanta-specific representations in the summed input. The error due to this is much MORE for the low frequency quanta than the higher ones.

This mis-identification error is added on top of  the label mismatch error  and dominates it , leading to the the overall skew of the plot reversing -> Low Freq Quanta  = Higher EL2n Score, and High Freq Quanta = Low EL2N Score.
*This explaination is supported by the observed curves where the  el2n avg curve in Case 2 is lower than the el2n avg curve of case 1. Indicating that the proposition of the extra loss due to representation misidentificaiton is highly plausible.*

