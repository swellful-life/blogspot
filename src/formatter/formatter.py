from markdown import markdown
from bs4 import BeautifulSoup

class CommentFormatter:
    def __init__(self, markdown_extensions=None):
        self.markdown_extensions = markdown_extensions or ["codehilite","fenced_code", "tables"]

    def markdown_to_html(self, markdown_text):
        html = markdown(markdown_text, extensions=self.markdown_extensions,output_format="html")

        return html

    def clean_html(self, html):
        soup = BeautifulSoup(html, "html.parser")

        for blockquote in soup.find_all("blockquote"):
            for p in blockquote.find_all("p"):
                p.unwrap()
        
        for img in soup.find_all("img"):
            if img.parent.name == "p":
                img.parent.unwrap()

        for table in soup.find_all("table"):
            if table.parent.name != "div" or "table-wrapper" not in table.parent.get("class", []):
                wrapper = soup.new_tag("div", **{"class": "table-wrapper"})
                table.insert_before(wrapper)
                wrapper.append(table)

        return str(soup)
