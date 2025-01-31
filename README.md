### Mini Markdown to HTML Converter

## Overview

This Python script converts Markdown text into HTML. It parses the Markdown text, builds a hierarchical tree structure, and generates the corresponding HTML output. This script is part of my programming portfolio and demonstrates my ability to work with text processing, regular expressions, and tree data structures.

## Features

**Markdown Parsing**: Converts Markdown text into a structured tree of nodes.

**HTML Generation**: Renders the parsed Markdown as HTML.

**Inline Tag Handling**: Supports inline tags like code snippets.

**List Handling**: Processes bulleted lists.

**Code Block Handling**: Supports code blocks with proper escaping of HTML characters.

## Installation

To use this script, you need to have Python installed on your system. You can download Python from python.org.

## Usage

1. Clone the repository:

        git clone https://github.com/yourusername/mini_markdown_to_html.git
        cd mini_markdown_to_html

2. Prepare your Markdown input file (e.g., input.md).

3. Run the script:

        python mini_markdown_to_html.py

4. The HTML output will be saved to output.html.

## Code Explanation

**Node Class**

The `Node` class creates a hierarchical tree structure with optional type, children, and text attributes.

**escape_html Function**

The `escape_html` function escapes special characters in a text and optionally unescapes a specific tag to prevent HTML injection attacks.

**add_inline_tags Function**

The `add_inline_tags` function searches for a specific regex pattern in a line of text and wraps the matched substring with specified HTML tags.

**parse_markdown Function**

The `parse_markdown` function parses Markdown text into a structured tree of nodes representing different elements like headings, code blocks, lists, and paragraphs.

**emit_minidown_as_html Function**

The `emit_minidown_as_html` function takes an input file in Markdown format, renders it as HTML, and writes the output to a specified file.

**render_html Function**

The `render_html` function takes a node object and recursively generates HTML code based on its type and content.

**read_minidown_file Function**

The `read_minidown_file` function reads a file at a given path, appends information about the author and date at the beginning of the file, and returns the modified content.

## Example

Here is an example of how to use the script:

1. Create a Markdown file (input.md) with the following content:

```
# Sample Markdown

This is a paragraph with `inline code`.

* Bullet point 1
* Bullet point 2
```

2. Run the script:

```
python mini_markdown_to_html.py
```

3. The output HTML (output.html) will look like this:

```
<h1>Sample Markdown</h1>
<p>This is a paragraph with <code>inline code</code>.</p>
<ul>
    <li>Bullet point 1</li>
    <li>Bullet point 2</li>
</ul>
```

## Author

Ryan Levee

## License

This project is licensed under the MIT License - see the LICENSE file for details.