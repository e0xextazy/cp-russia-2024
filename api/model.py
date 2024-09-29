from transformers import AutoConfig, AutoModel, AutoTokenizer
import torch.nn as nn
import torch
import pickle
import numpy as np
import torch.nn.functional as F


def pool(hidden_state, mask, pooling_method="csl"):
    if pooling_method == "mean":
        s = torch.sum(hidden_state * mask.unsqueeze(-1).float(), dim=1)
        d = mask.sum(axis=1, keepdim=True).float()
        return s / d
    elif pooling_method == "cls":
        return hidden_state[:, 0]


def prepare_input(text):
    inputs = tokenizer.encode_plus(
        text,
        return_tensors=None,
        add_special_tokens=True,
        max_length=512,
        pad_to_max_length=True,
        truncation=True,
    )
    for k, v in inputs.items():
        inputs[k] = torch.tensor([v], dtype=torch.long)
    return inputs


class CustomModel(nn.Module):
    def __init__(self, name):
        super().__init__()
        self.model = AutoModel.from_pretrained(name)
        self.config = AutoConfig.from_pretrained(name)
        self.fc_class1 = nn.Linear(self.config.hidden_size, 11)
        self.fc_class2 = nn.Linear(self.config.hidden_size, 39)

    def feature(self, inputs):
        outputs = self.model(**inputs)
        embeddings = pool(
            outputs.last_hidden_state, 
            inputs["attention_mask"],
            pooling_method="cls" # or try "mean"
        )
        return F.normalize(embeddings, p=2, dim=1)

    def forward(self, inputs):
        feature = self.feature(inputs)
        class1 = self.fc_class1(feature)
        class2 = self.fc_class2(feature)

        return class1, class2


def setup():
    model_name = "ai-forever/ru-en-RoSBERTa"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = CustomModel(model_name)
    state = torch.load(
        "api/encoder_model/ai-forever-ru-en-RoSBERTa_fold0_best.pth",
        map_location=torch.device("cpu"),
    )
    model.load_state_dict(state["model"])
    model.eval()

    return model, tokenizer


model, tokenizer = setup()
with open("api/encoder_model/class1_le.pkl", "rb") as f:
    class1_le = pickle.load(f)
with open("api/encoder_model/class2_le.pkl", "rb") as f:
    class2_le = pickle.load(f)


def get_predicts(text):
    inputs = prepare_input(text)
    class1_probs, class2_probs = model(inputs)
    class1 = np.argmax(class1_probs.detach())
    class2 = np.argmax(class2_probs.detach())
    class1_name = class1_le.inverse_transform([class1])[0]
    class2_name = class2_le.inverse_transform([class2])[0]

    return class1_name, class2_name
