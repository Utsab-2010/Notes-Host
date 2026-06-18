---
title: "When Do Curricula Work?"
---

#curriculum_learning

Paper: [\[2012.03107\] When Do Curricula Work?](http://arxiv.org/abs/2012.03107)

### Contributions
- investigate the implicit curricula resulting from achitectural and optimisation bias
- quantify the benefit of explicit curricula, we conduct extensive experiments over thousands of orderings spanning three kinds of learning: curriculum, anti-curriculum, and random-curriculum
- train over 25,000 models over four datasets, CIFAR10/100, FOOD101, and FOOD101N covering a wide range of choices in designing curricula
- curriculum learning, random, and anti-curriculum learning perform almost equally well in the standard setting
- Curriculum learning improves over standard training when training time is limited
- Curricula improves over standard training in noisy regime



![](/vault/papers/attachments/pasted-image-20260507124100.png)
- Each row is an CIFAR image, X axis is the list of different configurations(142 in total) on which the image was trained.
- All the images have been ordered by their average value(across configurations) of the *learned iteration* took to get learnt.
- The redish plot is the spearman correlation matrix. It shows high values between architectural families coz the iteration orderings over the images is similar.
#### Implicit Curricula
The order in which the network learns the training samples from a dataset under normal SGD with iid data sampling is referred to as *Implicit Curricula*. It is a result of the architecture and optimisation procedure.




#### Scoring Functions 
We define scoring functions such that samples with more score are more difficult to learn.
- *Simple Loss Function*: $l(f_{w}(x_{i}),y)$
- *Learned epoch/iteration*: $s(x_i, y_i) =  min_{t^∗}\{t^∗|\hat{y}(t)_i=y_i\forall \quad t^*\leq t\leq T\}$
- *Estimated c-score*: itss designed to capture the consistency of a reference model correctly predicting a particular example’s label when trained on independent i.i.d. draws of a fixed sized dataset not containing that example
	![](/vault/papers/attachments/pasted-image-20260510201729.png)

### Pacing Functions: Forcing explicit curricula
![](/vault/papers/attachments/pasted-image-20260510203314.png)
a = fraction of training till full dataset is accessed
b = initial fraction of dataset being accessed
![](/vault/papers/attachments/pasted-image-20260510203429.png)
- each symbol is a (a,b) config. We observe that in the standard learning scenario with a good dataset and ample training time, *curricula does not provide any benefit*.

![](/vault/papers/attachments/pasted-image-20260510203635.png)
![](/vault/papers/attachments/pasted-image-20260510204059.png)



![](/vault/papers/attachments/pasted-image-20260510205210.png)
- both label noise and reduced time training induce a more difficult c-score distribution and curricula can help by focusing first on the easier examples.

### Curricula in the large data regime
- Large data like FOOD101 and FOOD101N
- Again, we observe none of the orderings or pacing functions significantly outperforms standard i.i.d. SGD learning. 
- Similar conclusions as before
	- Curricula only helps for limited time or noisy label scenarios
