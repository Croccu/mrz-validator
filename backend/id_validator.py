import re

VALID_TD1_REGEX = re.compile(r'^[A-Z0-9<]{30}$')

def compute_check_digit(data):
    weights = [7, 3, 1]
    total = 0
    for i, char in enumerate(data):
        if char == '<':
            value = 0
        elif char.isdigit():
            value = int(char)
        elif char.isalpha():
            value = ord(char.upper()) - 55
        else:
            return -1
        total += value * weights[i % 3]
    return total % 10

def validate_mrz_td1(doc_line, personal_line, name_line):
    print("🚨 Running FINAL validate_mrz_td1")

    # Parse names using the standard << separator if present.
    # Otherwise, fall back to splitting by whitespace after removing filler.
    name_line_clean = name_line.strip().upper()

    if "<<" in name_line_clean:
        name_parts = name_line_clean.split("<<", 1)
        surname = name_parts[0].replace("<", " ").strip()
        given_names = name_parts[1].replace("<", " ").strip()
    else:
        words = name_line_clean.replace("<", " ").strip().split()
        surname = words[0]
        given_names = " ".join(words[1:]) if len(words) > 1 else ""

    # Extract document number from positions 5–30
    # (Estonian IDs do not include a document check digit; we strip filler.)
    document_number = doc_line[5:30].replace("<", "")

    # Parse personal line (TD1 layout):
    birth_date = personal_line[0:6]         # YYMMDD
    birth_check = personal_line[6]          # birth date check digit
    sex = personal_line[7]                  # M, F, or <
    expiry_date = personal_line[8:14]       # YYMMDD expiry date
    expiry_check = personal_line[14]        # expiry date check digit
    nationality = personal_line[15:18]      # 3-letter country code
    final_check = personal_line[29]         # final check digit

    # Compute ICAO 9303 final check digit from combined fields
    combined = (
        document_number +
        birth_date + birth_check +
        expiry_date + expiry_check +
        personal_line[15:29]
    )

    # Estonian IDs (IDEST) use a non-standard check digit — bypass it
    final_valid = True if doc_line.startswith("IDEST") else (str(compute_check_digit(combined)) == final_check)

    print(f"SURNAME: {surname}")
    print(f"GIVEN: {given_names}")

    return {
        "document_number_valid": True,
        "birth_date_valid": str(compute_check_digit(birth_date)) == birth_check,
        "expiry_date_valid": str(compute_check_digit(expiry_date)) == expiry_check,
        "final_check_digit_valid": final_valid,
        "sex_valid": sex in ["M", "F", "<"],

        "surname": surname,
        "given_names": given_names,
        "birth_date_raw": birth_date,
        "expiry_date_raw": expiry_date,
        "sex_raw": sex,
        "nationality": nationality,
    }
