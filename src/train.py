import torch
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import LoraConfig
from trl import SFTTrainer, SFTConfig

MODEL_ID = "meta-llama/Llama-3.1-8B-Instruct"   # use a smaller model if VRAM < 12 GB

bnb = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                         bnb_4bit_compute_dtype=torch.float16)
model = AutoModelForCausalLM.from_pretrained(MODEL_ID, quantization_config=bnb,
                                             device_map="auto")
tok = AutoTokenizer.from_pretrained(MODEL_ID)

lora = LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05,
                  target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
                  task_type="CAUSAL_LM")

data = load_dataset("json", data_files={"train": "data/train.jsonl",
                                        "test": "data/test.jsonl"})

trainer = SFTTrainer(
    model=model, peft_config=lora, processing_class=tok,
    train_dataset=data["train"], eval_dataset=data["test"],
    args=SFTConfig(output_dir="outputs/lora", num_train_epochs=2,
                   per_device_train_batch_size=2, gradient_accumulation_steps=8,
                   learning_rate=2e-4, logging_steps=10, fp16=True),
)
trainer.train()
trainer.save_model("outputs/lora")