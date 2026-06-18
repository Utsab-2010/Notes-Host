---
title: "Detect the change of implicit curricula"
---

### Hypothesis:
Based on the quantisation paper, to learn a particular quanta it has to be seen $\tau$ no. of times(in unique samples). But that paper kinda considered the quantas to be independent of each other, that is learning one quanta does not affect the learning of another quanta.

For a particular dataset having a range of quantas, the model will follow its own implicit curricula for the dataset based on which samples it can learn earlier. Now pruning based on some metric will change this curricula? It can improve or degrade it?

How to see this change of curricula with a our datasets?


# Experiment Design:
### 1. The Time to Learn - per Quanta
a. Basically Train on the given dataset for a number of epochs.
b. At each epoch, check if the quanta has been learnt.
	Basically to test the particular quanta, we take a batch of that that quanta's template vector, add noise to it(prepare a monogenic sample with that quanta) and pass it through the model to find the class. Since each monogenic sample maps to a particular class there won't be an issue.
	If the acc on this minibatch is more than 90% then keep the epoch count same for that quanta otherwise inc the epoch count.
c. Plot the learned epoch values against each quanta's rank.
*Multiple colors represent the different classes for each quanta. Since each quanta corresponds to a single class in a mono-genic setup.(it's dominant class)*
# Observations
**Some Results and Conclusions:**
- Frequency seems to have a positive Corr with the learned epoch. Higher frequency usually corresponds to  lower learned epoch value(based on the quantisation paper)
**Alpha = 1.2** for all the following setups
### Setup 1: Polygeny = 1, Noiseless, Classes = 1000, mx_q_classes = 50
![](/vault/attachments/pasted-image-20260616153442.png)
### Setup 2: Polygeny = 1, Noiseless, Classes = 100, mx_q_classes = 50
![](/vault/attachments/pasted-image-20260616153657.png)
### Setup 3: Polygeny = 1, Noiseless, Classes = 100, mx_q_classes = 5
![](/vault/attachments/pasted-image-20260616153827.png)

### Setup 4: Polygeny = 10, Noiseless, Classes = 100, mx_q_classes = 15
![](/vault/attachments/pasted-image-20260616154005.png)

### Setup 5: Polygeny = 10, N = 0.01, Classes = 100, mx_q_classes = 15
![](/vault/attachments/pasted-image-20260616154211.png)

*Noise Doesn't Seem to be Affecting It*.

### Setup 6: Polygeny = 1, N = 0.01, Classes = 100, mx_q_classes = 5, alpha = 0.4
![](/vault/research-work/val-del/attachments/pasted-image-20260616165018.png)
Lower Alpha leads to a fatter tail of the distribution and hence more close frequency counts for the higher ranks. Hence some bias helping your neighbour learn is more likely to help you learn too within the same epoch.
Also notice the big seperation in between.
**Below is the same Setup 6 but with NO NOISE.**
![](/vault/research-work/val-del/attachments/pasted-image-20260616165414.png)


## Possible Explanations for the Plots
1. **Maybe the correlations from templates are affecting it?** -  input is noiseless, but the templates (tq​) are random vectors in a 256-dimensional space. While random high-dimensional vectors are _mostly_ orthogonal, they are never _perfectly_ orthogonal. There will always be random variance in their cosine similarities.
	**Not the main reason** - as shown by the corr. plot below.
	![636](/vault/attachments/pasted-image-20260616155033.png)

2. **$\tau_{learn}$ dependent on frequency and training biases?**
	Basically when the model starts learning the more frequent samples, it gets biased towards theirs class mappings. And that  bias buildup influences the training time of the other rarer quantas. (*This is basically one of the predicted benefits of curricula learning - using the bias from previous samples to learn later samples faster. However I am not sure how it is happening because all the quanta vectors are independent.*)
	In the above plots, we see that the $\tau_{learn}$ of the rarer quantas vary from the very low to the predicted (frequency based) value.

## Some Doubts Regarding this Evaluation Setup
1. In the Quantization paper, their task bits didn't exactly map to a single class in a monogenic setup. Rather the task bits encoded a decision rule(based on subset selection) and that rule was followed over the data part of the input.
	However, in this case our quanta encoded to a fixed ranomd vector template which again leads to a particular class.  While the later one is more close in behaviour to image datasets, this difference in the data generation might be something to rethink a few more times. 
	Maybe we can try thinking of some combination of both these ideas.