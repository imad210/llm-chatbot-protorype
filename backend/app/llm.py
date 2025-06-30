# backend/app/llm.py
from openai import OpenAI
import os
import logging # Import logging for better output than print
from .config import OPENAI_API_KEY

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the OpenAI client once.
# The API key is loaded from config.py, which gets it from the environment.
client = OpenAI(api_key=OPENAI_API_KEY)

def ask_gpt_to_plan(user_query: str) -> str:
    """
    Sends a user query to GPT-3.5-turbo to generate a data filtering plan
    in JSON format.

    Args:
        user_query (str): The user's natural language question about the data.

    Returns:
        str: A JSON string representing the filtering plan.
    """
    system_prompt = """
You are a smart data analyst. Your task is to interpret user queries (in Malay or English)
and extract relevant demographic filtering rules. You must always output a JSON object
containing the specified fields. If a field is not mentioned or implied by the query,
set its value to 'Any'.

## Output Fields and Their Values:
- "negeri": String (e.g., "Johor", "W.P. Kuala Lumpur", "Any")
- "daerah": String (e.g., "Johor Bahru", "Any")
- "umur_min": String (numeric string, e.g., "15", "Any")
- "umur_max": String (numeric string, e.g., "30", "Any")
- "jantina": String ("Lelaki", "Perempuan", "Any")
- "etnik": String (e.g., "Melayu", "Cina", "India", "Lain-lain", "Any")
- "status_oku": String ("OKU", "Bukan OKU", "Any")
- "pekerjaan_utama": String (e.g., "Pelajar", "Pekerja Swasta", "Menganggur", "Suri Rumah", "Any")
- "pendidikan_tertinggi": String (e.g., "menengah atas", "ijazah sarjana muda atau yang setaraf", "Any")

## Shortform mapping for 'negeri':
- "kl" or "KL" → "W.P. Kuala Lumpur"
- "pj" or "PJ" → "W.P. Putrajaya"
- "n9" or "ns" → "Negeri Sembilan"
- "p.Pinang" or "Penang" (case-insensitve) → "Pulau Pinang"
- "Sabah" -> "Sabah" (No change)
- "Sarawak" -> "Sarawak" (No change)
- "Kedah" -> "Kedah" (No change)
- "Kelantan" -> "Kelantan" (No change)
- "Melaka" -> "Melaka" (No change)
- "Pahang" -> "Pahang" (No change)
- "Perak" -> "Perak" (No change)
- "Perlis" -> "Perlis" (No change)
- "Selangor" -> "Selangor" (No change)
- "Terengganu" -> "Terengganu" (No change)

## Recognize Malay demographic terms for 'umur':
- "belia" → umur between 15 and 30
- "bawah umur" or "budak sekolah" → umur less than 18 (umur_max: "17")
- "kanak-kanak" or "budak" → umur less than or equal 12 (umur_max: "12")
- "remaja" → umur between 13 and 19 (umur_min: "13", umur_max: "19")
- "dewasa" → umur more than 18 (umur_min: "18")
- "warga emas" or "orang tua" → umur 60 and above (umur_min: "60")

## Recognize this for 'pekerjaan_utama':
- "swasta" → "Pekerja Swasta"
- "gomen" → "Pekerja Kerajaan"
- "anggur", "tidak bekerja", "tiada pekerjaan" → "Menganggur"
- "suri rumah" -> "Suri Rumah"

## Recognize this for 'pendidikan_tertinggi':
- "SPM" → "Menengah Atas"
- "Degree" → "Ijazah Sarjana Muda atau yang setaraf"
- "Master" → "Ijazah Sarjana atau yang setaraf"
- "Phd" → "Ijazah Kedoktoran atau yang setaraf"
- "PMR" -> "Menengah Rendah"
- "UPSR" -> "Rendah"
- "Tiada Pendidikan Formal" -> "Tiada Pendidikan Formal"
- "Lain-lain" -> "Lain-lain"

## Output Format:
Return your output strictly in this JSON format. No extra text or markdown outside the JSON.
```json
{
  "negeri": "Any",
  "daerah": "Any",
  "jantina": "Any",
  "umur_min": "Any",
  "umur_max": "Any",
  "etnik": "Any",
  "status_oku": "Any",
  "pekerjaan_utama": "Any",
  "pendidikan_tertinggi": "Any"
}
```
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # You can make this configurable via config.py if needed
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            response_format={"type": "json_object"} # Ensure JSON output
        )
        # Log the full response for debugging
        logging.info(f"GPT Response: {response.choices[0].message.content}")
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error calling OpenAI API: {e}")
        # Re-raise the exception or return a structured error response
        raise

