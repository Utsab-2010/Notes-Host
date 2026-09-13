---
title: "Law of Total Expectations"
lastmod: 2026-02-11
---

![](/vault/video-ideas/spider-fly-problem.png)

## Script
#### Intro
While going through the course material for a class at my university I stumbled upon this problem. I tried long and hard to solve this but it seemed like I always overcomplicated the train of thought.
A thing about solving such problems is to build a proper intuition through practice. This problem introduced me to the beautiful concept of Total expectation theorem.

Since you are watching this video, I expect that you have a basic idea of what probability theory is. Basic concepts like random variables and their expectations.
But to summarize once again.
- a random variable refers to the outcome of a random experiment.
- Now this experiment is sampled from the event space containing all possible events/scenarios. each scenario leads to an outcome.
- Now given a random variable X with a probability distribution , we can write the expectation of X: $$E(X) = \sum_{w \in F} x.p(x) \ $$
- In simple words, the expected value of X can be said to be the average value of X you will get given you conduct this random experiment a LARGE number of times.

### Total Expectation Theorem
It states that the expectation of random variable X is equal to the sum of the conditional expectations weighted by their respective probabilities.
While a formal proof is beyond the scope on this video, the intuitive way of thinking about it would be to think of a weighted average the same way we thought of the definition of the expectation.
Any outcome X can be broken into sub-scnearios called conditional outcomes X|A. 
this means that given A has happened
so E[X|A] means that given that A has happened what is the expected value of X.
if there can only be two conditional scnearios A1 and A2, then we can break the outcome of random variable X into X|A1 and X| A2.  Now when we  write the law of total expectations , think of this as the mean of these  two probable outcomes, like a normal mean of a random variable having two possible values, you write it as 
$$\large  
\mathbb{E}[X]  
= \mathbb{E}[X \mid A_1] . P(A_1)  + \mathbb{E}[X \mid A_2] . P(A_2)
$$


This is good but why am I talking about this theorem??
This will be better illustrated by this following problem.
Consider this
![](/vault/video-ideas/total-expectation-ques.png)

How would you solve this ? If you want to try it out give it a go.

Let us mark X as the random
While one approach would be to calculate the probability distribution of PMF of  X and then use that to find out the expectation using the expression we discussed before.
The other approach would be a clever use of the law of total expectations.
