---
title: "LPCV-Track-1"
---

[LPCV - Low Power Computer Vision](https://lpcv.ai/2026LPCVC/tracks/track1/)

![](/vault/competitions/attachments/pasted-image-20260305000240.png)
## To-Dos:
- [ ] Implement the sample solution
- [ ] Find relevant papers
- [ ] Create Repo
- [ ] Run the sample solution
- [ ] Collect relevant datasets
- [ ] prepare baseline
- [ ] create pipeline to train easily on vast.ai

## Ideas

The current State-of-the-Art (SOTA) involves moving beyond simple contrastive learning toward methods that handle **hard negatives**, **compositional logic**, and **parameter efficiency**.

### 1. High-Level Fine-Tuning Approach

The standard objective is the **InfoNCE (Contrastive) Loss**. You feed the model batches of $(Image, Text)$ pairs and train it to maximize the cosine similarity of matching pairs while minimizing it for all others in the batch.

#### The "SOTA Recipe":

1. **Initialize with Pre-trained Weights:** Start with `ViT-L/14` or `ViT-H/14` from [OpenCLIP](https://github.com/mlfoundations/open_clip).
    
2. **Use a Small Learning Rate:** Typically $1 \times 10^{-5}$ to $5 \times 10^{-6}$. CLIP is sensitive; a high LR will destroy the pre-trained features (catastrophic forgetting).
    
3. **Large Batch Size:** Contrastive learning relies on having many "negatives" in a batch. If hardware is limited, use **Gradient Accumulation**.
    

---

### 2. SOTA Methods & Techniques

#### A. Semantic Refinement & Angular Margin (**CLIP2SRITR**)

Standard CLIP uses a simple dot product. Recent methods like **CLIP2SRITR (2025)** introduce an **Additive Angular Margin** (similar to ArcFace). This forces the model to not just "separate" images and text, but to create a highly compact cluster for related concepts, significantly boosting **Recall@K**.

#### B. Handling Negation & Composition (**NegCLIP / CLIPGlasses**)

A common failure of CLIP is "bag-of-words" behavior (it can't tell the difference between "a red bike with a blue basket" and "a blue bike with a red basket").

- **Method:** Fine-tune using **Hard Negative Mining**. For every correct caption, include "shuffled" or "negated" captions as negatives in the same batch.
    
- **Source:** _Enabling CLIP to Comprehend Negated Visual Descriptions_ (2026).
    

#### C. Parameter-Efficient Fine-Tuning (PEFT/LoRA)

Instead of updating all billions of parameters, use **LoRA (Low-Rank Adaptation)**. This keeps the original CLIP "knowledge" frozen and only trains small adapter layers.

- **Benefit:** Prevents the model from over-fitting to your specific dataset (e.g., COCO) and maintains its general-purpose "zero-shot" ability.
    

#### D. Feature Map Distillation

Standard CLIP only looks at the global `[CLS]` token. SOTA methods now use **Feature Map Distillation** to force the image encoder to pay attention to spatial tokens (patches). This helps in retrieving images based on small objects mentioned in the text (like "the soccer ball in the basket").

---

### 3. Relevant Sources & Repositories

|**Category**|**Source / Paper**|**Key Link/Identifier**|
|---|---|---|
|**Code (The Best)**|**OpenCLIP**|[GitHub: mlfoundations/open_clip](https://github.com/mlfoundations/open_clip)|
|**Library**|**Hugging Face PEFT**|For LoRA/Adapters implementation|
|**SOTA Paper**|_CLIP-based Semantic Refinement Method_|[CLIP2SRITR (2025)](https://www.google.com/search?q=https://www.researchgate.net/publication/391216548)|
|**SOTA Paper**|_Negated Visual Descriptions_|[arXiv:2602.21035 (2026)](https://www.google.com/search?q=https://arxiv.org/abs/2602.21035)|
|**Benchmark**|**CLIP Benchmark**|[GitHub: LAION-AI/CLIP_benchmark](https://github.com/LAION-AI/CLIP_benchmark)|

---

### Implementation Tip

If you are working on a specific dataset (like the one in your image with "red color bikes"), I recommend starting with **LoRA fine-tuning** on the **MS-COCO** dataset using the **OpenCLIP** library. It is the most stable path to high Recall@10 scores.