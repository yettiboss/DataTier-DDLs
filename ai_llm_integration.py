import os
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments
from datasets import Dataset
def load_sql_scripts(directory):
    data = []
    for filename in os.listdir(directory):
        if filename.endswith(".sql"):
            with open(os.path.join(directory, filename), 'r') as file:
                data.append({"text": file.read()})
    return Dataset.from_dict({"text": data})
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')

def tokenize_function(examples):
    return tokenizer(examples['text'], truncation=True, padding=True)

dataset = load_sql_scripts("path_to_your_sql_scripts")
tokenized_dataset = dataset.map(tokenize_function, batched=True)
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    num_train_epochs=3,
    per_device_train_batch_size=2,
    save_steps=10_000,
    save_total_limit=2,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
)

trainer.train()
def generate_sql(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(inputs.input_ids, max_length=100)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Example usage
prompt = "CREATE TABLE users ("
generated_sql = generate_sql(prompt)
print(generated_sql)
