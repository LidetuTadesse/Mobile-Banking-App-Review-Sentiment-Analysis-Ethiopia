# task4_main.py
from insights.data_loader import load_reviews
from insights.insights_generator import extract_drivers_pain_points, compare_banks
from insights.visualizer import (
    plot_sentiment_distribution,
    plot_rating_distribution,
    generate_wordcloud
)

def main():
    print("Loading data...")
    df = load_reviews()
    print("Columns in DataFrame:", df.columns.tolist())
    print("Data types:\n", df.dtypes)
    print("First row as dict:\n", df.iloc[0].to_dict())
    print("Sample data:\n", df.head())
    print("Generating insights...")
    drivers, pains = extract_drivers_pain_points(df)
    for bank in drivers:
        print(f"\nBank: {bank}")
        print("Drivers (Positive Samples):")
        for d in drivers[bank]:
            print(" -", d)
        print("Pain Points (Negative Samples):")
        for p in pains[bank]:
            print(" -", p)

    print("\nComparing banks on ratings and sentiment:")
    print(compare_banks(df))

    print("\nGenerating visualizations...")
    plot_sentiment_distribution(df)
    plot_rating_distribution(df)
    generate_wordcloud(df, 'positive')
    generate_wordcloud(df, 'negative')
    print("Visualizations saved in 'reports/' folder.")

if __name__ == "__main__":
    main()