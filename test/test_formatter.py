import pytest
import textwrap
from src.formatter.formatter import CommentFormatter

@pytest.fixture
def formatter():
    return CommentFormatter()

def test_markdown_to_html_with_code_block(formatter):
    markdown_text = textwrap.dedent("""
    Here is a code block:

    ```python
    def hello():
        print("Hello, World!")
    ```
    """)
    expected_html = textwrap.dedent("""
    <p>Here is a code block:</p>
    <div class="codehilite"><pre><span></span><code><span class="k">def</span> <span class="nf">hello</span><span class="p">():</span>
        <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;Hello, World!&quot;</span><span class="p">)</span>
    </code></pre></div>
    """)
    html = formatter.markdown_to_html(markdown_text)

    assert html.strip() == expected_html.strip()

def test_markdown_to_html_with_table(formatter):
    markdown_text = textwrap.dedent("""
    | Header 1 | Header 2 |
    |----------|----------|
    | Row 1    | Data 1   |
    | Row 2    | Data 2   |
    """)

    expected_html = (
        '<table>\n'
        '<thead>\n'
        '<tr>\n'
        '<th>Header 1</th>\n'
        '<th>Header 2</th>\n'
        '</tr>\n'
        '</thead>\n'
        '<tbody>\n'
        '<tr>\n'
        '<td>Row 1</td>\n'
        '<td>Data 1</td>\n'
        '</tr>\n'
        '<tr>\n'
        '<td>Row 2</td>\n'
        '<td>Data 2</td>\n'
        '</tr>\n'
        '</tbody>\n'
        '</table>'
    )

    html = formatter.markdown_to_html(markdown_text)

    assert html.strip() == expected_html.strip()


def test_clean_html(formatter):
    markdown_text = textwrap.dedent("""
    > This is a blockquote.
    ![Image](image.png)
                                    
    ![Image](image.png)                                
                                    
    | Header 1 | Header 2 |
    |----------|----------|
    | Row 1    | Data 1   |
    | Row 2    | Data 2   |

    """)
    html = formatter.markdown_to_html(markdown_text)
    cleaned_html = formatter.clean_html(html)

    expected_html = textwrap.dedent("""
        <blockquote>
        This is a blockquote.
        <img alt="Image" src="image.png"/>
        </blockquote>
        <img alt="Image" src="image.png"/> 
        <div class="table-wrapper"><table>
        <thead>
        <tr>
        <th>Header 1</th>
        <th>Header 2</th>
        </tr>
        </thead>
        <tbody>
        <tr>
        <td>Row 1</td>
        <td>Data 1</td>
        </tr>
        <tr>
        <td>Row 2</td>
        <td>Data 2</td>
        </tr>
        </tbody>
        </table></div>                                
    """)

    assert cleaned_html.strip() == expected_html.strip()