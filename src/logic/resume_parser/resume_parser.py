import spacy
from spacy.matcher import Matcher

from src.logic.resume_parser.utils import *


class ResumeParser(object):
    def __init__(self, resume, pdf=True):
        nlp = spacy.load("en_core_web_sm")
        self.__matcher = Matcher(nlp.vocab)
        self.__details = {
            "name": None,
            "email": None,
            "mobile_number": None,
            "skills": None,
            "education": None,
            "experience": None,
            "competencies": None,
            "measurable_results": None,
        }
        self.__resume = resume

        if pdf:
            self.__text_raw = extract_text(
                self.__resume, os.path.splitext(self.__resume)[1]
            )
            self.__text = " ".join(self.__text_raw.split())
        else:
            self.__text_raw = resume
            self.__text = resume
        self.__nlp = nlp(self.__text)
        self.__noun_chunks = list(self.__nlp.noun_chunks)
        self.__get_basic_details()

    def get_extracted_data(self):
        return self.__details

    def __get_basic_details(self):
        name = extract_name(self.__nlp, matcher=self.__matcher)
        email = extract_email(self.__text)
        mobile = extract_mobile_number(self.__text)
        skills = extract_skills(self.__nlp, self.__noun_chunks)
        edu = extract_education(
            [sent.string.strip() for sent in self.__nlp.sents]
        )
        experience = extract_experience(self.__text)
        entities = extract_entity_sections(self.__text_raw)
        self.__details["name"] = name
        self.__details["email"] = email
        self.__details["mobile_number"] = mobile
        self.__details["skills"] = skills
        # self.__details['education'] = entities['education']
        self.__details["education"] = edu
        self.__details["experience"] = experience
        try:
            self.__details["competencies"] = extract_competencies(
                self.__text_raw, entities["experience"]
            )
            self.__details["measurable_results"] = extract_measurable_results(
                self.__text_raw, entities["experience"]
            )
        except KeyError:
            self.__details["competencies"] = []
            self.__details["measurable_results"] = []
        return


def job_result_wrapper(resume, pdf: bool):
    parser = ResumeParser(resume, pdf)
    return parser.get_extracted_data()


# if __name__ == '__main__':
#
#     # pool = mp.Pool(mp.cpu_count())
#     resumes = []
#     data = []
#     for root, directories, filenames in os.walk('/Users/vishal/Documents/code/ResumeParser/resumes'):
#         for filename in filenames:
#             file = os.path.join(root, filename)
#             resumes.append(file)
#
#     # results = [pool.apply_async(resume_result_wrapper, args=(x,)) for x in resumes]
#     result = job_result_wrapper(resumes[0], True)
#     # results = [p.get() for p in results]
#     print(result)
#     # pprint.pprint(results)
