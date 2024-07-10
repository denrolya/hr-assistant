# HR Assistant

# Running the app
1. [Install NGRok](https://ngrok.com/download)
2. Run `ngrok http http://localhost:[host_port]` to get a public URL
3. Create dedicated virtualenv: `python -m venv .venv`
4. Activate virtualenv: `source .venv/bin/activate`
5. Install requirements in current virtualenv: `pip install -r requirements.txt`
6. `cp .env.example .env` and fill in empty values in `.env` file
7. Run app
   1. Locally: `flask run` or `python app.py`
   2. Docker: `docker build -t [image_name] . && docker run -p [host_port]:[container_port] [image_name]`


## Console commands
* Generate cover letter console command: `flask main generate:cover-letter`
* List all available routes:`flask routes`

### <<<<<<< DEPRECATED Generate cover letter: >>>>>>>>
1. Add your CV as json. You can use ```python app.py -u``` to generate it but make sure u have a corresponding pdf file in `assets/`
2. Find a job description u wanna work with
3. Run `python app.py -c` and then hit enter when u have job description copied in ur clipboard


## Database operations I performed
```bask
flask db init
flask db migrate -m "initial commit"
flas db upgrade
```