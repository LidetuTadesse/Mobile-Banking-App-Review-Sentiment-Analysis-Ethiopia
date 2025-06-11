import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os

def plot_sentiment_distribution(df):
    plt.figure(figsize=(8, 5))
    sns.countplot(data=df, x='sentiment_label', hue='bank_name')
    plt.title("Sentiment Distribution by Bank")
    plt.xlabel("Sentiment")
    plt.ylabel("Count")
    plt.xticks(rotation=0)
    plt.tight_layout()
    os.makedirs("reports", exist_ok=True)  # ensure directory exists
    plt.savefig("reports/sentiment_distribution.png")
    plt.close()

def plot_rating_distribution(df):
    plt.figure(figsize=(8, 5))
    sns.histplot(data=df, x='rating', hue='bank_name', bins=5, multiple='dodge')
    plt.title("Rating Distribution by Bank")
    plt.xlabel("Rating")
    plt.ylabel("Frequency")
    plt.tight_layout()
    os.makedirs("reports", exist_ok=True)  # ensure directory exists
    plt.savefig("reports/rating_distribution.png")
    plt.close()

def generate_wordcloud(df, label='positive'):
    # Normalize label to uppercase to match DataFrame sentiment_label values
    label_upper = label.upper()

    # Extract texts filtered by sentiment label and drop missing values
    texts = df.loc[df['sentiment_label'] == label_upper, 'cleaned_text'].dropna()

    # Join all texts into one string
    text = ' '.join(texts)

    # Check if text is empty to avoid wordcloud error
    if not text.strip():
        print(f"No text found for label '{label_upper}'. Skipping word cloud generation.")
        return

    # Generate and plot the word cloud
    wc = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.title(f"{label.capitalize()} Word Cloud")
    plt.tight_layout()
    os.makedirs("reports", exist_ok=True)  # ensure directory exists
    plt.savefig(f"reports/{label.lower()}_wordcloud.png")
    plt.close()
