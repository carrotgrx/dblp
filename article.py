# -*- coding: UTF-8 -*-
import xml.sax


class DblpHandler(xml.sax.ContentHandler):
    def __init__(self, start_year, end_year, output_file):
        super().__init__()
        self.CurrentData = ""
        self.authors = []
        self.title = ""
        self.pages = ""
        self.year = ""
        self.volume = ""
        self.journal = ""
        self.number = ""
        self.ee = []
        self.url = []
        self.start_year = start_year
        self.end_year = end_year
        self.in_article = False
        self.output_file = output_file

    def write_to_file(self, data):
        with open(self.output_file, "a", encoding="utf-8") as file:
            file.write(data)

    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "article":
            self.in_article = True
            self.authors = []
            self.title = ""
            self.pages = ""
            self.year = ""
            self.volume = ""
            self.journal = ""
            self.number = ""
            self.ee = []
            self.url = []

    def endElement(self, tag):
        if self.in_article:
            if tag == "article" and self.is_valid_year(self.year):
                self.write_to_file("Authors: " + ", ".join(self.authors) + "\n")
                self.write_to_file(f"title: {self.title}\n")
                self.write_to_file(f"pages: {self.pages}\n")
                self.write_to_file(f"year: {self.year}\n")
                self.write_to_file(f"volume: {self.volume}\n")
                self.write_to_file(f"journal: {self.journal}\n")
                self.write_to_file("ee: " + ", ".join(self.ee) + "\n")
                self.write_to_file("url: " + ", ".join(self.url) + "\n\n")
            self.CurrentData = ""
            if tag == "article":
                self.in_article = False

    def characters(self, content):
        if self.in_article:
            if self.CurrentData == "author":
                self.authors.append(content)
            elif self.CurrentData == "title":
                self.title = content
            elif self.CurrentData == "pages":
                self.pages = content
            elif self.CurrentData == "year":
                self.year = content
            elif self.CurrentData == "volume":
                self.volume = content
            elif self.CurrentData == "journal":
                self.journal = content
            elif self.CurrentData == "number":
                self.number = content
            elif self.CurrentData == "ee":
                self.ee.append(content)
            elif self.CurrentData == "url":
                self.url.append(content)

    def is_valid_year(self, year):
        try:
            year = int(year)
            return self.start_year <= year <= self.end_year
        except ValueError:
            return False


if __name__ == "__main__":
    start_year = 2002
    end_year = 2006
    output_file = "Article.txt"

    # 清空输出文件，以防数据累积
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("")

    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    Handler = DblpHandler(start_year, end_year, output_file)
    parser.setContentHandler(Handler)
    parser.parse("dblp.xml")
