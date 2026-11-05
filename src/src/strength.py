import string #importing the string module to access predefined character sets for password generation.
import math

def check_common_password(password: str) -> bool: #defining a function to check if the provided password is a common password by comparing it against a predefined list of common passwords.
    common_passwords = { #creating a set of common passwords for quick lookup.
        "password", "123456", "123456789", "qwerty", "abc123", "password1", "111111", "12345678",
        "iloveyou", "admin", "welcome", "monkey", "letmein", "football", "starwars", "dragon",
        "passw0rd", "master", "hello", "freedom", "whatever", "qazwsx", "trustno1", "123123", "654321", "superman", "1qaz2wsx", "qwertyuiop", "zaq1zaq1", "password123","1q2w3e4r", "qwerty123", "1qazxsw2", "qwerty1", "1234", "12345", "1234567", "123456789"
    }
    return password.lower() in common_passwords #returning True if the password (in lowercase) is found in the set of common passwords, otherwise returning False.

def password_strength(password: str) -> str: #defining a function to evaluate the strength of the provided password based on its length and character composition.
    length = len(password) #calculating the length of the password.
    has_upper = any(c.isupper() for c in password) #checking if the password contains at least one uppercase letter.
    has_lower = any(c.islower() for c in password) #checking if the password contains at least one lowercase letter.
    has_digit = any(c.isdigit() for c in password) #checking if the password contains at least one digit.
    has_special = any(c in string.punctuation for c in password) #checking if the password contains at least one special character (punctuation).

    score = sum([has_upper, has_lower, has_digit, has_special]) #calculating a score based on the presence of different character types.

    if length >= 12 and score >= 3:
        return "Strong"
    if length >= 8 and score >= 2:
        return "Moderate"
    return "Weak"


def estimate_crack_time(password: str, guesses_per_second: float = 10_000_000_000) -> str:
    if not password:
        return "—"
    if not math.isfinite(guesses_per_second) or guesses_per_second <= 0:
        raise ValueError("guesses_per_second must be greater than zero.")
    if any(ord(character) > 127 for character in password):
        return "Unavailable for non-ASCII characters"

    alphabet_size = sum(
        (
            26 if any(character.isupper() for character in password) else 0,
            26 if any(character.islower() for character in password) else 0,
            10 if any(character.isdigit() for character in password) else 0,
            len(string.punctuation)
            if any(character in string.punctuation for character in password)
            else 0,
        )
    )
    if not alphabet_size:
        return "Unavailable"

    log10_seconds = (
        len(password) * math.log10(alphabet_size)
        - math.log10(guesses_per_second)
        - math.log10(2)
    )
    if log10_seconds < 0:
        return "Less than 1 second"

    units = (
        ("year", 365.25 * 24 * 60 * 60),
        ("day", 24 * 60 * 60),
        ("hour", 60 * 60),
        ("minute", 60),
        ("second", 1),
    )
    for unit, seconds_per_unit in units:
        unit_log = math.log10(seconds_per_unit)
        if log10_seconds >= unit_log:
            amount = 10 ** (log10_seconds - unit_log)
            if unit == "year" and amount >= 1_000_000_000_000:
                return f"About 10^{math.log10(amount):.0f} years"
            rounded = max(1, round(amount))
            suffix = "" if rounded == 1 else "s"
            return f"About {rounded:,} {unit}{suffix}"
    return "Less than 1 second"


def feedback_on_password(password: str) -> str: #defining a function to provide feedback on the provided password, including its strength and whether it is a common password.
    strength = password_strength(password) #evaluating the strength of the password using the password_strength function.
    is_common = check_common_password(password) #checking if the password is a common password using the check_common_password function.

    feedback = f"Password Strength: {strength}" #creating a feedback message that includes the evaluated strength of the password.
    if is_common: #adding a warning to the feedback message if the password is found to be common.
        feedback += " (Warning: This is a common password!)"
    return feedback #returning the complete feedback message.

def main() -> None: #defining the main function that serves as the entry point for the password strength checker program. It prompts the user for input and displays feedback on the provided password.
    password = input("Enter a password to check its strength: ") #prompting the user to enter a password for evaluation.
    feedback = feedback_on_password(password) #obtaining feedback on the entered password using the feedback_on_password function.
    print(feedback) #displaying the feedback message to the user.
