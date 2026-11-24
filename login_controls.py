
import time
import logging

# Configure security audit log
logging.basicConfig(
    filename="security_audit.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Security settings
MAX_ATTEMPTS = 5
LOCKOUT_TIME = 15 * 60  # 15 minutes

# Demo user credentials
USERNAME = "admin"
PASSWORD = "admin123"


class LoginAttemptControl:

    def __init__(self):
        self.failed_attempts = {}
        self.locked_accounts = {}

    # Check whether account is locked
    def is_locked(self, username):

        if username in self.locked_accounts:

            expiry = self.locked_accounts[username]

            if time.time() < expiry:
                return True

            # Unlock after 15 minutes
            del self.locked_accounts[username]
            self.failed_attempts[username] = 0

            logging.info(
                "ACCOUNT_UNLOCKED: %s", username
            )

        return False

    # Login verification
    def login(self, username, password):

        # Check account lock
        if self.is_locked(username):

            logging.warning(
                "LOGIN_BLOCKED: %s", username
            )

            return False, "Account is locked. Try later."

        # Verify username and password
        if username == USERNAME and password == PASSWORD:

            self.failed_attempts[username] = 0

            logging.info(
                "LOGIN_SUCCESS: %s", username
            )

            return True, "Login successful!"

        # Increase failed attempts
        self.failed_attempts[username] = (
            self.failed_attempts.get(username, 0) + 1
        )

        attempts = self.failed_attempts[username]

        logging.warning(
            "LOGIN_FAILED: %s Attempt: %d",
            username, attempts
        )

        print(
            f"Incorrect login attempts: {attempts}/{MAX_ATTEMPTS}"
        )

        # Lock account after 5 failures
        if attempts >= MAX_ATTEMPTS:

            self.locked_accounts[username] = (
                time.time() + LOCKOUT_TIME
            )

            logging.critical(
                "ACCOUNT_LOCKED: %s for 15 minutes",
                username
            )

            return False, "Account locked for 15 minutes!"

        remaining = MAX_ATTEMPTS - attempts

        return False, (
            f"Invalid username or password. "
            f"{remaining} attempts remaining."
        )


# Main program
def main():

    security = LoginAttemptControl()

    print("====================================")
    print("     LOGIN ATTEMPT CONTROL SYSTEM")
    print("====================================")

    while True:

        print("\n---------- LOGIN ----------")

        username = input("Enter username: ")
        password = input("Enter password: ")

        success, message = security.login(
            username, password
        )

        print("\nLogin Status:", message)

        if success:
            print("Welcome to the system!")
            break

        if security.is_locked(username):
            print("Please wait for 15 minutes.")
            break


if __name__ == "__main__":
    main()
