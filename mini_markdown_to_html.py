from datetime import date
import re

my_css = """
<style>
  body {
    background-color: #fcfffa;
    margin: 1.25rem;
    margin-bottom: 3rem;
    font-size: 1.05em;
  }

  code {
    color: indianred;
    font-weight: 700;
  }

  pre {
    background-color: #202020;
    color: #dedede;
    padding: 0.75rem 0.5rem;
    font-weight: normal !important;
  }

  li {
    padding: 0.25rem 0.5rem;
  }
</style>
"""

class Node:
# Creates a hierarchical tree structure with optional type, children, and text attributes
    def __init__(self, type_=None, children=None, text=''):
        '''Initializes the Node object.

        Parameters
        ----------
        type_
            The `type_` parameter is used to specify the type of the object being initialized.
        It is an optional parameter with a default value of `None`.

        children
            The `children` parameter is used to store a list of child nodes for a particular node
        in a tree structure. Each child node can have its own children, forming a hierarchical structure.
        The `children` parameter is initialized with an empty list if no value is provided.

        text
            The `text` parameter is a string parameter that allows you to initialize the `text` attribute
        of an object with a default value of an empty string if no value is provided during object creation.

        '''
        self.type_ = type_
        self.children = children if children is not None else []
        self.text = text


def escape_html(text, unescape=''):
    '''The function `escape_html` escapes special characters in a text and optionally unescapes a
    specific tag.

    Parameters
    ----------
    text
        The `text` parameter is the input text that you want to escape HTML characters in. This
    function replaces special characters like `&`, `<`, `>`, `"`, and `'` with their corresponding
    HTML entities to prevent HTML injection attacks.

    unescape
        The `unescape` parameter is used to specify a tag that should be unescaped in the HTML text.
    This means that if a particular tag is specified in the `unescape` parameter, it will be converted
    back to its original form in the returned HTML text.

    Returns
    -------
        The `escape_html` function returns the `escaped_text` after performing HTML escaping on the input
    `text` and optionally unescaping a specific tag specified by the `unescape` parameter.

    '''
    escaped_text = (
        text.replace('&', '&amp;')
        .replace('<', '&lt;')
        .replace('>', '&gt;')
        .replace('"', '&quot;')
        .replace("'", '&#39;')
    )
    if unescape:
        escaped_text = escaped_text.replace(
            f'&lt;{unescape}&gt;', f'<{unescape}>'
        ).replace(
            f'&lt;/{unescape}&gt;', f'</{unescape}>'
        )
    return escaped_text


def add_inline_tags(lines, i, regex, tag):
    '''The function `add_inline_tags` searches for a specific regex pattern in a line of text and wraps the
    matched substring with specified HTML tags.

    Parameters
    ----------
    lines
        The `lines` parameter is a list of strings representing lines of text. Each element in the list is
    a separate line of text.

    i
        The parameter `i` represents the index of the line in the `lines` list where you want to add inline
    tags based on the provided regex pattern and tag.

    regex
        The `regex` parameter is a regular expression pattern that is used to find specific patterns within
    the lines of text. This pattern is used to identify the substrings that need to be enclosed within
    the specified HTML tag.

    tag
        The `tag` parameter is a string representing the HTML tag that you want to add to the matched text
    in the given line. For example, if `tag` is set to "strong", the matched text will be wrapped in
    `<strong>` and `</strong>` tags.

    '''
    match = re.findall(r'' + regex + '', lines[i])
    for m in match:
        lines[i] = lines[i].replace(m, '<' + tag + '>' + m[1:-1] + '</' + tag + '>')


