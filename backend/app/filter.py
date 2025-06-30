# backend/app/filter.py
import pandas as pd

def filter_and_count(df, plan: dict):
    """
    Filters a DataFrame based on a given plan and calculates total counts
    and grouped results.

    Args:
        df (pandas.DataFrame): The input DataFrame to filter.
        plan (dict): A dictionary containing filtering criteria.
                     Example: {"negeri": "Johor", "umur_min": "15", "umur_max": "30"}

    Returns:
        dict: A dictionary containing:
            - "total" (int): The total count after applying all filters.
            - "groups" (list): A list of dictionaries, each representing
                              a grouped result with a label and data.
    """
    df_filtered = df.copy() # Work on a copy to avoid modifying the original DataFrame

    # Initialize mask as a Series of True values for all rows
    mask = pd.Series(True, index=df.index)

    # Define direct filters and their corresponding keys in the plan
    filters_map = {
        'negeri': 'negeri',
        'daerah': 'daerah',
        'jantina': 'jantina',
        'etnik': 'etnik',
        'pekerjaan_utama': 'pekerjaan_utama',
        'oku': 'status_oku', # Map 'oku' column to 'status_oku' in plan
        'pendidikan_tertinggi': 'pendidikan_tertinggi',
    }

    # Apply direct filters
    for df_col, plan_key in filters_map.items():
        val = plan.get(plan_key, 'Any') # Use .get() for safer access
        if val != 'Any':
            # Ensure case-insensitivity for string comparisons if necessary,
            # but for exact matches, direct comparison is fine.
            mask &= (df[df_col] == val)
    
    # Apply age range filters
    umur_min_val = plan.get('umur_min', 'Any')
    umur_max_val = plan.get('umur_max', 'Any')

    if umur_min_val != 'Any':
        try:
            mask &= (df['umur'] >= int(umur_min_val))
        except ValueError:
            print(f"Warning: Invalid umur_min value '{umur_min_val}'. Skipping filter.")
    if umur_max_val != 'Any':
        try:
            mask &= (df['umur'] <= int(umur_max_val))
        except ValueError:
            print(f"Warning: Invalid umur_max value '{umur_max_val}'. Skipping filter.")
    
    # Apply the combined mask to get the filtered DataFrame
    df_filtered = df[mask]
    
    # Calculate the total count
    total = int(df_filtered["COUNT"].sum()) if not df_filtered.empty else 0
    
    # Define fields for grouping results, along with their display labels
    group_fields = {
        'Negeri': 'negeri',
        'Daerah': 'daerah',
        'Jantina': 'jantina',
        'Etnik': 'etnik',
        'Umur': 'umur', # 'umur' here refers to the column, not 'umur_min' or 'umur_max'
        'Status OKU': 'oku',
        'Pekerjaan Utama': 'pekerjaan_utama',
        'Pendidikan Tertinggi': 'pendidikan_tertinggi'
    }

    grouped_results = []

    # Generate grouped results for fields not specified in the plan (i.e., 'Any')
    for label, field_name in group_fields.items():
        # Determine the corresponding key in the 'plan' based on the field_name
        # Special handling for 'oku' to 'status_oku'
        plan_check_key = 'status_oku' if field_name == 'oku' else field_name
        
        # Check if the field was NOT explicitly set in the plan, meaning it's 'Any'
        # Also, ensure 'umur' is only grouped if neither umur_min nor umur_max were set
        if field_name == 'umur':
            if plan.get('umur_min', 'Any') == 'Any' and plan.get('umur_max', 'Any') == 'Any':
                # Group by 'umur' only if no age range was specified
                if not df_filtered.empty:
                    grouped_df = df_filtered.groupby(field_name)['COUNT'].sum().reset_index()
                    # Rename the column to the display label
                    grouped_df.columns = [label, 'COUNT']
                    grouped_results.append({"label": label, "data": grouped_df.to_dict(orient="records")})
        elif plan.get(plan_check_key, 'Any') == 'Any':
            if not df_filtered.empty:
                grouped_df = df_filtered.groupby(field_name)['COUNT'].sum().reset_index()
                # Rename the column to the display label
                grouped_df.columns = [label, 'COUNT']
                grouped_results.append({"label": label, "data": grouped_df.to_dict(orient="records")})

    return {"total": total, "groups": grouped_results}

