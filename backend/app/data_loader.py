# backend/app/data_loader.py
import pandas as pd
from .config import CSV_FILE

def safe_value(val, default='Tiada Data'):
    """
    Safely returns a value, replacing NaN or common 'no data' strings with a default.
    
    Args:
        val: The value to check.
        default: The default string to return if the value is considered missing.
    
    Returns:
        The original value or the default string.
    """
    if pd.isna(val) or str(val).strip().upper() in ['NA', '?', 'N/A', 'NONE']: # Added more common missing value indicators
        return default
    return val

def load_data():
    """
    Loads the demographic data from the specified CSV file and converts each row into a text string.
    
    Returns:
        tuple: A tuple containing:
            - pandas.DataFrame: The loaded DataFrame.
            - list[str]: A list of text representations for each row.
    """
    try:
        df = pd.read_csv(CSV_FILE)
        # Ensure 'COUNT' column is numeric, fill NaNs with 0 to prevent errors during sum
        df['COUNT'] = pd.to_numeric(df['COUNT'], errors='coerce').fillna(0)
    except FileNotFoundError:
        print(f"Error: CSV file not found at {CSV_FILE}. Please check your config.py and file path.")
        raise
    except Exception as e:
        print(f"Error loading or processing CSV file: {e}")
        raise

    def row_to_text(row):
        """
        Converts a single DataFrame row into a human-readable text string.
        """
        return (
            f"Jantina: {safe_value(row['jantina'])}, Umur: {safe_value(row['umur'])}, "
            f"Daerah: {safe_value(row['daerah'])}, Negeri: {safe_value(row['negeri'])}, "
            f"Etnik: {safe_value(row['etnik'])}, OKU: {safe_value(row['oku'])}, "
            f"Pendidikan Tertinggi: {safe_value(row['pendidikan_tertinggi'])}, "
            f"Pekerjaan: {safe_value(row['pekerjaan_utama'])}, Jumlah: {safe_value(row['COUNT'])}"
        )

    texts = df.apply(row_to_text, axis=1).tolist()
    return df, texts