def parse_markdown(markdown_text):
    '''The `parse_markdown` function parses markdown text into a structured tree of nodes representing
    different elements like headings, code blocks, lists, and paragraphs.

    Parameters
    ----------
    markdown_text
        The `markdown_text` parameter is typically a string of text containing markdown syntax.

    Returns
    -------
        The `parse_markdown` function returns a tree structure representing the parsed markdown text.
    The root of the tree is a Node object with children nodes representing different elements such as
    headings, paragraphs, code blocks, and lists.

    '''
    lines = markdown_text.split('\n')
    root = Node('root')
    current_parent = root
    paragraph = ''
    code_block = ''
    in_list = False
    in_code_block = False
    bulleted_line = ''

    for i in range(len(lines) - 1):
        # Displayed code
        if lines[i].startswith('```'):
            if in_code_block:
                in_code_block = False
            else:
                in_code_block = True
            continue
        elif in_code_block:
            code_block += lines[i] + '\n'

            if lines[i + 1].startswith('```'):
                current_parent.children.append(
                    Node('pre', text=escape_html(code_block)))
                code_block = ''
            continue

        # Section headings
        if lines[i].startswith('#'):
            level = lines[i].count('#', 0, lines[i].find(' '))
            current_parent.children.append(
                Node(f'h{level}', text=escape_html(lines[i][level:].strip())))
            continue

        # Inline code
        add_inline_tags(lines, i, '\`[^`]+?\`', 'code')

        # Bulleted lists
        if lines[i].startswith('* '):
            if not in_list:
                current_parent = Node('ul')
                root.children.append(current_parent)
                in_list = True
            bulleted_line = ' ' + lines[i].strip()
        elif in_list:
            bulleted_line += ' ' + lines[i].strip()

        if bulleted_line:
            if lines[i + 1].startswith('* ') or lines[i + 1] == '':
                current_parent.children.append(
                    Node('li', text=escape_html(bulleted_line[2:].strip(), unescape='code')))

                if lines[i + 1] == '':
                    bulleted_line = ''
                    in_list = False
                    current_parent = root
            continue

        # Paragraphs
        paragraph += ' ' + lines[i]

        if lines[i + 1] == '':
            current_parent.children.append(
                Node('p', text=escape_html(paragraph.strip(), unescape='code')))
            paragraph = ''

    return root


def emit_minidown_as_html(input, output):
    '''The function `emit_minidown_as_html` takes an input file in markdown format, renders it as HTML, and
    writes the output to a specified file.

    Parameters
    ----------
    input
        The `input` parameter is typically a string containing markdown formatted text for converting to HTML.
    This text may include markdown syntax for formatting text, such as headers, lists, and emphasis.

    output
        The `output` parameter is the file path where the HTML output will be written. This is the file that
    will contain the HTML representation of the input content after processing.

    '''
    with open(output, "w") as f:
        f.write(render_html(input))


def render_html(node):
    '''The function `render_html` takes a node object and recursively generates HTML code based on its type
    and content.

    Parameters
    ----------
    node
        The `render_html` function takes a `node` object as input and generates HTML code based on the type
    of the node.

    Returns
    -------
        If the node type is "root", the `render_html` function returns the HTML structure for a
    full HTML document with CSS and body content. If the node type is one of the specified heading or
    paragraph types, it generates the corresponding HTML tag with the node's information. If the node
    type type is empty, it returns the an empty string.

    '''
    if node.type_ == "root":
        return (
            f"<html>{my_css}<body>\n"
            + "\n".join(render_html(child) for child in node.children)
            + "\n</body>\n</html>"
        )
    elif node.type_ in ["h1", "h2", "h3", "h4", "h5", "h6", "p", "pre", "li"]:
        return f"<{node.type_}>{node.text}</{node.type_}>"
    elif node.type_ == "ul":
        return (
            "<ul>\n"
            + "\n".join(render_html(child) for child in node.children)
            + "\n</ul>"
        )
    else:
        return node.text


def read_minidown_file(path):
    '''The function `read_minidown_file` reads a file at a given path, appends information about the author
    and date at the beginning of the file, and returns the modified content.

    Parameters
    ----------
    path
        The specified path tells the function `read_minidown_file` where to find the file to read.

    Returns
    -------
        The function `read_minidown_file` reads a file at the specified `path`, appends the current date
    and the user's name to the beginning of the file, and then returns the modified content of the file as a string.

    '''
    name = 'Ryan Levee'
    today = date.today().strftime("%B %d, %Y")
    name_position = re.compile(r"(?=^.{1})")
    rendered_by = f'```\nRendered by {name} on {today}\n```\n'

    with open(path, 'r') as f:
        f = f.read() + '\n'
        f = re.sub(name_position, rendered_by, f)

    return f


if __name__ == '__main__':
    # Convert the file to a modified string
    md = read_minidown_file('input.md')

    # Parse the markdown text into an abstract syntax tree
    ast = parse_markdown(md)

    # Emit the abstract syntax tree as HTML to a file
    emit_minidown_as_html(ast, "output.html")
