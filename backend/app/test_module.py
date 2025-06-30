from data_loader import load_data
df, texts = load_data()
print(f"Loaded {len(df)} rows and {len(texts)} texts")