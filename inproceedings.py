# -*- coding: UTF-8 -*-
import xml.sax


class DblpHandler(xml.sax.ContentHandler):
    def __init__(self, start_year, end_year, output_file):
        super().__init__()
        self.CurrentData = ""
        self.authors = []
        self.title = ""
        self.book_title = ""
        self.year = ""
        self.volume = ""
        self.number = ""
        self.pages = ""
        self.month = ""
        self.organization = ""
        self.start_year = start_year
        self.end_year = end_year
        self.in_article = False
        self.output_file = output_file

    def write_to_file(self, data):
        with open(self.output_file, "a", encoding="utf-8") as file:
            file.write(data)

    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "inproceedings":
            self.in_article = True
            self.authors = []
            self.title = ""
            self.book_title = ""
            self.year = ""
            self.volume = ""
            self.number = ""
            self.pages = ""
            self.month = ""
            self.organization = ""

    def endElement(self, tag):
        if self.in_article:
            if tag == "inproceedings" and self.is_valid_year(self.year):
                self.write_to_file("Authors: " + ", ".join(self.authors) + "\n")
                self.write_to_file(f"title: {self.title}\n")
                self.write_to_file(f"booktitle: {self.book_title}\n")
                self.write_to_file(f"year: {self.year}\n")
                self.write_to_file(f"volume: {self.volume}\n")
                self.write_to_file(f"number: {self.number}\n")
                self.write_to_file(f"pages: {self.pages}\n")
                self.write_to_file(f"month: {self.month}\n")
                self.write_to_file(f"organization: {self.organization}\n\n")
            self.CurrentData = ""
            if tag == "inproceedings":
                self.in_article = False

    def characters(self, content):
        if self.in_article:
            if self.CurrentData == "author":
                self.authors.append(content)
            elif self.CurrentData == "title":
                self.title = content
            elif self.CurrentData == "booktitle":
                self.book_title = content
            elif self.CurrentData == "year":
                self.year = content
            elif self.CurrentData == "volume":
                self.volume = content
            elif self.CurrentData == "number":
                self.number = content
            elif self.CurrentData == "pages":
                self.pages = content
            elif self.CurrentData == "month":
                self.month = content
            elif self.CurrentData == "organization":
                self.organization = content

    def is_valid_year(self, year):
        try:
            return self.start_year <= int(year) <= self.end_year
        except ValueError:
            return False


if __name__ == "__main__":
    start_year = 2002
    end_year = 2006
    output_file = "Inproceedings.txt"

    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    Handler = DblpHandler(start_year, end_year, output_file)
    parser.setContentHandler(Handler)
    parser.parse("dblp.xml")
