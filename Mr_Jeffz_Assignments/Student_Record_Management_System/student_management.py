"""Menu-driven Student Record Management System.

Core student information is stored in ``students.csv`` while additional
details are stored in ``students.json``.  All files are kept beside this
script so the project can be moved to another computer as one folder.
"""

from __future__ import annotations

import csv
import io
import json
import logging
import re
from pathlib import Path
from typing import Callable


CSV_FIELDS = ["registration_number", "first_name", "last_name", "email"]
DETAIL_FIELDS = ["address", "contact", "program"]
REGISTRATION_PATTERN = re.compile(r"^[A-Za-z0-9/-]{3,20}$")
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
CONTACT_PATTERN = re.compile(r"^\+?[0-9]{7,15}$")


class StudentSystemError(Exception):
    """Base exception for expected student-system errors."""


class DuplicateStudentError(StudentSystemError):
    """Raised when a registration number already exists."""


class StudentNotFoundError(StudentSystemError):
    """Raised when a requested registration number cannot be found."""


class DataFileError(StudentSystemError):
    """Raised when a data file is missing, damaged, or cannot be processed."""


def configure_logger(log_path: Path) -> logging.Logger:
    """Create a file logger without adding duplicate handlers on re-import."""
    logger = logging.getLogger(f"student_system.{log_path.resolve()}")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        handler = logging.FileHandler(log_path, encoding="utf-8")
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s | %(levelname)-8s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )
        logger.addHandler(handler)
    return logger


def validate_registration_number(value: str) -> str:
    """Validate and normalize a registration number."""
    value = value.strip().upper()
    if not REGISTRATION_PATTERN.fullmatch(value):
        raise ValueError(
            "Registration number must be 3-20 characters and may contain "
            "letters, numbers, /, or -."
        )
    return value


def validate_name(value: str, field_name: str) -> str:
    """Validate a student's first or last name."""
    value = " ".join(value.strip().split())
    valid_characters = all(
        character.isalpha() or character in " -'" for character in value
    )
    if not value or len(value) > 50 or not valid_characters:
        raise ValueError(
            f"{field_name} must contain only letters, spaces, apostrophes, "
            "or hyphens (maximum 50 characters)."
        )
    return value.title()


def validate_email(value: str) -> str:
    """Perform a practical, user-friendly email format check."""
    value = value.strip().lower()
    if len(value) > 100 or not EMAIL_PATTERN.fullmatch(value):
        raise ValueError("Enter a valid email address, for example name@example.com.")
    return value


def validate_contact(value: str) -> str:
    """Validate a contact number after removing common visual separators."""
    value = value.strip().replace(" ", "").replace("-", "")
    if not CONTACT_PATTERN.fullmatch(value):
        raise ValueError(
            "Contact must contain 7-15 digits and may begin with a plus sign."
        )
    return value


def validate_text(value: str, field_name: str, maximum: int) -> str:
    """Validate a required free-text value."""
    value = " ".join(value.strip().split())
    if not value:
        raise ValueError(f"{field_name} cannot be empty.")
    if len(value) > maximum:
        raise ValueError(f"{field_name} cannot exceed {maximum} characters.")
    return value


