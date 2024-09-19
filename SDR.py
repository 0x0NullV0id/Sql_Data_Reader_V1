import re
import os
import argparse

# Define the email domains to search for
email_domains = ['gmail.com', 'hotmail.com', 'yahoo.com', 'example.com']  # Add more domains as needed

# Refined email pattern for SQL-like entries
email_pattern = re.compile(r"['\"]([a-zA-Z0-9._%+-]+@(" + '|'.join(email_domains) + r"))['\"]")

def extract_emails_from_sql(file_path, verbose=False):
    """Extract emails from the given SQL file."""
    emails = set()
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            for line_number, line in enumerate(file, start=1):
                found_emails = email_pattern.findall(line)
                if found_emails and verbose:
                    print(f"Line {line_number}: Found emails {found_emails}")
                # Update emails set with first item in each match tuple
                emails.update([email[0] for email in found_emails])
    except Exception as e:
        if verbose:
            print(f"Error reading {file_path}: {e}")
    return emails

def write_emails_to_file(emails, output_file, verbose=False):
    """Write the extracted emails to the output file."""
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            for email in sorted(emails):
                file.write(f"{email}\n")
        if verbose:
            print(f"Total {len(emails)} emails written to {output_file}")
    except Exception as e:
        if verbose:
            print(f"Error writing to {output_file}: {e}")

def main(verbose=False):
    """Main function to extract emails from all SQL files in the current directory."""
    all_emails = set()
    
    # Get the directory where the script is located
    input_directory = os.path.dirname(os.path.realpath(__file__))
    
    # Read all .sql files in the current directory
    sql_files = [f for f in os.listdir(input_directory) if f.endswith('.sql')]
    
    if not sql_files:
        print("No .sql files found in the current directory.")
        return
    
    for filename in sql_files:
        file_path = os.path.join(input_directory, filename)
        if verbose:
            print(f"Processing {filename}...")
        emails = extract_emails_from_sql(file_path, verbose=verbose)
        all_emails.update(emails)
    
    # Define output file name
    output_file = os.path.join(input_directory, 'extracted_emails.txt')
    
    # Write all collected emails to the output file
    if all_emails:
        write_emails_to_file(all_emails, output_file, verbose=verbose)
        if verbose:
            print(f"Emails extracted and saved to {output_file}")
    else:
        print("No emails found in the .sql files.")

if __name__ == "__main__":
    # Add command line argument for verbose mode
    parser = argparse.ArgumentParser(description="Extract emails from SQL files.")
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()
    
    # Call the main function with the verbose flag
    main(verbose=args.verbose)
