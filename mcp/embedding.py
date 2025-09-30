import os

import onnxruntime as ort
from transformers import AutoTokenizer
import numpy as np

# Initiallization: Embedding Model
class EmbeddingModel:
    def __init__(self, model_path, tokenizer):
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer)
        self.session = ort.InferenceSession(model_path)

    def from_CLS_2_Embeddings(self, inputs, last_hidden_state):
        attention_mask = inputs["attention_mask"]
        mask_expanded = np.expand_dims(attention_mask, -1).astype(np.float32)
        sum_embeddings = np.sum(last_hidden_state * mask_expanded, axis=1)
        sum_mask = np.clip(mask_expanded.sum(axis=1), a_min=1e-9, a_max=None)
        mean_pooled = sum_embeddings / sum_mask

        # Normalize
        embeddings = mean_pooled / np.linalg.norm(mean_pooled, axis=1, keepdims=True)

        return embeddings

    def __call__(self, texts):
        inputs = self.tokenizer(texts, return_tensors="np", padding=True, truncation=True)

        # Run ONNX inference
        outputs = self.session.run(
            None,
            {
                "input_ids": inputs["input_ids"],
                "attention_mask": inputs["attention_mask"]
            }
        )
        last_hidden_state, _ = outputs

        # Pooling
        embeddings = self.from_CLS_2_Embeddings(inputs, last_hidden_state)

        return embeddings