
import sys
import re

# ============================================================
# 1. Attempt to load a small, fast neural model
# ============================================================
try:
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import torch

    # Choose your model: 
    # - "distilgpt2" (smallest, fastest, ~82M parameters)
    # - "microsoft/DialoGPT-small" (more coherent, ~124M parameters)
    # - "microsoft/DialoGPT-medium" (better but slower, ~355M parameters)
    MODEL_NAME = "distilgpt2"   # Efficient default
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

    # Set pad token (DistilGPT2 doesn't have one by default)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # Move model to CPU (explicit, but default is CPU anyway)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()  # Set to evaluation mode for inference

    # Conversation history
    chat_history_ids = None
    NEURAL_AVAILABLE = True
    print(f"Neural model '{MODEL_NAME}' loaded on {device}.", file=sys.stderr)

except ImportError:
    NEURAL_AVAILABLE = False
    print("Transformers not installed. Falling back to advanced rule‑based bot.", file=sys.stderr)
    print("To use the neural model, run: pip install transformers torch", file=sys.stderr)

# ============================================================
# 2. Fast rule‑based fallback (optimised version)
# ============================================================
# This is a stripped‑down, efficient rule engine with context memory.
# (No sklearn dependency – pure Python for speed and reliability.)

context = {"name": None}

# Pre‑compiled regex patterns for speed
patterns = [
    (re.compile(r'hello|hi|hey', re.I), "Hello! How can I help you?"),
    (re.compile(r'how are you', re.I), "I'm just code, but I'm functioning perfectly!"),
    (re.compile(r'your name|who are you', re.I), "I'm a Python chatbot. You can call me PyBot."),
    (re.compile(r'what can you do', re.I), "I respond to greetings, remember your name, and answer basic questions."),
    (re.compile(r'bye|goodbye|exit', re.I), "Goodbye! Have a great day."),
    (re.compile(r'thanks|thank you', re.I), "You're welcome!"),
    (re.compile(r'help', re.I), "I understand greetings and name remembering. Try 'my name is ...'."),
]

def fast_rule_response(user_input):
    """Return a response if any regex matches (first match wins)."""
    for pattern, response in patterns:
        if pattern.search(user_input):
            return response
    return None

def handle_context_fast(user_input):
    """Very fast name handling without complex NLP."""
    global context
    lower_input = user_input.lower()
    if "my name is" in lower_input:
        # Simple extraction: take everything after "my name is"
        name = lower_input.split("my name is")[-1].strip().title()
        context["name"] = name
        return f"Nice to meet you, {name}!"
    if "what is my name" in lower_input or "what's my name" in lower_input:
        if context["name"]:
            return f"Your name is {context['name']}."
        else:
            return "I don't know your name yet. Tell me with 'My name is ...'."
    return None

def get_fallback_response(user_input):
    """Combine context and rule matching for fallback."""
    # Context first
    ctx = handle_context_fast(user_input)
    if ctx:
        return ctx
    # Then rule patterns
    rule = fast_rule_response(user_input)
    if rule:
        return rule
    # Default
    return "I'm not sure how to respond to that. Try saying 'hello' or 'help'."

# ============================================================
# 3. Main chat loop – efficient neural generation with caching
# ============================================================
def chat():
    print("=" * 60)
    print("     EFFICIENT HUGE‑LEVEL CHATBOT (Simple Mode)")
    print("=" * 60)
    print("Type 'bye', 'exit', or 'quit' to end the conversation.\n")

    global chat_history_ids

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["bye", "exit", "quit"]:
            print("ChatBot: Goodbye!")
            break
        if not user_input:
            continue

        if NEURAL_AVAILABLE:
            # --- Neural response generation (optimised) ---
            # Encode input and move to same device as model
            new_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt').to(device)

            # Concatenate with history (if any)
            if chat_history_ids is not None:
                # Ensure history is on the same device
                chat_history_ids = chat_history_ids.to(device)
                bot_input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1)
            else:
                bot_input_ids = new_input_ids

            # Generate response with conservative settings for speed
            with torch.no_grad():  # Disable gradient calculation for inference
                chat_history_ids = model.generate(
                    bot_input_ids,
                    max_length=bot_input_ids.shape[-1] + 50,  # Limit new tokens
                    pad_token_id=tokenizer.eos_token_id,
                    do_sample=True,
                    top_p=0.9,
                    top_k=40,
                    temperature=0.8,
                    no_repeat_ngram_size=3
                )

            # Decode only the newly generated part
            response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
            print(f"ChatBot: {response}")
        else:
            # --- Fast fallback response ---
            response = get_fallback_response(user_input)
            print(f"ChatBot: {response}")

if __name__ == "__main__":
    chat()
