import wikipediaapi

def search_wikipedia(subject):
    # Set a proper User-Agent string
    user_agent = "JarvisAI/1.0 (https://yourwebsite.com; contact@yourwebsite.com)"
    wiki_wiki = wikipediaapi.Wikipedia('en', user_agent=user_agent)

    page = wiki_wiki.page(subject)

    if page.exists():
        say(f"Here is what I found on Wikipedia about {subject}:")
        say(page.summary[0:60])  # Adjust the length as needed
        print(page.summary)
    else:
        say(f"Sorry, I couldn't find any information on Wikipedia about {subject}.")
        print("Page does not exist.")
