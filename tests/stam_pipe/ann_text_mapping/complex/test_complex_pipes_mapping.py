from pathlib import Path

from pecha_framework import Document, Pipe, Pipeline


class PageTextExtractor(Pipe):
    name = "page_text_extractor"

    def __call__(self, doc: Document):
        """
        Input: volume text as doc.text
        Output: Page texts as doc.pages (list of strings)
        """
        pages = []
        for page in doc.text.split("\n\n"):
            pages.append(page)
        setattr(doc, "pages", pages)
        return doc


class PageContentExtractor(Pipe):
    name = "page_content_extractor"
    requires = ["page_text_extractor"]

    def __call__(self, doc: Document):
        """
        Input: doc.pages (list of strings)

        Each Page is in the following format
              Page PageNumber
              Page Content
        Output: Extract Page Content and its Span.
        """
        for idx, page in enumerate(getattr(doc, "pages")):
            page_no, _ = page.split("\n", 1)[0], page.split("\n", 1)[1]
            doc.annotations[page_no] = [(len(page_no) + 1, len(page))]
            doc.resource_ann_mapping.append((f"pages[{idx}]", page_no))

        return doc


def test_storing_resource_ann_mapping():
    data = Path(__file__).parent / "data"
    volume_text = Path(data / "V001.txt").read_text(encoding="utf-8")
    doc = Document(text=volume_text)
    pipeline = Pipeline(["page_text_extractor", "page_content_extractor"])
    doc = pipeline(doc)

    # Check if the pages are extracted correctly
    assert doc.get_attr("pages[0]") == "Page 1\nBDRC"
    assert doc.get_attr("pages[1]") == "Page 2\nChonjuk"
    assert doc.get_attr("pages[2]") == "Page 3\nMT Data"

    # Check if the annotations are stored correctly
    assert doc.annotations == {
        "Page 1": [(7, 11)],
        "Page 2": [(7, 14)],
        "Page 3": [(7, 14)],
    }
    # Check if the ann text mapping is stored correctly
    assert doc.resource_ann_mapping == [
        ("pages[0]", "Page 1"),
        ("pages[1]", "Page 2"),
        ("pages[2]", "Page 3"),
    ]

    # Check if we are able to access the page content using the resource_ann_mapping
    assert doc.get_attr("pages[0]")[7:11] == "BDRC"
    assert doc.get_attr("pages[1]")[7:14] == "Chonjuk"
    assert doc.get_attr("pages[2]")[7:14] == "MT Data"


test_storing_resource_ann_mapping()
