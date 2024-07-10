import datetime
from flask import request, render_template
from src.services.printer import Printer
from src.services.job_application_service import JobApplicationService
from src.blueprints.main import main_bp


@main_bp.route('/', methods=['GET', 'POST'])
def index(printer: Printer, jas: JobApplicationService):
    if request.method == 'POST':
        job_description = request.form['job_description']
        cover_letter = jas.generate_cover_letter(job_description)
        printer.print(cover_letter, color='magenta')

        return render_template('index.html', utc_dt=datetime.datetime.utcnow(), cover_letter=cover_letter)

    return render_template('index.html', utc_dt=datetime.datetime.utcnow())
