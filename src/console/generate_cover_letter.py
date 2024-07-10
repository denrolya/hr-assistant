import clipboard
from flask.cli import with_appcontext
from injector import inject

from src.blueprints.main import main_bp
from src.services.job_application_service import JobApplicationService
from src.services.printer import Printer
from src.services.groq_manager import GroqManager


@main_bp.cli.command('generate:cover-letter')
@with_appcontext
@inject
def generate_cover_letter_command():
    printer = Printer()
    jas = JobApplicationService(GroqManager())
    printer.print(
        content="Please copy the job description to your clipboard and press Enter when done:",
        color="bold_purple"
    )
    input()  # Wait for the user to press Enter
    job_description = clipboard.paste()
    cover_letter = jas.generate_cover_letter(job_description)

    printer.print(cover_letter[0], color="bold_purple")
    printer.print(cover_letter[1], color="bold_yellow")

    feedback = input(
        "Would you like to make any further changes to the cover letter? (Leave empty and press Enter when done): ")

    # Get feedback from the user
    while feedback:
        # Adjust the cover letter based on the feedback
        # This assumes you have a function adjust_cover_letter() that takes the current cover letter and feedback as arguments
        # and returns the adjusted cover letter
        cover_letter = jas.adjust_cover_letter(job_description, cover_letter, feedback)

        printer.print(cover_letter[0], color="bold_purple")
        printer.print(cover_letter[1], color="bold_yellow")

        # Get feedback from the user
        feedback = input(
            "Would you like to make any further changes to the cover letter? (Leave empty and press Enter when done): ")

    with open(cover_letter[0], 'w') as file:
        file.write(cover_letter[1])

    printer.print(f"Cover letter has been written to {cover_letter[0]}", color="bold_green")
