from transformers import pipeline

# Choose a model with a language modeling head (adjust based on needs)
generator = pipeline("text-generation", model="gpt2")
TF_ENABLE_ONEDNN_OPTS=0
def generate_output(prompt, max_length=150, top_k=10):
  try:
    # Generate text with adjustments
    response = generator(prompt, max_length=max_length,  
                          num_return_sequences=1,  # Generate only 1 response
                          do_sample=True,  # Enable sampling
                          top_k=top_k)  # Consider top k most probable tokens

    return response[0]['generated_text'].strip()
  except Exception as e:
    print("Error:", e)
    return None

if __name__ == "__main__":
  prompt = input("Enter your prompt: ")
  output = generate_output(prompt)
  if output:
    print("Hugging Face Output:", output)
