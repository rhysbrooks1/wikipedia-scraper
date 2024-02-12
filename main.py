import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from collections import Counter


def word_frequency(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    for ref_section in soup.find_all("div", {"class": "reflist"}):
        ref_section.decompose()

    text = soup.get_text()

    words = text.split()

    for i in range(0, len(words)):
        words[i] = normalize_word(words[i])

    word_count = Counter(words)

    stop_words = set(line.strip() for line in open('stopwords.txt'))
    word_count = {word: count for word, count in word_count.items() if word.lower() not in stop_words}

    most_common_words = Counter(word_count).most_common(20)
    
    return most_common_words

def normalize_word(word):

    word = word.lower()

    if word.endswith("'s"):
        word = word[:-2]

    return word

def main():
    try:
    # Input Wikipedia URL
        url = input("Enter Wikipedia URL: ")
        
        # Perform word frequency analysis
        most_common_words = word_frequency(url)
        
        # Display the most common words in a bar chart
        words, frequencies = zip(*most_common_words)

        plt.figure(facecolor='lightgrey')
        plt.bar(words, frequencies)
        plt.xlabel('Words')
        plt.ylabel('Frequency')
        plt.title('Top 20 Most Common Words')
        plt.xticks(rotation = 90)
        plt.tight_layout()

        plt.show()

    
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()