class StudentRecordSystem:
    """Coordinate student data stored across CSV and JSON files."""

    def __init__(self, data_directory: Path | str | None = None) -> None:
        self.data_directory = Path(data_directory or Path(__file__).resolve().parent)
        self.data_directory.mkdir(parents=True, exist_ok=True)
        self.csv_path = self.data_directory / "students.csv"
        self.json_path = self.data_directory / "students.json"
        self.log_path = self.data_directory / "student_system.log"
        self.logger = configure_logger(self.log_path)
        self._initialize_files()

    def _initialize_files(self) -> None:
        """Create correctly structured data files when they do not exist."""
        try:
            if not self.csv_path.exists():
                with self.csv_path.open("w", newline="", encoding="utf-8") as file:
                    csv.DictWriter(file, fieldnames=CSV_FIELDS).writeheader()
                self.logger.info("Created CSV data file: %s", self.csv_path.name)

            if not self.json_path.exists():
                self.json_path.write_text("{}\n", encoding="utf-8")
                self.logger.info("Created JSON data file: %s", self.json_path.name)
        except OSError as error:
            self.logger.exception("Could not initialize the data files")
            raise DataFileError("The system could not create its data files.") from error
        finally:
            self.logger.info("Data-file initialization check completed")

    def _load_students(self) -> list[dict[str, str]]:
        """Read and validate all core records from the CSV file."""
        try:
            with self.csv_path.open("r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                if reader.fieldnames != CSV_FIELDS:
                    raise DataFileError(
                        "students.csv has an invalid or missing header row."
                    )
                return [dict(row) for row in reader]
        except (OSError, csv.Error) as error:
            self.logger.exception("Failed to read %s", self.csv_path.name)
            raise DataFileError("The CSV data file could not be read.") from error
        finally:
            self.logger.debug("CSV read attempt completed")

    def _load_details(self) -> dict[str, dict[str, str]]:
        """Read and validate additional details from the JSON file."""
        try:
            with self.json_path.open("r", encoding="utf-8") as file:
                details = json.load(file)
            if not isinstance(details, dict):
                raise DataFileError("students.json must contain a JSON object.")
            for registration_number, record in details.items():
                valid_record = (
                    isinstance(registration_number, str)
                    and isinstance(record, dict)
                    and set(record) == set(DETAIL_FIELDS)
                    and all(isinstance(record[field], str) for field in DETAIL_FIELDS)
                )
                if not valid_record:
                    raise DataFileError(
                        "students.json contains an incorrectly structured record."
                    )
            return details
        except json.JSONDecodeError as error:
            self.logger.exception("Invalid JSON in %s", self.json_path.name)
            raise DataFileError("The JSON data file contains invalid JSON.") from error
        except OSError as error:
            self.logger.exception("Failed to read %s", self.json_path.name)
            raise DataFileError("The JSON data file could not be read.") from error
        finally:
            self.logger.debug("JSON read attempt completed")

    @staticmethod
    def _write_text(path: Path, content: str) -> None:
        """Write complete text content using consistent UTF-8 encoding."""
        with path.open("w", encoding="utf-8", newline="") as file:
            file.write(content)

    def _commit(
        self,
        students: list[dict[str, str]],
        details: dict[str, dict[str, str]],
    ) -> None:
        """Write both stores and restore their old contents if either write fails."""
        original_csv = self.csv_path.read_text(encoding="utf-8")
        original_json = self.json_path.read_text(encoding="utf-8")

        csv_lines: list[str] = []
        try:
            # A temporary in-memory string keeps CSV quoting correct.
            csv_buffer = io.StringIO(newline="")
            writer = csv.DictWriter(csv_buffer, fieldnames=CSV_FIELDS)
            writer.writeheader()
            writer.writerows(students)
            csv_lines.append(csv_buffer.getvalue())

            json_text = json.dumps(details, indent=4, ensure_ascii=False) + "\n"
            self._write_text(self.csv_path, csv_lines[0])
            self._write_text(self.json_path, json_text)
        except (OSError, csv.Error, TypeError, ValueError) as error:
            self.logger.exception("Failed to save student data; restoring old files")
            try:
                self._write_text(self.csv_path, original_csv)
                self._write_text(self.json_path, original_json)
            except OSError:
                self.logger.critical("Rollback failed; inspect both data files")
            raise DataFileError("Changes could not be saved safely.") from error
        finally:
            self.logger.debug("Data save attempt completed")

    @staticmethod
    def _validated_record(
        registration_number: str,
        first_name: str,
        last_name: str,
        email: str,
        address: str,
        contact: str,
        program: str,
    ) -> tuple[dict[str, str], dict[str, str]]:
        """Validate fields and split them into CSV and JSON records."""
        registration_number = validate_registration_number(registration_number)
        student = {
            "registration_number": registration_number,
            "first_name": validate_name(first_name, "First name"),
            "last_name": validate_name(last_name, "Last name"),
            "email": validate_email(email),
        }
        details = {
            "address": validate_text(address, "Address", 150),
            "contact": validate_contact(contact),
            "program": validate_text(program, "Program", 100),
        }
        return student, details

    def add_student(
        self,
        registration_number: str,
        first_name: str,
        last_name: str,
        email: str,
        address: str,
        contact: str,
        program: str,
    ) -> None:
        """Add a validated student to both data stores."""
        student, extra_details = self._validated_record(
            registration_number,
            first_name,
            last_name,
            email,
            address,
            contact,
            program,
        )
        students = self._load_students()
        registration_number = student["registration_number"]

        if any(
            row["registration_number"].upper() == registration_number
            for row in students
        ):
            self.logger.warning("ADD rejected: duplicate %s", registration_number)
            raise DuplicateStudentError(
                f"Student {registration_number} already exists."
            )

        details = self._load_details()
        students.append(student)
        details[registration_number] = extra_details
        self._commit(students, details)
        self.logger.info("ADD student %s", registration_number)

    def view_students(self) -> list[dict[str, str]]:
        """Return combined records from both data stores."""
        students = self._load_students()
        details = self._load_details()
        combined = [
            {**student, **details.get(student["registration_number"], {})}
            for student in students
        ]
        self.logger.info("VIEW all students (%d record(s))", len(combined))
        return combined

    def search_student(self, registration_number: str) -> dict[str, str]:
        """Find one student by registration number."""
        registration_number = validate_registration_number(registration_number)
        students = self._load_students()
        details = self._load_details()

        for student in students:
            if student["registration_number"].upper() == registration_number:
                self.logger.info("SEARCH found student %s", registration_number)
                return {**student, **details.get(registration_number, {})}

        self.logger.warning("SEARCH could not find student %s", registration_number)
        raise StudentNotFoundError(f"Student {registration_number} was not found.")

    def update_student(
        self, registration_number: str, updates: dict[str, str]
    ) -> None:
        """Update supplied fields while leaving blank/omitted fields unchanged."""
        registration_number = validate_registration_number(registration_number)
        students = self._load_students()
        details = self._load_details()

        index = next(
            (
                position
                for position, student in enumerate(students)
                if student["registration_number"].upper() == registration_number
            ),
            None,
        )
        if index is None:
            self.logger.warning("UPDATE could not find student %s", registration_number)
            raise StudentNotFoundError(f"Student {registration_number} was not found.")

        current = {
            **students[index],
            **details.get(registration_number, {field: "" for field in DETAIL_FIELDS}),
        }
        current.update(
            {
                key: value
                for key, value in updates.items()
                if key in CSV_FIELDS + DETAIL_FIELDS and key != "registration_number"
            }
        )
        student, extra_details = self._validated_record(
            registration_number,
            current["first_name"],
            current["last_name"],
            current["email"],
            current["address"],
            current["contact"],
            current["program"],
        )
        students[index] = student
        details[registration_number] = extra_details
        self._commit(students, details)
        self.logger.info(
            "UPDATE student %s fields=%s",
            registration_number,
            ",".join(sorted(updates)) or "none",
        )

    def delete_student(self, registration_number: str) -> None:
        """Delete a student from both files."""
        registration_number = validate_registration_number(registration_number)
        students = self._load_students()
        details = self._load_details()
        remaining = [
            student
            for student in students
            if student["registration_number"].upper() != registration_number
        ]

        if len(remaining) == len(students):
            self.logger.warning("DELETE could not find student %s", registration_number)
            raise StudentNotFoundError(f"Student {registration_number} was not found.")

        details.pop(registration_number, None)
        self._commit(remaining, details)
        self.logger.info("DELETE student %s", registration_number)


def prompt_value(
    prompt: str,
    validator: Callable[[str], str],
    *,
    allow_blank: bool = False,
) -> str:
    """Prompt repeatedly until a value passes its validator."""
    while True:
        value = input(prompt).strip()
        if allow_blank and not value:
            return ""
        try:
            return validator(value)
        except ValueError as error:
            print(f"Invalid input: {error}")


def display_student(student: dict[str, str]) -> None:
    """Display one combined student record."""
    print("\n" + "-" * 58)
    print(f"Registration number : {student.get('registration_number', 'N/A')}")
    print(
        "Name                : "
        f"{student.get('first_name', 'N/A')} {student.get('last_name', '')}"
    )
    print(f"Email               : {student.get('email', 'N/A')}")
    print(f"Address             : {student.get('address', 'N/A')}")
    print(f"Contact             : {student.get('contact', 'N/A')}")
    print(f"Program             : {student.get('program', 'N/A')}")


def add_student_menu(system: StudentRecordSystem) -> None:
    """Collect the fields required to create a student."""
    print("\nADD A NEW STUDENT")
    registration_number = prompt_value(
        "Registration number: ", validate_registration_number
    )
    first_name = prompt_value(
        "First name: ", lambda value: validate_name(value, "First name")
    )
    last_name = prompt_value(
        "Last name: ", lambda value: validate_name(value, "Last name")
    )
    email = prompt_value("Email: ", validate_email)
    address = prompt_value(
        "Address: ", lambda value: validate_text(value, "Address", 150)
    )
    contact = prompt_value("Contact number: ", validate_contact)
    program = prompt_value(
        "Program: ", lambda value: validate_text(value, "Program", 100)
    )
    system.add_student(
        registration_number,
        first_name,
        last_name,
        email,
        address,
        contact,
        program,
    )
    print("Student added successfully.")


def view_students_menu(system: StudentRecordSystem) -> None:
    """Display every student, or a friendly empty-state message."""
    students = system.view_students()
    if not students:
        print("\nNo student records are available.")
        return
    print(f"\nALL STUDENTS ({len(students)} record(s))")
    for student in students:
        display_student(student)


def search_student_menu(system: StudentRecordSystem) -> None:
    """Prompt for and display a single student."""
    registration_number = prompt_value(
        "Enter registration number: ", validate_registration_number
    )
    display_student(system.search_student(registration_number))


def update_student_menu(system: StudentRecordSystem) -> None:
    """Collect optional replacement values for an existing student."""
    registration_number = prompt_value(
        "Registration number to update: ", validate_registration_number
    )
    current = system.search_student(registration_number)
    display_student(current)
    print("\nPress Enter to keep an existing value.")

    prompts: list[tuple[str, str, Callable[[str], str]]] = [
        (
            "first_name",
            f"First name [{current.get('first_name', '')}]: ",
            lambda value: validate_name(value, "First name"),
        ),
        (
            "last_name",
            f"Last name [{current.get('last_name', '')}]: ",
            lambda value: validate_name(value, "Last name"),
        ),
        ("email", f"Email [{current.get('email', '')}]: ", validate_email),
        (
            "address",
            f"Address [{current.get('address', '')}]: ",
            lambda value: validate_text(value, "Address", 150),
        ),
        ("contact", f"Contact [{current.get('contact', '')}]: ", validate_contact),
        (
            "program",
            f"Program [{current.get('program', '')}]: ",
            lambda value: validate_text(value, "Program", 100),
        ),
    ]
    updates: dict[str, str] = {}
    for field, prompt, validator in prompts:
        value = prompt_value(prompt, validator, allow_blank=True)
        if value:
            updates[field] = value

    if not updates:
        print("No changes were entered.")
        system.logger.info("UPDATE cancelled: no changes for %s", registration_number)
        return
    system.update_student(registration_number, updates)
    print("Student updated successfully.")


def delete_student_menu(system: StudentRecordSystem) -> None:
    """Confirm and delete a student record."""
    registration_number = prompt_value(
        "Registration number to delete: ", validate_registration_number
    )
    display_student(system.search_student(registration_number))
    confirmation = input("\nType YES to permanently delete this record: ").strip()
    if confirmation.upper() != "YES":
        print("Deletion cancelled.")
        system.logger.info("DELETE cancelled for %s", registration_number)
        return
    system.delete_student(registration_number)
    print("Student deleted successfully.")


def print_menu() -> None:
    """Display the application's main menu."""
    print(
        "\n"
        "========================================\n"
        "   STUDENT RECORD MANAGEMENT SYSTEM\n"
        "========================================\n"
        "1. Add a new student\n"
        "2. View all students\n"
        "3. Search by registration number\n"
        "4. Update student details\n"
        "5. Delete a student record\n"
        "6. Exit\n"
    )


def main() -> None:
    """Run the menu loop and handle user-facing errors."""
    system: StudentRecordSystem | None = None
    try:
        system = StudentRecordSystem()
        system.logger.info("SYSTEM START")
        actions = {
            "1": add_student_menu,
            "2": view_students_menu,
            "3": search_student_menu,
            "4": update_student_menu,
            "5": delete_student_menu,
        }

        while True:
            print_menu()
            choice = input("Choose an option (1-6): ").strip()
            if choice == "6":
                print("Thank you for using the Student Record Management System.")
                break

            action = actions.get(choice)
            if action is None:
                print("Invalid choice. Please enter a number from 1 to 6.")
                system.logger.warning("Invalid menu choice: %r", choice)
                continue

            try:
                action(system)
            except (StudentSystemError, ValueError) as error:
                print(f"Unable to complete the action: {error}")
            except OSError as error:
                system.logger.exception("Unexpected file-system error")
                print(f"A file-system error occurred: {error}")
            except Exception:
                system.logger.exception("Unexpected system error")
                print("An unexpected error occurred. See student_system.log.")
            finally:
                system.logger.info("Menu action %s completed", choice)
    except (EOFError, KeyboardInterrupt):
        print("\nProgram interrupted. No unsaved changes were kept.")
        if system:
            system.logger.warning("SYSTEM interrupted by the user")
    except StudentSystemError as error:
        print(f"System startup failed: {error}")
    finally:
        if system:
            system.logger.info("SYSTEM STOP")
        logging.shutdown()


if __name__ == "__main__":
    main()
