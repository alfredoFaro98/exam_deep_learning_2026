import pandas as pd
import numpy as np
import os

def count_lines(filepath):
    """
    Counts lines in a file rapidly using a buffer, avoiding loading the whole file into RAM.
    """
    try:
        with open(filepath, 'rb') as f:
            lines = 0
            buf_size = 1024 * 1024
            read_f = f.read
            buf = read_f(buf_size)
            while buf:
                lines += buf.count(b'\n')
                buf = read_f(buf_size)
            return lines
    except Exception:
        return 0

def validate_file_structure(filepath, sep, expected_cols, file_type):
    """
    Validates file existence, line count, and column count (reading only first 5 rows).
    """
    res = {'status': 'Pending', 'shape': None, 'details': []}
    
    if not os.path.exists(filepath):
        res['status'] = 'Missing'
        res['details'].append(f'{file_type} file not found.')
        return res, 0, 0

    try:
        # 1. Fast Line Count (Raw I/O)
        n_rows = count_lines(filepath)
        
        # 2. Fast Header/Column Check (Pandas with nrows)
        # We assume no header in the file based on previous context, so header=None
        try:
            df_preview = pd.read_csv(filepath, header=None, sep=sep, nrows=5)
        except:
            # Fallback for separator issues
            df_preview = pd.read_csv(filepath, header=None, sep=None, engine='python', nrows=5)
            
        # Check for Timestamp column (col 0) removal necessity
        # We simulate the removal to see if the rest matches
        n_cols_raw = df_preview.shape[1]
        n_cols_data = n_cols_raw - 1 # We always drop the first timestamp column
        
        # Capture Preview Data (First 5 rows, first 6 cols + last 3 cols if wide)
        # Convert to list of lists
        # We handle just the raw values for display
        # Slicing: Col 0 (Time) + Next 5 cols ...
        preview = []
        if n_cols_raw > 10:
             # Show first 6 columns (Time + 5 vals)
             preview_df = df_preview.iloc[:, :7]
             preview = preview_df.values.tolist()
        else:
             preview = df_preview.values.tolist()

        formatted_preview = []
        for row in preview:
            # Round floats for nice display
            formatted_row = []
            for val in row:
                try:
                    formatted_row.append(f"{float(val):.4f}")
                except:
                    formatted_row.append(str(val))
            formatted_preview.append(formatted_row)

        res['preview'] = formatted_preview
        res['preview_hidden_cols'] = (n_cols_raw > 10)

        res['details'].append(f'File exists. Total rows: {n_rows}')
        res['details'].append(f'Detected columns: {n_cols_raw} (will drop timestamp -> {n_cols_data})')

        # Check Column Match
        if n_cols_data == expected_cols:
            res['status'] = 'Success'
            res['shape'] = (n_rows, n_cols_data)
        elif n_cols_data > expected_cols:
            res['status'] = 'Warning'
            res['shape'] = (n_rows, n_cols_data)
            res['details'].append(f'Extra columns detected ({n_cols_data} > {expected_cols}). Will require slicing.')
            # Treating as success-ish for the dashboard view
        else:
            res['status'] = 'Error'
            res['shape'] = (n_rows, n_cols_data)
            res['details'].append(f'Column mismatch! Expected {expected_cols}, got {n_cols_data}')

        return res, n_rows, n_cols_data

    except Exception as e:
        res['status'] = 'Error'
        res['details'].append(f'Error reading file: {str(e)}')
        return res, 0, 0


def load_and_validate_data(data_dir):
    """
    Lightweight validation.
    Does NOT load entire datasets into memory.
    """
    results = {
        'coordinates': {'name': 'Coordinates', 'status': 'Pending', 'shape': None, 'details': []},
        'forces': {'name': 'Forces', 'status': 'Pending', 'shape': None, 'details': []},
        'velocities': {'name': 'Velocities', 'status': 'Pending', 'shape': None, 'details': []},
        'consistency': {'name': 'Consistency Check', 'status': 'Pending', 'details': []}
    }
    
    expected_atom_cols = 414 # 138 atoms * 3
    
    # 1. Coordinates
    res_coord, rows_c, cols_c = validate_file_structure(
        os.path.join(data_dir, 'coordinates.csv'), 
        sep=';', 
        expected_cols=expected_atom_cols, 
        file_type='coordinates.csv'
    )
    results['coordinates'] = dict(results['coordinates'], **res_coord)

    # 2. Forces
    # Forces often have weird separators, try \t first implies logic in validate_file_structure handled by engine='python' fallback
    # But let's pass '\t' as hint
    res_force, rows_f, cols_f = validate_file_structure(
        os.path.join(data_dir, 'forces.csv'), 
        sep='\t', 
        expected_cols=expected_atom_cols, 
        file_type='forces.csv'
    )
    results['forces'] = dict(results['forces'], **res_force)

    # 3. Velocities
    res_vel, rows_v, cols_v = validate_file_structure(
        os.path.join(data_dir, 'velocity.csv'), 
        sep='\t', 
        expected_cols=expected_atom_cols, 
        file_type='velocity.csv'
    )
    results['velocities'] = dict(results['velocities'], **res_vel)

    # 4. Consistency
    consistent = True
    messages = []
    
    # Check if all files were found
    if rows_c == 0 or rows_f == 0 or rows_v == 0:
        consistent = False
        messages.append("One or more files are missing or empty.")
    else:
        # Check Row Consistency
        if not (rows_c == rows_f == rows_v):
            consistent = False
            messages.append(f"Row mismatch: Coords({rows_c}), Forces({rows_f}), Vels({rows_v})")
        
        # Check Column Consistency (already flagged in individual statuses, but good to summarize)
        if cols_c != expected_atom_cols:
            consistent = False
            messages.append("Coordinates columns invalid.")
        if cols_f < expected_atom_cols:
             consistent = False
             messages.append("Forces columns insufficient.")
        if cols_v < expected_atom_cols:
             consistent = False
             messages.append("Velocities columns insufficient.")

    if consistent:
        results['consistency']['status'] = 'Success'
        results['consistency']['details'].append("All data files appear consistent (Rows & Cols match).")
    else:
        results['consistency']['status'] = 'Warning'
        results['consistency']['details'] = messages

    return results
