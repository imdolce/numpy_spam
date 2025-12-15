# I know i'm a slob for using py, but at least the input filtering is nice

import numpy as np
import sys
import glob

def mat_extract(file_path): 
    # Extracts all matrices from one CSV file within the main folder
    # This is a subprocess of load_matrix(), handling each file.
    mat = {}
    current_matrix_name = None
    
    # Why use try? So that your program doesn't shit itself when input error.
    try:
        with open(file_path, "r", encoding='utf-8-sig') as data:
            for line in data:
                line = line.strip()
                if not line:
                    continue
                if line.startswith('matran'):
                    # Found a new matrix 
                    current_matrix_name = line
                    mat[current_matrix_name] = []
                elif current_matrix_name:
                    # Found data, append to the current matrix
                    try:
                        row = [int(x) for x in line.split(',')]
                        mat[current_matrix_name].append(row)
                    except ValueError:
                        # Ignore non integer value error
                        continue

        # Convert lists to numpy arrays
        for name, data_list in mat.items():
            if data_list:
                mat[name] = np.array(data_list)
            else:
                # remove empty matrices
                del mat[name]

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}", file=sys.stderr)
    except Exception as e:
        print(f"An error occurred processing {file_path}: {e}", file=sys.stderr)
        
    return mat

def load_matrices():
    # Extract output from mat_extract()
    # Index to user.
    all_matrices = {}
    csv_files = glob.glob('*.csv')
    if not csv_files:
        print("No CSV files found in the current directory.")
        return None

    print(f"Found CSV files: {', '.join(csv_files)}")

    for file in csv_files:
        matrices_from_file = mat_extract(file)
        for mat_name, mat_data in matrices_from_file.items():
            unique_name = f"{file}:{mat_name}"
            all_matrices[unique_name] = mat_data
            
    return all_matrices

def handle_input_logic(mat_a, mat_b, op):
    # Calculate 2 matrices with ops
    try:
        if op == 'add':
            if mat_a.shape != mat_b.shape:
                raise ValueError(f"Shape Mismatch: Cannot add {mat_a.shape} and {mat_b.shape}")
            return mat_a + mat_b

        elif op == 'subtract':
            if mat_a.shape != mat_b.shape:
                raise ValueError(f"Shape Mismatch: Cannot subtract {mat_a.shape} and {mat_b.shape}")
            return mat_a - mat_b

        elif op == 'multiply':
            if mat_a.shape[1] != mat_b.shape[0]:
                raise ValueError(f"Dimension Mismatch: Cannot multiply {mat_a.shape} by {mat_b.shape}")
            return mat_a @ mat_b

    except ValueError as e:
        print(f"❌ op ERROR: {e}", file=sys.stderr)
        return None

def calc_mat():
    # Gemini improved this function
    master_matrix_list = load_matrices()

    if not master_matrix_list:
        return

    # Convert dict to a list of tuples (name, matrix) for indexed access
    indexed_matrices = list(master_matrix_list.items())

    while True:
        print("\nAvailable Matrices:")
        for i, (name, matrix) in enumerate(indexed_matrices):
            print(f"  {i+1}: {name} (shape: {matrix.shape})")

        try:
            # --- Choose First Matrix ---
            choice1 = int(input("Choose the first matrix (by number): ")) - 1
            if not 0 <= choice1 < len(indexed_matrices):
                print("Invalid number. Please try again.")
                continue
            
            # --- Choose Second Matrix ---
            choice2 = int(input("Choose the second matrix (by number): ")) - 1
            if not 0 <= choice2 < len(indexed_matrices):
                print("Invalid number. Please try again.")
                continue

            # --- Choose op ---
            op = input("Choose op (add, subtract, multiply): ").lower()
            if op not in ['add', 'subtract', 'multiply']:
                print("Invalid op. Please choose 'add', 'subtract', or 'multiply'.")
                continue

            mat_a_name, mat_a = indexed_matrices[choice1]
            mat_b_name, mat_b = indexed_matrices[choice2]

            print(f"\nPerforming '{op}' on '{mat_a_name}' and '{mat_b_name}'...")
            
            result = handle_input_logic(mat_a, mat_b, op)

            if result is not None:
                print("\n--- Result ---")
                print(result)
                print("--------------")

        except ValueError:
            print("\nInvalid input. Please enter a number.")
            continue
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}", file=sys.stderr)
            continue

        # --- Continue or Quit ---
        another = input("\nPerform another calculation? (y/n): ").lower()
        if another in ['n', 'q', 'no', 'quit']:
            print("Exiting calculator.")
            break

if __name__ == "__main__":
    calc_mat()