---
title: "BERT模型训练实践"
date: 2025-04-21
categories: [AI, AI]
description: ""
---

**平台**：Windows 11 + NVIDIA RTX 4060 + CUDA 12.6 + Miniconda + PyTorch + Hugging Face Transformers

使用 Hugging Face 的 Transformers 库，基于 `bert-base-uncased` 模型进行微调，完成一个**句子评分/分类任务**的训练与预测流程，并使用 GPU 加速训练。

完整代码地址：[https://github.com/Doge2077/learn-bert](https://github.com/Doge2077/learn-bert)

## 技术介绍

### BERT 核心思想

BERT（Bidirectional Encoder Representations from Transformers）是由 Google 在 2018 年提出的预训练语言模型，基于 Transformer 架构。它通过大规模无监督语料进行训练，能够捕捉文本的深层语义和上下文信息。以下是 BERT 的核心原理及其各层功能的详细解析：

### 一、BERT 的核心原理

1.  **双向上下文建模**：
    BERT 通过 Transformer 的自注意力机制（Self-Attention）同时捕捉文本的**双向上下文关系**，克服了传统模型（如 LSTM）单向或简单双向拼接的局限性。

2.  **预训练任务**：
    *   **Masked Language Model (MLM)**：随机遮盖 15% 的输入词，模型预测被遮盖的词（学习上下文依赖）。
    *   **Next Sentence Prediction (NSP)**：判断两个句子是否连续（学习句子间关系）。

3.  **Transformer Encoder 架构**：
    BERT 仅使用 Transformer 的**编码器（Encoder）** 部分，由堆叠的编码器组成，每层包含自注意力机制和前馈神经网络。

### 二、BERT 的层级结构

BERT 模型分为**输入层、嵌入层、多层编码器**。以 BERT-Base 为例（12 层编码器），每一层的作用如下：

#### 1. 输入层（Input Layer）

*   **功能**：将原始文本转换为模型可处理的输入表示。
*   **输入格式**：
    *   `[CLS]`：句首标记，用于分类任务的聚合表示。
    *   `Token Embeddings`：词向量（如 `WordPiece` 分词后的词）。
    *   `Segment Embeddings`：区分句子 A 和句子 B（用于 NSP 任务）。
    *   `Position Embeddings`：位置编码，标记词的位置信息。

#### 2. 嵌入层（Embedding Layer）

*   **功能**：将输入转换为稠密向量。
    *   词嵌入（Token Embeddings）：将词映射到低维向量。
    *   位置嵌入（Position Embeddings）：编码词的位置信息。
    *   分段嵌入（Segment Embeddings）：区分不同句子（如问答任务中的问题和答案）。

#### 3. 编码器层（Encoder Layers）

每层编码器包含两个核心模块：**多头自注意力（Multi-Head Self-Attention）** 和 **前馈神经网络（Feed-Forward Network）**，并通过残差连接和层归一化（LayerNorm）以优化训练。

*   **(1) 多头自注意力机制（Multi-Head Self-Attention）**
    *   **功能**：捕捉词与词之间的全局依赖关系。
    *   **实现**：将输入拆分为多个子空间（如 12 个“头”），每个头独立计算注意力权重，最后拼接结果。
    *   **公式**：
        $$
        \text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
        $$
        （其中 $Q, K, V$ 是查询、键、值矩阵，$d_k$ 是维度）

*   **(2) 前馈神经网络（Feed-Forward Network, FFN）**
    *   **功能**：对自注意力的输出进行非线性变换。
    *   **结构**：两层全连接层（如中间层维度扩大为 4 倍），激活函数为 GELU 或 ReLU。

*   **(3) 残差连接与层归一化**：
    每层输出前均应用残差连接，以缓解梯度消失问题。

### **4. 各编码器层的特点**
- **底层（靠近输入层）**：学习基础语法、局部特征（如词性、短语结构）。
- **中层**：捕捉句内和句间关系（如指代消解、语义角色）。
- **高层**：提取抽象语义（如情感倾向、文本主旨）。

### **3. BERT 的输出**
- **最后一层编码器的输出**：每个词对应的上下文向量。
- `[CLS]` 向量：用于分类任务（如情感分析），聚合全局信息。
- 其他词向量：用于序列标注（如命名实体识别）、问答等任务。

## 环境配置

| 项目 | 说明 |
| :--- | :--- |
| 平台 | Windows 11 + NVIDIA RTX 4060 + CUDA 12.6 + Miniconda + PyTorch + Hugging Face Transformers |
| 安装参考 | [Miniconda安装文档](https://www.anaconda.com/docs/getting-started/miniconda/install#power-shell) |
| 安装命令 | `conda create -n ai python=3.12 -y`&lt;br&gt;`conda activate ai` |
| PyTorch安装 | 请访问 [PyTorch官网](https://pytorch.org/) 选择对应版本，示例命令如下：&lt;br&gt;`pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126` |
| 验证命令 | `python -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"` |
| 预期输出 | `2.6.0+cu126`&lt;br&gt;`True` |

## 项目结构

```
my_transformer_demo/
├── config.json
├── data/
│   └── dataset.csv
├── train.py
├── utils.py
```

## 配置文件 `config.json`
```json
{
  "model_name": "bert-base-uncased",
  "max_length": 128,
  "train_batch_size": 8,
  "eval_batch_size": 8,
  "num_train_epochs": 3,
  "learning_rate": 2e-5,
  "output_dir": "./models",
  "num_labels": 5
}
```

## 数据集 `data/dataset.csv`
```text
sentence,score
"The weather is perfect today!",5
"This restaurant serves awful food.",1
"I'm so happy with my new phone.",5
"The concert was mediocre at best.",3
...
```

## 工具函数 `utils.py`
```python
import pandas as pd
from datasets import Dataset

def load_dataset(path):
    df = pd.read_csv(path)
    df['label'] = df['score'] - 1  # 评分1~5 → label 0~4
    return Dataset.from_pandas(df[['sentence', 'label']])
```

## 训练脚本 `train.py`
```python
import json

import torch
from transformers import BertTokenizer, BertForSequenceClassification, TrainingArguments, Trainer, DataCollatorWithPadding
from sklearn.metrics import accuracy_score

from utils import load_dataset

print(torch.cuda.is_available())

# ========== 设备检测 ==========
device = "cuda" if torch.cuda.is_available() else "cpu"
if device == "cuda":
    print(f"🚀 使用 GPU：{torch.cuda.get_device_name(0)}")
    print(f"显存占用：{torch.cuda.memory_allocated() / 1024 ** 2:.2f} MB")
else:
    print("未检测到 GPU，使用 CPU 训练")

# ========== 加载配置 ==========
with open("config.json") as f:
    cfg = json.load(f)

# ========== 加载数据 ==========
tokenizer = BertTokenizer.from_pretrained(cfg["model_name"])
dataset = load_dataset("data/dataset.csv")

def tokenize(example):
    return tokenizer(example["sentence"], truncation=True, max_length=cfg["max_length"])

tokenized_dataset = dataset.map(tokenize, batched=True)
tokenized_dataset = tokenized_dataset.train_test_split(test_size=0.2)

# ========== 加载模型 ==========
model = BertForSequenceClassification.from_pretrained(
    cfg["model_name"],
    num_labels=cfg["num_labels"]
).to(device)

# ========== 评估指标 ==========
def compute_metrics(eval_pred):
    logits, labels = eval_pred.predictions, eval_pred.label_ids
    preds = logits.argmax(axis=-1)
    acc = accuracy_score(labels, preds)
    return {"accuracy": acc}

# ========== 训练参数 ==========
args = TrainingArguments(
    output_dir=cfg["output_dir"],
    per_device_train_batch_size=cfg["train_batch_size"],
    per_device_eval_batch_size=cfg["eval_batch_size"],
    num_train_epochs=cfg["num_train_epochs"],
    learning_rate=cfg["learning_rate"],
    save_strategy="epoch",
    logging_dir='./logs',
    report_to=["none"],
    evaluation_strategy="epoch",
    load_best_model_at_end=True,
)

# ========== 显存监控 Hook ==========
from transformers import TrainerCallback

class PrintMemoryCallback(TrainerCallback):
    def on_epoch_begin(self, args, state, control, **kwargs):
        if torch.cuda.is_available():
            mem = torch.cuda.memory_allocated() / 1024 ** 2
            print(f"Epoch {state.epoch:.0f} 开始，当前显存占用：{mem:.2f} MB")

# ========== 启动训练器 ==========
trainer = Trainer(
    model=model,
    args=args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["test"],
    tokenizer=tokenizer,
    data_collator=DataCollatorWithPadding(tokenizer),
    compute_metrics=compute_metrics,
    callbacks=[PrintMemoryCallback()]
)

trainer.train()
# ========== 保存模型 ==========
trainer.save_model(cfg["output_dir"])
tokenizer.save_pretrained(cfg["output_dir"])
print("✅ 模型和分词器保存成功！")
```

### 使用模型 `predict.py`
模型会保存到 `./models/`。

```python
import sys
import torch
from transformers import BertTokenizer, BertForSequenceClassification

model_path = "models"
tokenizer = BertTokenizer.from_pretrained(model_path)
model = BertForSequenceClassification.from_pretrained(model_path)

def predict(sentence):
    inputs = tokenizer(sentence, return_tensors="pt", truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        # label 0~4 → score 1~5
        score = torch.argmax(probs) + 1
        return score.item()

if __name__ == "__main__":
    sentence = " ".join(sys.argv[1:]) or "This is a test."
    print(f"Score: {predict(sentence)}")
```