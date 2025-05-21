import re

VALID_MRZ_REGEX = re.compile(r'^[A-Z0-9<]{44}$')

def char_to_value(char):
    if char.isdigit():
        return int(char)
    elif char.isalpha():
        return ord(char.upper()) - 55
    elif char == '<':
        return 0
    raise ValueError(f"Invalid character in MRZ: {char}")

def compute_check_digit(data):
    weights = [7, 3, 1]
    total = sum(char_to_value(c) * weights[i % 3] for i, c in enumerate(data))
    return str(total % 10)

def validate_mrz(mrz_line1, mrz_line2):
    if len(mrz_line1) != 44 or len(mrz_line2) != 44:
        return {"error": "Both MRZ lines must be exactly 44 characters"}

    if not VALID_MRZ_REGEX.match(mrz_line1) or not VALID_MRZ_REGEX.match(mrz_line2):
        return {"error": "MRZ contains invalid characters. Only A-Z, 0–9, and '<' are allowed."}

    names_raw = mrz_line1[5:].split("<<", 1)
    surname = names_raw[0].replace("<", " ").strip()
    given_names = names_raw[1].replace("<", " ").strip() if len(names_raw) > 1 else ""

    passport_number = mrz_line2[0:9]
    passport_check = mrz_line2[9]
    nationality = mrz_line2[10:13]
    birth_date = mrz_line2[13:19]
    birth_check = mrz_line2[19]
    sex = mrz_line2[20]
    expiry_date = mrz_line2[21:27]
    expiry_check = mrz_line2[27]
    personal_number = mrz_line2[28:42]
    final_check = mrz_line2[43]

    all_for_final = (
        passport_number + passport_check +
        birth_date + birth_check +
        expiry_date + expiry_check +
        personal_number
    )

    return {
        "passport_number_valid": compute_check_digit(passport_number) == passport_check,
        "birth_date_valid": compute_check_digit(birth_date) == birth_check,
        "expiry_date_valid": compute_check_digit(expiry_date) == expiry_check,
        "final_check_digit_valid": compute_check_digit(all_for_final) == final_check,
        # Parsed personal data:
        "surname": surname,
        "given_names": given_names,
        "nationality": nationality,
        "birth_date_raw": birth_date,
        "expiry_date_raw": expiry_date,
        "sex_raw": sex,
    }
