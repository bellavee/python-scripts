import ebooklib
from ebooklib import epub
import re

def create_epub_from_text(text_file, epub_file):
    with open(text_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # Create a new EPUB book
    book = epub.EpubBook()

    # Add metadata
    book.set_identifier('id123456')
    book.set_title('Sample book')
    book.set_language('en')
    book.add_author('Author Name')

    # Define the CSS style
    css_style = '''
    h1 {
        font-size: 14pt;
        font-weight: bold;
        page-break-before: always;
        text-align: center;
    }
    p {
        line-height: 1.5;
    }
    '''
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=css_style)
    book.add_item(nav_css)

    # Regular expression to match chapter titles
    chapter_pattern = re.compile(r'(Chapter \d{2} [^\n]+)\n(.*?)\n(?=Chapter \d{2} |$)', re.DOTALL)
    chapters = chapter_pattern.findall(content)

    epub_chapters = []

    for i, (chapter_title, chapter_text) in enumerate(chapters):
        # Remove the word "Chapter" from the title
        chapter_title = chapter_title.replace('Chapter ', '')

        # Split the chapter text into lines and wrap each line in <p> tags
        paragraphs = ['<p>{}</p>'.format(line) for line in chapter_text.strip().split('\n') if line.strip()]

        # Create chapter
        chapter = epub.EpubHtml(title=chapter_title, file_name=f'chap_{i+1}.xhtml', lang='en')
        chapter.content = u'<h1>{}</h1>{}'.format(chapter_title, ''.join(paragraphs))
        chapter.add_item(nav_css)  # Link CSS to this chapter
        
        book.add_item(chapter)
        epub_chapters.append(chapter)

    # Define book spine and table of contents
    book.spine = ['nav'] + epub_chapters
    book.toc = tuple(epub_chapters)

    # Add navigation files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Write the EPUB file
    epub.write_epub(epub_file, book, {})

    print("Created")



def format_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    content = content.replace(' ,', ',')
    content = content.replace(' .', '.')
    content = content.replace(' !', '!')
    content = content.replace(' ?', '?')

    paragraphs = content.split('\n')  # Splitting the content into paragraphs
    capitalized_paragraphs = []

    for paragraph in paragraphs:
        # Strip leading and trailing whitespace and capitalize the first letter
        paragraph = paragraph.strip()
        if paragraph:
            capitalized_paragraphs.append(paragraph[0].upper() + paragraph[1:])

    # Join the paragraphs back into a single string, preserving paragraph breaks
    capitalized_content = '\n'.join(capitalized_paragraphs)

    # Write the modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(capitalized_content)
    
    print("Formatted")



# Replace 'your_file.txt' with the path to your text file
# format_text('812465.txt')

# Replace 'your_text_file.txt' and 'output_book.epub' with your file names
create_epub_from_text('812465.txt', 'output_book.epub')