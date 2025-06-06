import tkinter as tk
from tkinter import scrolledtext
from transformers import T5Tokenizer, T5ForConditionalGeneration

tokenizer = T5Tokenizer.from_pretrained("t5-base")
model = T5ForConditionalGeneration.from_pretrained("t5-base")


default_article = (
    "Artificial Intelligence (AI) is a branch of computer science focused on building smart machines capable of "
    "performing tasks that typically require human intelligence. It includes technologies like machine learning, "
    "deep learning, natural language processing, and robotics. AI is increasingly used in sectors like healthcare, "
    "finance, transportation, and customer service."
)

def summarize_article():
    user_input = input_area.get("1.0", tk.END).strip()

    if not user_input:
        return 

    formatted_input = "summarize: " + user_input
    encoded_input = tokenizer.encode(formatted_input, return_tensors="pt", max_length=1024, truncation=True)

    generated_output = model.generate(
        encoded_input,
        length_penalty=1.0,
        num_beams=4,
        early_stopping=True
    )

    final_summary = tokenizer.decode(generated_output[0], skip_special_tokens=True)

    output_area.delete("1.0", tk.END)
    output_area.insert(tk.END, final_summary)

root = tk.Tk()
root.title("Task 1 – Article Summarizer")
root.geometry("860x620")
root.configure(bg="#38602A")

font_label = ("Segoe UI", 11)
font_text = ("Segoe UI", 10)
button_style = {
    "bg": "#00FFFF",
    "fg": "black",
    "font": font_label,
    "cursor": "hand2"
}

tk.Label(root, text="Paste or Edit Article Below (Up to ~1000 words):", font=font_label, bg="#38602A", fg="white").pack(pady=5)
input_area = scrolledtext.ScrolledText(root, width=95, height=14, font=font_text, wrap=tk.WORD)
input_area.pack(padx=10, pady=5)
input_area.insert(tk.END, default_article)

tk.Button(root, text="Summarize ✨", command=summarize_article, **button_style).pack(pady=10)

tk.Label(root, text="Summary Output:", font=font_label, bg="#38602A", fg="white").pack(pady=5)
output_area = scrolledtext.ScrolledText(root, width=95, height=8, font=font_text, wrap=tk.WORD)
output_area.pack(padx=10, pady=(0, 15))

def summarize_on_start():
    formatted_input = "summarize: " + default_article
    encoded = tokenizer.encode(formatted_input, return_tensors="pt", max_length=1024, truncation=True)
    output_ids = model.generate(encoded, length_penalty=1.0, num_beams=4, early_stopping=True)
    result = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    output_area.insert(tk.END, result)

summarize_on_start()

root.mainloop()
