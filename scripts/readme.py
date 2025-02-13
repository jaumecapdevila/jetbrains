import os
import markdown
from bs4 import BeautifulSoup

SOURCE_FILE = os.path.join(os.path.dirname(__file__), '..', 'README.md')
DEST_PATH = os.path.join(os.path.dirname(__file__), '..', 'build')

if not os.path.exists(DEST_PATH):
    os.makedirs(DEST_PATH)

with open(SOURCE_FILE, 'r') as source:
    html = markdown.markdown(source.read())
    soup = BeautifulSoup(html, 'html.parser')
    # Reconstruct title
    new_title = soup.new_tag('p')
    new_title.string = "😱 A dark theme for JetBrains IDEs"
    soup.find('h1').replace_with(new_title)
    # Remove badges
    blockquote_h2 = soup.find('blockquote')
    blockquote_h2.find_next_sibling('p').decompose()
    blockquote_h2.decompose()
    # Set image widths
    for img in soup.find_all('img'):
        img['width'] = '700'
    # Add margin above images
    for img in soup.find_all('img'):
        img.insert_before(soup.new_tag('br'))
    # Remove installation
    installation_h2 = soup.find('h2', text='Installation')
    installation_h2.find_next('ol').decompose()
    installation_h2.decompose()
    # Remove team
    team_h2 = soup.find('h2', text="Team")
    for p in team_h2.find_all_next('p', limit=2):
        p.decompose()
    team_h2.decompose()
    # Remove license
    license_h2 = soup.find('h2', text='License')
    license_h2.find_next('p').decompose()
    license_h2.decompose()

with open(os.path.join(DEST_PATH, 'README.html'), 'w') as output_file:
    output_file.write(str(soup).strip())
