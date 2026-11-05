import secrets
import string
# importing the secrets module for generating secure random numbers and the string module for accessing character sets.
#determine the types of characters that can be included in the password, mapping user choices to corresponding character sets.
CHARACTER_TYPES = {
    "1": ("letters", string.ascii_letters),
    "2": ("digits", string.digits),
    "3": ("punctuation", string.punctuation),
}

#creating a function to generate a password based on the specified length and selected character types. It validates the input choices, ensures that the password length is sufficient, and constructs the password using secure random selection from the chosen character sets.
def generate_password(length: int, choices: list[str]) -> str:
    selected_choices = set(choices)
    invalid_choices = selected_choices - CHARACTER_TYPES.keys()
#using set operations to identify any invalid choices provided by the user. If there are invalid choices, a ValueError is raised with a message indicating the invalid selections. The function also checks if at least one character type is selected and if the password length is sufficient to accommodate the selected character types.
    if invalid_choices:
        raise ValueError(f"Invalid choice(s): {', '.join(sorted(invalid_choices))}.")       #adding a check to ensure that the user has selected valid character types, raising a ValueError if any invalid choices are detected.
    if not selected_choices:
        raise ValueError("Select at least one character type.")     #adding a check to ensure that the user has selected at least one character type, raising a ValueError if no character types are selected.
    if length < len(selected_choices):
        raise ValueError(
            "Password length must be at least the number of selected character types."      #adding a check to ensure that the password length is at least equal to the number of selected character types, raising a ValueError if this condition is not met.
        )

    selected_character_sets = [
        CHARACTER_TYPES[choice][1] for choice in sorted(selected_choices)   #creating a list of selected character sets based on the user's choices, ensuring that the character sets are sorted for consistent password generation.
    ]
    all_characters = "".join(selected_character_sets)

    rng = secrets.SystemRandom()        #using the secrets module's SystemRandom class to create a secure random number generator for selecting characters from the chosen character sets.
    password = [rng.choice(characters) for characters in selected_character_sets]
    password.extend(
        rng.choice(all_characters) for _ in range(length - len(password))       #adding additional random characters from the combined character sets to meet the desired password length, ensuring that the password contains a mix of the selected character types.
    )
    rng.shuffle(password)           #shuffling the password list to ensure that the characters are randomly distributed, enhancing the security of the generated password.
    return "".join(password)        #returning the generated password as a string after shuffling the characters to ensure randomness and security.


def main() -> None:     #defining the main function that serves as the entry point for the password generator program. It prompts the user for input, handles exceptions, and displays the generated password.
    print("Choose character types to include in the password:")
    for choice, (name, _) in CHARACTER_TYPES.items():       #iterating over the CHARACTER_TYPES dictionary to display the available character type options to the user, allowing them to select which types of characters they want to include in the generated password.
        print(f"{choice}. {name.title()}")

    try:
        length = int(input("Enter the password length: "))      #prompting the user to enter the desired password length and converting the input to an integer. If the input is not a valid whole number, a ValueError is raised, which is caught and handled by displaying an error message and exiting the program.
    except ValueError as error:
        raise SystemExit("Password length must be a whole number.") from error

    raw_choices = input(        #prompting the user to enter their choices for character types, allowing them to input one or more selections separated by commas. The input is then processed to create a list of valid choices by stripping whitespace and filtering out any empty entries.
        "Enter one or more choices separated by commas (for example, 1, 2, 3): "
    )
    choices = [choice.strip() for choice in raw_choices.split(",") if choice.strip()]       #processing the user's input to create a list of valid character type choices.

    try:        #calling the generate_password function with the specified length and selected character types. If any validation errors occur during password generation, they are caught and handled by displaying an error message and exiting the program.
        password = generate_password(length, choices)
    except ValueError as error:
        raise SystemExit(str(error)) from error

    print("Generated password: " + password)


if __name__ == "__main__":      #checking if the script is being run directly (as opposed to being imported as a module). If it is, the main function is called to execute the password generation process.
    main()
