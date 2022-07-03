from time import perf_counter

from bionicwriter.bionicreadpdf import BionicWritePDF
from bionicwriter.config import read_config
from bionicwriter.logger import logger

config = read_config("./config.json")

def main() -> None:
    """jobscraper takes the provided querystring, searches for job results,
    and for each of those job results generates a cover letter.
    """
    start = perf_counter()
    bio_write = BionicWritePDF(config,3)
    bio_write.run()
    elapsed = perf_counter() - start
    logger.info("Job search finished in %s seconds.", elapsed)  # type: ignore

if __name__ == "__main__":
    main()

'''
def epub_to_bionic(target):
        search_terms: list[str] = [ path.join(target, file) 
                        for file in listdir(target) 
                        if fnmatch(path.basename(file), "*.html")
                        ]
        all_pages:str = str([read_chapters_into_list(term) for term in search_terms])
        make_book_txt(all_pages)
        
def make_book_txt(text: str):
    """This creates the cover letter as a .txt file."""

    with open(
        f"22XX__BookIdeaProgram.txt", "w", encoding="utf-8"
    ) as text_letter:
        text_letter.write(text)

def read_chapters_into_list(term):
    with open(file=term, mode = 'r', encoding='utf-8') as book:
        chapters = [item for item in book]
        return [BeautifulSoup(chapter, "html.parser").text for chapter in chapters]
'''
#if __name__ == '__main__':
#    epub_to_bionic('/Users/johnfallot/Downloads/bionic-reading-py-master/OEBPS')