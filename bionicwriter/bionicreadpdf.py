from dataclasses import dataclass, field
import logging
from typing import Any
import pdfplumber
from nltk.tokenize import word_tokenize
from math import ceil
import random
from datetime import datetime

import reportlab.rl_config
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate

from tqdm import tqdm

reportlab.rl_config.warnOnMissingFontGlyphs = 0  # type: ignore

from bionicwriter.config import BionicConfig
from bionicwriter.dir import change_dir

now = datetime.now()
date = now.strftime("%y%m%d")
logger = logging.getLogger("bionicreadformatter")

def calc_fixation(word: str) -> int:
    return ceil((len(word)* 0.5))

class BionicWritePDF:
    def __init__(self, config: BionicConfig, min_fixation_length: int):
        self.config = config
        self.target = self.config.target
        self.min_fixation_length = min_fixation_length
        self.pdfmetrics = pdfmetrics
        self.export_title = f"{date}_Book_{random.randint(0,100)}.pdf"
        self.date = now.strftime("%B %d, %Y")
        self.story = []
        self.export_dir = f"{date}_{self.config.export_dir}"
        self.doc = SimpleDocTemplate(
            self.export_title,
            pagesize=letter,
            rightMargin=inch * 1.5,
            leftMargin=inch * 1.5,
            topMargin=inch,
            bottomMargin=inch,
            title=self.export_title
        )
        self.styles = getSampleStyleSheet()
        self.preprints: list[str] = []

    def run(self):
        self.register_fonts()
        self.add_styles()
        
        with change_dir(self.config.export_dir):
            self.pdf_to_bionic()
            self.pdf_processing()

    def pdf_to_bionic(self) -> list[str]:
        with pdfplumber.open(self.target) as study:
            pages: list[Any] = study.pages
            study_length = len(pages)
            pages_to_check = [*pages][:study_length]
            for page_number, page in enumerate(tqdm(pages_to_check, desc="Bionicly Transcribing", unit="pages")):
                page: str = pages[page_number].extract_text(
                    x_tolerance=.5, y_tolerance=0
                )
                logger.info(
                    f"[bionicreadformatter]: Processing Page {page_number} "
                    f"of {study_length-1} | {self.target}...",
                )
                print(page)
                page.replace('\n','<br />')
                self.preprints.append(page)
            return self.preprints

    def pdf_processing(self):
        for paragraph in self.preprints:
            ptext = self.compute_bolded_tokens(paragraph)
            self.story.append(Paragraph(ptext, self.styles["Main"]))
        
        self.doc.build(self.story)
                # The preprints are stripped of extraneous
                # characters and all made lower case.
            #postprint = [re.sub(r"\W+", " ", manuscript) for manuscript in manuscripts]
                # The ensuing manuscripts are stripped of
                # lingering whitespace and non-alphanumeric characters.

    def compute_bolded_tokens(self, text_list: list[str]) -> str:
        """Takes a lowercase string, now removed of its non-alphanumeric characters.
        It returns (as a list comprehension) a parsed and tokenized
        version of the text, with stopwords and names removed.
        """

        tokens: list[str] = word_tokenize(str(text_list))
        punctuation: list[str] = ['.',',','’',':','[',']',';']
        ptext: str = ''

        for word in tokens:
            fixation = calc_fixation(word)

            if word in punctuation:
                ptext += word.strip()
                
            elif fixation >= self.min_fixation_length:
                ptext += ' ' + f'<b>{word[:fixation]}</b>{word[fixation:]}'

            else:
                ptext += ' ' + word

        return ptext

    def register_fonts(self):
        """This registers the fonts for use in the PDF, querying them from the config.json file."""
        self.pdfmetrics.registerFont(TTFont("AtkinsonHyperlegible-Regular", self.config.font_regular))
        self.pdfmetrics.registerFont(TTFont("AtkinsonHyperlegible-Bold", self.config.font_bold))
        self.pdfmetrics.registerFont(TTFont("AtkinsonHyperlegible-Italic", self.config.font_italic))
        self.pdfmetrics.registerFont(TTFont("AtkinsonHyperlegible-BoldItalic", self.config.font_bolditalic))
        self.pdfmetrics.registerFontFamily(
            "AtkinsonHyperlegible",
            normal="AtkinsonHyperlegible-Regular",
            bold="AtkinsonHyperlegible-Bold",
            italic="AtkinsonHyperlegible-Italic",
            boldItalic="AtkinsonHyperlegible-BoldItalic"
        )
    
    def add_styles(self):
        self.styles.add(
            ParagraphStyle(
                "Main",
                parent=self.styles["Normal"],
                fontName="AtkinsonHyperlegible-Regular",
                spaceBefore=0.5 * inch,
                fontSize=13,
                leading=26,
                firstLineIndent=0.5 * inch,
            )
        )