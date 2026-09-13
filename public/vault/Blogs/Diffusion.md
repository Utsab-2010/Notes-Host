---
title: "Diffusion"
lastmod: 2026-05-09
---

#diffusion #blog 
Title- Diffusion: A simple hands-on introduction

### Resources
- [Simplest Implementation of Diffusion Models \| Emilio’s Blog](https://e-dorigatti.github.io/math/deep%20learning/2023/06/25/diffusion.html)
- 

Generative AI has been the buzz and face of AI industry for the last few years. Particularly image and video generative models. How do they models generative an image when given a prompt? But how exactly does a model take in text prompt and transform it into a visual output catering to the context of that prompt?

This is where diffusion comes in ! One of the most amazing model architectures and training methodologies in modern AI.

Before we dive into the topic we would first benefit from breaking down this very broad topic into some bite sized chunks for easier digestion.
My intention with this blog will be to give you a intuitive overview of both the math and training workflow of diffusion along with a hands on implementation at the end. While I will go over the necessary math involved, it will be explained in a more intuitive sense rather than rigorous proofs.

It will take a bit of your time but should leave you will good enough clarity regarding the topic.

Here are the topics that we will follow:
- Images as Samples of a distribution
- A Model as an Approximation for a Distribution
- Diffusion: Forward Process - Generating the Training Data
- Denoising Reverse Process
- Visualising the transformation of the probability distribution
- Conditional Diffusion Training

### Images as Samples
Since diffusion based models rely on the idea of transforming a probability distributions and then sampling from them, it is judicious to first understand how images can be seen as samples from some probability distribution.

Any image is just a grid of pixels and each pixel is just a tuple of RGB values. If you consider an image to be a set of variables then you can create any image of resolution HxW with 3HW independent variables ranged between 0-255(or some other common scale). For a typical image generator, generating the image is like sampling from a joint distribution of all these variables. Now ofcourse if the distribution is just some standard distribution like the Gausssian then you will just get a noisy incoherent image. But given that the distribution is a relevent and useful one , the kind of images you want will  have high probability densities and the useless irrelevant ones will have lower.

During training also we like to assume that all the images of our image dataset belong to some joint probability distribution over the variables  and we train our model to learn this ideal distribution from the training data points.

![](/vault/blogs/attachments/pasted-image-20260505091116.png)


### Model as an Approximation
Now it is very difficult to arrive at a closed form solution for getting this probability distribution given the very high dimensionality of the sample space. Hence we use neural networks to approximate this distribution function.
For a discrete sample space, for example in the case of classification problems, we have fixed set of classes into which we need to segregate an image. So typically what we do is we train the model to take in an input and give a probability mass function over the different classes. Then we choose the class with the highest probability as the identified class of the input.
However in the case of image generation we are dealing with a continuous space  and so the approximated function has to be a pdf over this sample space. How can this be done?
We can try training a model with a sigmoid in the last layer to get a value between 0 and 1. But there is no guarantee that it will add up to 1 when summed/integrated over the entire sample space. Hence the function will not a be a probability distribution.

So this is quite a challenging task! What is the general practice that is followed and works out well is to use NNs to approximate the defining parameters of already known distributions. The most standard practice is to use the Gaussian Distribution due to a lot of good properties which I won't discuss :)

Therefore, we define the network as  $p_\theta(x) = \mathcal{N}(x; \mu_\theta, \Sigma_\theta)$; a nn with parameters $\theta$ that approximates the $\mu$ and $\Sigma$ of the required multivariate normal distribution.

### Diffusion Denoising Reverse Process
- [Diffusion Models](/vault/deep-learning/diffusion-models/)
- [Diffusion Reverse Process](/vault/deep-learning/diffusion-reverse-process/)
Now in diffusion we don't exactly find the required probability distribution directly. Instead we follow an iterative process of slowly transforming our starting noising distribution into the required final distribution. Why is this done? That discussion won't happen today but a simple explanation would be, its just works better for the practical setup of approximating non-linearities.

While the theoretical diffusion sampling process (the generative Markov chain) is defined by Gaussian transitions $p_\theta(x_{t-1} | x_t) = \mathcal{N}(x_{t-1}; \mu_\theta, \Sigma_\theta)$, we don't ask the neural network to spit out $\mu$ and $\Sigma$ directly because that's a high-variance, difficult learning task.

Instead we use use something called **reparameterisation trick** to get the values. We using the neural network to predict a noise amount $\epsilon_\theta$ and then use that to approximate the $\mu_{\theta}$ value. 
$$\mu_\theta(x_t, t) = \frac{1}{\sqrt{\alpha_t}} \left( x_t - \frac{\beta_t}{\sqrt{1 - \bar{\alpha}_t}} \epsilon_\theta(x_t, t) \right)$$
Notice that the model takes in input x_t and t. we will get back to this a bit later. The alpha and beta values are just fixed values depending on the noising schedule that is being followed. Why do we do this reparameterisation? Because it makes the training much more stable - similar to ResNets teaching networks to predict the change in input instead of the output estimate is easier for the model to learn. If you are curious why then refer to [this paper](https://arxiv.org/pdf/1712.09913).

Now given a trained model with parameters $\theta$ , the sampling algorithm for generating an image from the target distribution is as follows:

1. **Initialize:** Start with $x_T \sim \mathcal{N}(0, \mathbf{I})$ (pure white noise).
2. **Iterate:** For $t = T, T-1, \dots, 1$:
    - **Sample random noise:** $z \sim \mathcal{N}(0, \mathbf{I})$ if $t > 1$, else $z = 0$.
    - **Predict the noise:** Pass the current image $x_t$ and the time step $t$ into your model to get $\epsilon_\theta(x_t, t)$.
    - **Compute the Mean ($\mu_\theta$):** This is the "de-noised" version of the current image.$$\mu_\theta(x_t, t) = \frac{1}{\sqrt{\alpha_t}} \left( x_t - \frac{\beta_t}{\sqrt{1 - \bar{\alpha}_t}} \epsilon_\theta(x_t, t) \right)$$
    - **Update the Image:** Calculate the next step $x_{t-1}$ by adding back a tiny bit of controlled variance ($\sigma_t z$) to keep the process stochastic:$$x_{t-1} = \mu_\theta(x_t, t) + \sigma_t z$$
3. **Result:** $x_0$ is your generated image.

This algorithm essentially starts with a single sample from a random distribution and then iteratively transforms the distribution to the target distribution over T steps such that the sample gets transformed to a sample from the target distribution. And since in the target distribution only the coherent samples have high probabilities , the final sample should also be coherent and desirable.
Note:
- **Variance Schedule ($\alpha, \bar{\alpha}, \beta$):** These must be the exact same values used during the training (Forward) phase.
- **Total Steps ($T$):** The number of iterations (e.g., 1000).

### The Forward (Training) Process
Now that you understand(hopefully) the process of generation of an image via diffusion, we can discuss how these models can be trained.

While there has been a multitude of training methods catering to diffusion and similar architectures, I will be going over the most well-known one which was discussed in the foundational paper of DDPM.

Since we were using the trained model to predict the noise of a given image + timestamp input, we will need to create data to serve this purpose and train it accordingly with some loss function.  How do we make the training data for this? We make use of any image dataset and start adding noise at different intensities to the given image!

But we don't do it in any arbitrary manner, rather we do a time-scheduled addition, hence the "t" in the model input.

 In the forward process, we generate $x_t$ from the clean image $x_0$ and some sampled noise $\epsilon \sim \mathcal{N}(0, \mathbf{I})$:

$$x_t = \sqrt{\bar{\alpha}_t}x_0 + \sqrt{1-\bar{\alpha}_t} \epsilon$$

where $\bar{\alpha}_t$ goes from 1 at t=0 to 0 at t=T following some curve(linear, exponential, polynomial, etc). We define  $\alpha_t = 1 - \beta_t$ where $\beta_t$ is called the variance schedule 
 We use a variance schedule $\beta_t$ to gradually add Gaussian noise to a clean image $x_0$.

Using the **reparameterization trick**, we can sample an image $x_t$ at any arbitrary timestep $t$ directly from $x_0$ without iterating through all previous steps:

$$x_t = \sqrt{\bar{\alpha}_t} x_0 + \sqrt{1 - \bar{\alpha}_t} \epsilon, \quad \epsilon \sim \mathcal{N}(0, \mathbf{I})$$

Where:

-
    
- $\bar{\alpha}_t = \prod_{i=1}^t \alpha_i$ (the cumulative product of the noise schedule)
    
- $\epsilon$ is the "ground truth" noise we injected.
    

We provide the model (usually a U-Net) with the noisy image $x_t$ and the current timestep $t$. The model's job is to predict the noise $\epsilon$ that was used to corrupt $x_0$. 

What is the most simple loss function you can think of that might be used here? We are predicting a continuous value! This is just regression on the noise values. Therefore, a sane choice would be the **Mean Squared Error ($L_2$ norm)** between the true noise $\epsilon$ and the predicted noise $\epsilon_\theta$: 
$$\mathcal{L}_{simple}(\theta) = \mathbb{E}_{t, x_0, \epsilon} \left[ \| \epsilon - \epsilon_\theta(x_t, t) \|^2 \right]$$

#### Why $L_2$?

Mathematically, minimizing the $L_2$ error in noise prediction is equivalent to maximizing the **Evidence Lower Bound (ELBO)** under the assumption that the reverse transitions are Gaussian. In simpler terms: because we assume our "noise" is a Gaussian bell curve, the $L_2$ distance is the most natural way to measure how far our prediction is from the truth.
#### The Training Algorithm
1. **Sample** a clean image $x_0$ from your dataset (e.g., a digit from MNIST).
2. **Pick a random timestep** $t$ between $1$ and $T$ (e.g., $t=450$ out of $1000$).
3. **Generate random noise** $\epsilon$ and mix it with $x_0$ using the formula above to create $x_t$.
4. **Optimize:** Take a gradient descent step to minimize the $L_2$ distance between the predicted noise and actual noise.

---

















### Implementation


### Summary for the Reader

> "During training, we are essentially playing a game of 'Hide and Seek.' We hide a real image under a layer of static (noise) and tell the model exactly how much static we added. The model wins if it can look at the mess and accurately point out only the pixels that are noise. By repeating this millions of times across different levels of static, the model learns the underlying structure of the data it is trying to protect."

Would you like a snippet of the loss calculation in PyTorch to include alongside this math?


### How to explain this to your "Novice":

To your novice, don't show the $\alpha$ and $\beta$ algebra. Explain it as **"The Sculptor's Method"**:

> "Imagine you have a block of marble (the noise) and there is a statue (the digit 7) hidden inside it. Instead of the model trying to 'draw' the 7 from memory, the model is trained to identify which parts of the marble are **excess stone** that need to be chipped away. By predicting and removing the noise, the model is left with the perfect distribution of the digit."

### Why this is "Standard Normal to Required Normal":

You are exactly right: we start at $T$ with $x_T \sim \mathcal{N}(0, \mathbf{I})$ (Standard Normal).

At each step $t \to t-1$, we use our predicted noise to "shift" that distribution. We aren't just jumping to the answer; we are slowly nudging the center (mean) of our Gaussian until, at step 0, it perfectly overlaps with the data distribution.

Are you planning to show the derivation of that $\mu_\theta$ formula in your blog, or keep it strictly to the implementation of the $\epsilon$-loss?
