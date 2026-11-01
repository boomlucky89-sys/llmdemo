# ShopKart LLM

A small chat fine-tuning starter using Hugging Face Transformers and PEFT LoRA. The included raw conversations are synthetic examples; replace them with approved, representative data before training.

## Setup

Use Python 3.10 or newer. Install a PyTorch build suitable for your hardware, then install the project dependencies:

```powershell
python -m pip install -r requirements.txt
```

For CUDA training, install the matching PyTorch/CUDA build from the official PyTorch instructions before installing the remaining requirements if needed.

## Data format

Each JSONL line is one conversation with a non-empty `messages` array. Every message has a `role` (`system`, `user`, or `assistant`) and string `content`:

```json
{"messages":[{"role":"user","content":"Where is my order?"},{"role":"assistant","content":"Please share your order number so I can help."}]}
```

Prepare a deterministic split from `data/raw_chats.jsonl`:

```powershell
python src/prepare_data.py --test-size 0.2 --seed 42
```

The script writes `data/train.jsonl` and `data/test.jsonl`. It keeps at least one test conversation when there are two or more records and test size is greater than zero.

## Fine-tune

The default base model is `Qwen/Qwen2.5-0.5B-Instruct`. Override it to use another compatible causal language model:

```powershell
python src/train.py --model Qwen/Qwen2.5-0.5B-Instruct --epochs 3
```

The LoRA adapter and tokenizer are saved under `outputs/adapter`. Training defaults are intended as a starting point; adjust batch size and sequence length for available memory.

## Merge and evaluate

Merge the adapter into the base model:

```powershell
python src/merge.py
```

Run the test prompts against the base model, a merged model, or the adapter:

```powershell
python src/evaluate.py --model outputs/merged
python src/evaluate.py --adapter outputs/adapter
```

Evaluation prints expected and generated responses for manual inspection; it does not calculate an automated quality score.

## Chat API

The FastAPI service expects an OpenAI-compatible endpoint at `http://localhost:11434/v1` and a model named `shopkart` to be available there. Start the compatible local server and model first, then run:

```powershell
uvicorn src.app:app --reload
```

Send a JSON request to `http://localhost:8000/chat` with a `message` field. The `/chat/stream` endpoint streams generated text. The service masks basic phone/card-number-like strings and email addresses before sending the message to the model. The OpenAI Python SDK is used as the client for the compatible local endpoint.
