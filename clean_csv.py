import re
import pandas as pd



def is_blank(x):
    return x is None or (isinstance(x, float) and pd.isna(x)) or str(x).strip() == ""



df = pd.read_csv("skill-assessment-202511.csv")
total_rows = len(df)


#Email Cleaning


raw_non_empty_emails = (
    df["email"]
    .notna() &
    (df["email"].astype(str).str.strip() != "")
).sum()

raw_missing_emails = total_rows - raw_non_empty_emails

# print(f"Total rows: {total_rows}")
# print(f"Emails present (raw): {raw_non_empty_emails}")
# print(f"Emails missing (raw): {raw_missing_emails}")

def clean_email(email_raw):
    if is_blank(email_raw):
        return ""

    email = str(email_raw).strip().lower()

    if "@" not in email:
        return ""

    left, right = email.split("@", 1)

    if left == "":
        return ""

    if "." not in right:
        return ""

    return email

df["email_clean"] = df["email"].apply(clean_email)

clean_non_empty_emails = (
    df["email_clean"].astype(str).str.strip() != ""
).sum()

clean_missing_emails = total_rows - clean_non_empty_emails

# print(f"Emails present (clean): {clean_non_empty_emails}")
# print(f"Emails missing (clean): {clean_missing_emails}")


#Phone Cleaning


# print(df["phone"].head(10))
# print(df["phone"].tail(10))

def clean_phone(phone_raw):
    if is_blank(phone_raw):
        return ""

    phone = str(phone_raw)

    phone = re.sub(r"(ext\.?|x)\s*\d+.*$", "", phone, flags=re.IGNORECASE)

    digits = re.sub(r"\D", "", phone)

    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]

    if len(digits) != 10:
        return ""

    area = digits[:3]
    first = digits[3:6]
    last = digits[6:]

    return f"({area}) {first} - {last}"

df["phone_clean"] = df["phone"].apply(clean_phone)


# print(df[["phone", "phone_clean"]].head(10))
# print(df[["phone", "phone_clean"]].tail(10))


#Name Cleaning


def sentence_case(text):
    if is_blank(text):
        return ""
    text = str(text).strip()
    if text == "":
        return ""
    return text[:1].upper() + text[1:].lower()

def clean_name_string(name_raw):
    if is_blank(name_raw):
        return ""

    name = str(name_raw).strip()

    while len(name) >= 2 and name[0] == name[-1] and name[0] in ["'", '"']:
        name = name[1:-1].strip()

    name = re.sub(r"\s+", " ", name).strip()

    name = sentence_case(name)

    return name

def split_name(name_raw):
    name = clean_name_string(name_raw)

    if name == "":
        return ("", "", "")

    if "," in name:
        last_part, rest_part = [p.strip() for p in name.split(",", 1)]
        name = f"{rest_part} {last_part}".strip()
        name = re.sub(r"\s+", " ", name).strip()
        name = sentence_case(name)

    tokens = name.split(" ")

    if len(tokens) == 1:
        return ("", "", tokens[0])

    first_name = tokens[0]
    last_name = tokens[-1]

    if len(tokens) > 2:
        middle_name = " ".join(tokens[1:-1])
    else:
        middle_name = ""

    return (first_name, middle_name, last_name)

df[["first_name", "middle_name", "last_name"]] = df["name"].apply(
    lambda x: pd.Series(split_name(x))
)

# print(df[["name", "first_name", "middle_name", "last_name"]].head(10))
# print(df[["name", "first_name", "middle_name", "last_name"]].tail(10))


# Address Cleaning


# print(df["address"].head(10))
# print(df["address"].tail(10))

STATE_MAP = {
    "alabama": "AL", "alaska": "AK", "arizona": "AZ", "arkansas": "AR",
    "california": "CA", "colorado": "CO", "connecticut": "CT", "delaware": "DE",
    "florida": "FL", "georgia": "GA", "hawaii": "HI", "idaho": "ID",
    "illinois": "IL", "indiana": "IN", "iowa": "IA", "kansas": "KS",
    "kentucky": "KY", "louisiana": "LA", "maine": "ME", "maryland": "MD",
    "massachusetts": "MA", "michigan": "MI", "minnesota": "MN", "mississippi": "MS",
    "missouri": "MO", "montana": "MT", "nebraska": "NE", "nevada": "NV",
    "new hampshire": "NH", "new jersey": "NJ", "new mexico": "NM", "new york": "NY",
    "north carolina": "NC", "north dakota": "ND", "ohio": "OH", "oklahoma": "OK",
    "oregon": "OR", "pennsylvania": "PA", "rhode island": "RI", "south carolina": "SC",
    "south dakota": "SD", "tennessee": "TN", "texas": "TX", "utah": "UT",
    "vermont": "VT", "virginia": "VA", "washington": "WA", "west virginia": "WV",
    "wisconsin": "WI", "wyoming": "WY",
    "district of columbia": "DC"
}

