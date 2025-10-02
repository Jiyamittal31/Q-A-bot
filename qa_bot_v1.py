from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer, conversation, ConversationalPipeline

model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

chatbot = pipeline(model=model, tokenizer=tokenizer)

def ask_question(question):
    conversation = chatbot(question)
    return conversation[0]['generated_text']

def main():
    print("🤖 AI Q&A Bot| \n type 'exit' to quit\n")

    while True:
        user_input = input("You: ")

        if user_input.strip().lower() in ["exit", "quit", "bye"]:
            print("Bot: Goodbye! 👋")
            break

        if not user_input.strip():
            print("⚠️ Please enter a valid question.")
            continue

        answer = ask_question(user_input)
        print(f"Bot: {answer}\n")

if __name__ == "__main__":
    main()
