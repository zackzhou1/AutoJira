import yaml
from openai import OpenAI

def load_config(config_file='config.yaml'):
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    return config

def generate_text(prompt, config_file='config.yaml'):
    config = load_config(config_file)
    client = OpenAI(api_key=config['open_ai_api_key'],base_url="https://datalab-api.reyrey.net/Api/OpenAI")
    response = client.chat.completions.create(
        model=config['chat_model'],
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    # Example usage if run as a script
    prompt = "Write a short, friendly email inviting a colleague to lunch."
    output = generate_text(prompt)
    print(f"Prompt: {prompt}\nModel output: {output}\n")