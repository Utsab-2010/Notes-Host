---
title: "FLT Lecture"
lastmod: 2026-09-11
---

### Intuition Behind Generative Modelling - samples from a data distribution

First of all what is the problem that we are trying to solve? What does it mean to generate data and how would we do? What we have right now is my current dataset of images say thousands of pictures of animals - dogs, cats, giraffes,etc.

The main notion behind generative modelling is that we assume that all the data point be it be images,text ,etc are essentially sampled from some high-dimensional underlying distribution p_0. Now the goal of generative modelling is to find or estimate this underlying distribution. Once we have this distribution we should be able to sample from it and the samples should look similar (in essence or semantically) to those of the main dataset.

#### But doing this analytically is very difficult
The problem is real world data is very high dimensional. For an image, suppose

$$
x \in \mathbb{R}^{H\times W\times 3}.
$$

Even a relatively small $256\times256$ RGB image has nearly 200,000 dimensions. So we're trying to learn a probability distribution over an enormous, high-dimensional space most points in this space don't correspond to meaningful images. Which means what if we randomly choose pixels from this space, the resultant image we would get will be much closer to noise instead of anything semantically meaningly.

When I say semantically meaningful, I mean something which hold informtion relevant to us human - like something which can help us identify it, or use it later in some downstream task.

Now there is another popular hypothesis in machine learning called the manifold hypothesis which essentially saws that all this data essentially lies on a more structured lower dimensional manifold embedded inside the original high dimensional domain. The job of generative model is to understand this structure be able to leverage this understanding for meaninful generation.


### Different ways of learning the distribution
There have been several approaches to this.

For example, **autoregressive models** try to factorize the distribution:
$$  
p(x) = \prod_i p(x_i|x_1,\ldots,x_{i-1}).  
$$

VAEs introduce latent variables and learn a mapping between a latent distribution and the data.

GANs take a different approach: a generator produces samples, while a discriminator tries to distinguish generated samples from real ones.

Diffusion models take a rather different perspective.

Instead of trying to directly learn

$$  
p_{\text{data}}(x),  
$$

they construct a process that transforms the complicated data distribution into something very simple. And then they also allow us **reverse that transformation** during inference/generation. This reversal is done with the help of the so called trained diffusion model. Whose role is to help guide the transformation

This is the key intuition behind diffusion models.

## Forward Process
We mentioned that Diffusion is different from other Generative methods because it doesn't give us a direction generation setup but a process through which we can generate. 

The forward process of diffusion constitutes transforming our complex data distribution into a well-known distribution that we can work with. The DDPM paper by --- et. al models this forward process in the form of a markov chain. The proper of a markov chain being that each node's info dependents only on its previous node.

Assume that we have data samples $\mathbf{x}_0$ from the target distribution. In the _forward diffusion process_, noise is gradually added to the sample in $T$ steps, generating increasingly noisy samples $\mathbf{x}_1,\mathbf{x}_2,\ldots,\mathbf{x}_T$, with

$$\mathbf{x}_T \sim p_{\text{prior}}$$

(meaning that the $\mathbf{x}_T$-samples  follow a predefined distribution $p_{\text{prior}}$ for sufficiently large $T$-that is x_T looks like it has been sampled from this prior distribution). The noising procedure must be scheduled to add noise (“destroy” the data sample) at the right pace. To this end, the variance $\beta$ of the added noise increases following a schedule, i.e. the diffusion steps are parameterised by a _variance schedule_ ${\beta_t}_{t=1}^T$. The data distribution is gradually converted into another distribution by repeatedly applying a Markov diffusion kernel $K$, i.e. the data sample $\mathbf{x}_t$ at step $t$ is generated from $\mathbf{x}_{t-1}$ using

q(xt∣xt−1)=K(xt∣xt−1;βt),q(\mathbf{x}_t|\mathbf{x}_{t-1}) = K(\mathbf{x}_t|\mathbf{x}_{t-1};\beta_t),

where $\beta_t$ is the diffusion rate. This makes it clear that the process is Markovian, as each step depends only on the immediately preceding sample. The joint probability of the entire process from the original...
![](/vault/attachments/flt-lecture-1789122519468.webp)
![](/vault/attachments/flt-lecture-1789122664204.webp)
![](/vault/attachments/flt-lecture-1789122672045.webp) where all these Z terms belong to the the standard Normal Distribution.

![](/vault/attachments/flt-lecture-1789122859736.webp)
The samples xt gradually become more noisy, and as T → ∞, xT is drawn from an isotropic Gaussian distribution, q(xT |x0) ≈ N (0, I) = pprior. [Ho et al., 2020] use T = 1000. Regarding the variance schedule, values of βt are  typically in the range [10−4, 0.02].

![](/vault/attachments/flt-lecture-1789122915385.webp)


Thing whole forward noising process does not require any training of the model. But as will be shown later, helps generate the data that will be used to train the model.


