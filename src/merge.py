import torch
from peft import AutoPeftModelForCausalLM
from transformers import AutoTokenizer

m = AutoPeftModelForCausalLM.from_pretrained("outputs/lora", torch_dtype=torch.float16)
m = m.merge_and_unload()
m.save_pretrained("outputs/merged")
AutoTokenizer.from_pretrained("outputs/lora").save_pretrained("outputs/merged")