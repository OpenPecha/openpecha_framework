from pecha_framework.pipeline import Document, Pipe


class StamWriter(Pipe):
    name = "stam_writer"

    def __call__(self, doc: Document):
        """
        Write the Document object to STAM format.
        """
        print(doc.ann_text_mapping)
        return doc
