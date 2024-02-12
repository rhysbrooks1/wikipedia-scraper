import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from collections import Counter
from textblob import TextBlob
import matplotlib.patches as patches

def extract_words(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    for ref_section in soup.find_all("div", {"class": "reflist"}):
        ref_section.decompose()

    text = soup.get_text()

    words = text.split()

    for i in range(0, len(words)):
        words[i] = normalize_word(words[i])

    return words


def word_frequency(words):
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


def sentiment_score(words):
    total_sentiment_score = 0

    for word in words:
        sentiment_score = TextBlob(word).sentiment.polarity
        total_sentiment_score += sentiment_score

    average_sentiment_score = total_sentiment_score / len(words)

    return average_sentiment_score


def sentiment_score_to_color(avgScore):
    if avgScore <= -0.25:
        # Strong negative sentiment (Red)
        return (1, 0, 0)
    elif -0.25 < avgScore <= 0:
        # Slight negative sentiment (Red to Yellow transition)
        return (1, 1 + 4 * avgScore, 0)
    elif 0 < avgScore <= 0.1:
        # Slight negative to neutral transition (Yellow)
        return (1 - 10 * avgScore, 1, 0)
    elif 0.1 < avgScore <= 0.2:
        # Neutral sentiment (Yellow to Green transition)
        return (0, 1, 10 * avgScore - 1)
    elif 0.2 < avgScore < 0.3:
        # Neutral to good transition (Green)
        return (0, 1 - 10 * (avgScore - 0.2), 1)
    elif avgScore >= 0.3:
        # Good to very positive sentiment (Green to Blue transition)
        return (0, 10 * (avgScore - 0.3), 1)

def main():
    try:

        url = input("Enter Wikipedia URL: ")
        wordList = extract_words(url)
        
        # Perform word frequency analysis
        most_common_words = word_frequency(wordList)
        sentiment = sentiment_score(wordList)
        print(sentiment_score(wordList))

        # Display the most common words in a bar chart
        words, frequencies = zip(*most_common_words)

        plt.figure()
        plt.bar(words, frequencies)
        plt.xlabel('Words')
        plt.ylabel('Frequency')
        plt.title('Top 20 Most Common Words')
        plt.xticks(rotation = 90)
        plt.tight_layout()

        ax = plt.gca()
        ax.add_patch(patches.Rectangle((.6, .8), 0.5, 0.5, facecolor=sentiment_score_to_color(sentiment), edgecolor='black', transform=ax.transAxes))
        ax.text(0.6, 0.68, "Sentiment Gradient \n Red is negative, Green is positive", transform=ax.transAxes, fontsize=10, verticalalignment='bottom')

        plt.show()

    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()
