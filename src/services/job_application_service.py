import yaml
import json
import ast
import logging
import re
from datetime import datetime
from textwrap import dedent
from injector import inject

from src.utils import getenv
from src.services.groq_manager import GroqManager


class JobApplicationService:
    _job_description: dict
    _resume: dict
    _cover_letter_boilerplate: str

    _groq: GroqManager

    @inject
    def __init__(self, groq: GroqManager):
        self._groq = groq
        with open(getenv('BOILERPLATE_PATH'), 'r') as file:
            self._cover_letter_boilerplate = file.read()

            with open(getenv('CV_JSON_PATH'), 'rb') as file:
                self._resume = json.loads(file.read())

    def generate_cover_letter(self, job_description: dict):
        prompt = self._generate_cover_letter_prompt(
            job_description,
            self._resume,
            self._cover_letter_boilerplate
        )

        result_raw = self._groq.text(
            system_message=prompt.get('system_message'),
            user_message=prompt.get('user_message'),
            temp=0.2
        )

        result = ast.literal_eval(result_raw)

        header = dedent(f'''Name Surname
    name@gmail.com
    {datetime.today().strftime('%B %d, %Y')}

    ''')
        result[0] = f'assets/archive/{result[0]}'
        result[1] = header + result[1]

        return result

    def _minimize_job_description(self, job_description):
        return clean_and_validate_json_response(
            self._groq.text(
                system_message=dedent(f'''
                You are a machine that was built to analyze job descriptions and extract most important information from them.
                Your main objective would be to take the job description, extract all the necessary points from it:
                - Job title;
                - Company name;
                - Required number of years of experience;
                - Responsibilities;
                - Requirements;
                - Technology stack;
                - Corporate values;
                - Corporate culture;
                - Nice to have;
                - And other

                And result will be a JSON object with all these points.
            '''),
                user_message=dedent(f'''
                Here is the job description you need to minimize: {job_description};
                Response is strictly JSON object. No other text.
            '''),
                temp=0
            )
        )

    def _generate_cover_letter_prompt(
            self,
            job_description_json: dict,
            cv_json: dict,
            boilerplate: str
    ) -> dict[str, str]:
        return {
            'system_message': dedent(f'''
                You are a machine for creating cover letters for software development positions. 
                Your main objective is to take the cover letter, job description and CV and adjust the cover letter to the job description to match perfectly.
    
                Here are the rules you always follow:
                - Strictly follow the instructions from the boilerplate;
                - Always mention technologies candidate have worked with on each position. If job description mentions a technology that is not in resume, do not mention it;
                - Use multiline strings.
                - Your response is strictly an ARRAY OF 2 ELEMENTS:
                    - filename(should be in format cover.<company_name_snake_case>.<position_snake_case>.<candidate_name>.txt) 
                    - letter(MULTILINE STRING)
    
                Here are your settings:
                - Humour settings: 4/10;
                - Sophisticated terminology: 3/10;
                - Informal language: 6/10;            
                '''),
            'user_message': dedent(f'''
                Input Data:
                - Job description: {job_description_json}
                - Candidate's CV: {cv_json}
                - Cover letter boilerplate: {boilerplate}
                ''')
        }


def parse_yaml(yaml_string):
    try:
        data = yaml.safe_load(yaml_string)
        return data
    except yaml.YAMLError as e:
        logging.error(f"Error parsing YAML: {e}")
        return None


def clean_and_validate_json_response(response):
    try:
        response = re.sub(r'^[^{]*', '', response)
        response = re.sub(r'\\n', ' ', response)
        json_response = json.loads(response)

        return json_response

    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return None


def extract_json(s):
    start = s.find('{')
    if start == -1:
        return None

    s = s[start:]

    brace_count = 0
    for i, char in enumerate(s):
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0:
                json_str = s[:i + 1]
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError:
                    return None

    return None

def minify_json(json_string):
    return json.dumps(json_string, separators=(',', ":"))
