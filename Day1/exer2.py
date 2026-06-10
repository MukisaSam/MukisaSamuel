secret_number = input("Enter a secret number between 1 and 100: ")
attempts = 3
while attempts > 0:
    guess = input("Guess the secret number: ")
    if guess == secret_number:
        print(f"Congs, You've guessed the secret number: {secret_number}")
        break
    else:
        attempts -= 1
        print(f"Wrong guess. You have {attempts} attempts left.")
