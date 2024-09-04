import openai
from config import apikey  # Ensure you have a file named config.py with your OpenAI API key

def generate_content(prompt):
    openai.api_key = apikey
    try:
        response = openai.Completion.create(
            model="text-davinci-003",  # You can use the model you prefer
            prompt=prompt,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        response_text = response.choices[0].text.strip()
        return response_text
    except Exception as e:
        print(f"Error generating content: {e}")
        return "Sorry, I couldn't generate the content."

def write_to_file(filename, content):
    with open(filename, "w") as file:
        file.write(content)
    print(f"Content written to {filename}")

def create_context(query):
    # Determine the type of content to create based on the query
    if "write a mail regarding holiday" in query.lower():
        prompt = (
            "Write a formal email requesting holiday leave. Include a subject line, greeting, body, and closing."
        )
        filename = "Holiday_Leave_Request.txt"
    else:
        print("Unsupported request. Please provide a valid context.")
        return

    content = generate_content(prompt)
    write_to_file(filename, content)

if __name__ == "__main__":
    user_query = input("Enter your query: ")
    create_context(user_query)