STATE_ABBRS = set(STATE_MAP.values())

def clean_state(state_raw):
    if is_blank(state_raw):
        return ""

    state = str(state_raw).strip()

    if state == "":
        return ""

    upper = state.upper()
    if upper in STATE_ABBRS:
        return upper

    lowered = state.lower()
    if lowered in STATE_MAP:
        return STATE_MAP[lowered]

    return ""

# print(clean_state("il"))
# print(clean_state("Illinois"))
# print(clean_state("Ontario"))

def clean_zip(zip_raw):
    if is_blank(zip_raw):
        return ""

    z = str(zip_raw).strip()
    if z == "":
        return ""

    digits = re.sub(r"\D", "", z)

    if digits == "":
        return ""

    digits = digits[:5]

    return digits.zfill(5)

def sentence_case(text):
    if is_blank(text):
        return ""
    text = str(text).strip()
    if text == "":
        return ""
    return text[:1].upper() + text[1:].lower()

def strip_wrapping_quotes(text):
    if is_blank(text):
        return ""

    s = str(text).strip()

    if len(s) >= 2 and s[0] == s[-1] and s[0] in ["'", '"']:
        return s[1:-1].strip()

    return s

def clean_address(address_raw):
    if is_blank(address_raw):
        return ("", "", "", "")

    address = strip_wrapping_quotes(address_raw)

    address = re.sub(r"\s+", " ", address).strip()
    if address == "":
        return ("", "", "", "")

    parts = [p.strip() for p in address.split(",") if p.strip()]

    street_address = ""
    city = ""
    state = ""
    zip_code = ""

    if len(parts) >= 1:
        street_address = sentence_case(parts[0])

    if len(parts) >= 2:
        city = sentence_case(parts[1])

    tail = " ".join(parts[2:]) if len(parts) >= 3 else ""
    tail = tail.strip()

    tail = re.sub(r"\b(united states|usa)\b", "", tail, flags=re.IGNORECASE).strip()
    tail = re.sub(r"\s+", " ", tail).strip()

    zip_match = re.search(r"\b(\d{5})(?:-\d{4})?\b", tail)
    if zip_match:
        zip_code = clean_zip(zip_match.group(0))
        tail = (tail[:zip_match.start()] + tail[zip_match.end():]).strip()
        tail = re.sub(r"\s+", " ", tail).strip()

    if tail != "":
        tokens = tail.split()

        if len(tokens) >= 2:
            state_candidate_2 = " ".join(tokens[-2:])
            state_cleaned = clean_state(state_candidate_2)
            if state_cleaned != "":
                state = state_cleaned
            else:
                state_candidate_1 = tokens[-1]
                state = clean_state(state_candidate_1)
        else:
            state = clean_state(tokens[0])

    return (street_address, city, state, zip_code)

df[["street_address", "city", "state", "zip"]] = df["address"].apply(
    lambda x: pd.Series(clean_address(x))
)

# print(df[["address", "street_address", "city", "state", "zip"]].head(5))
# print(df[["address", "street_address", "city", "state", "zip"]].tail(5))


#Coverage Stats (Optional)


states_present = (df["state"].astype(str).str.strip() != "").sum()
zips_present = (df["zip"].astype(str).str.strip() != "").sum()
street_present = (df["street_address"].astype(str).str.strip() != "").sum()
city_present = (df["city"].astype(str).str.strip() != "").sum()

# print(f"States present (clean): {states_present} / {total_rows}")
# print(f"ZIPs present (clean): {zips_present} / {total_rows}")
# print(f"Street present (clean): {street_present} / {total_rows}")
# print(f"City present (clean): {city_present} / {total_rows}")


#Final Output


df["email_final"] = df["email_clean"]
df["phone_final"] = df["phone_clean"]

final_df = df[[
    "first_name",
    "middle_name",
    "last_name",
    "email_final",
    "phone_final",
    "street_address",
    "city",
    "state",
    "zip"
]].copy()

final_df = final_df.rename(columns={
    "email_final": "email",
    "phone_final": "phone"
})

final_df = final_df.fillna("")

output_file = "cleaned_output.csv"
final_df.to_csv(output_file, index=False)

# print(f"Saved cleaned CSV to: {output_file}")
# print(final_df.head(5))
# print(final_df.tail(5))
