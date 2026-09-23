#!/usr/bin/env python3
"""
Generate README.md from structured JSON data
"""
import json
import os
import sys

# Paths
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_TEMPLATE = """# Awesome NZ Tech

A curated list of awesome tech resources, projects, and communities in Aotearoa New Zealand.

{content}

## Contributing

Contributions are welcome! Please see the [Contributing Guidelines](./CONTRIBUTING.md) for more details.
"""

DATA_FILE = os.path.join(ROOT_DIR, 'data', 'resources.json')
README_FILE = os.path.join(ROOT_DIR, 'README.md')
README_TEMPLATE = os.path.join(ROOT_DIR, 'scripts', 'readme_template.md')

def tidy_description(description):
    """Capitalise the first letter and end with a period, as the list conventions ask."""
    description = description.strip()
    for index, character in enumerate(description):
        if character.isalpha():
            description = description[:index] + character.upper() + description[index + 1:]
            break
    if description and description[-1] not in ".!?":
        description = description + "."
    return description


def generate_readme():
    """Generate README.md from the resources.json file"""
    
    # Load the data
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading JSON data: {e}")
        sys.exit(1)
    
    # Load the template
    try:
        with open(README_TEMPLATE, 'r') as f:
            template = f.read()
    except FileNotFoundError:
        # Create a default template if it doesn't exist
        template = DEFAULT_TEMPLATE
    
    # Sections come out in name order, so regenerating twice is byte identical.
    categories = sorted(
        data.get('categories', {}).values(), key=lambda category: category['name']
    )

    content_sections = []
    for category in categories:
        section = f"## {category['name']}\n\n{category['description']}\n"

        entries = category.get('entries', [])
        if entries:
            for entry in entries:
                description = tidy_description(entry['description'])
                section += f"\n- [{entry['name']}]({entry['url']}) - {description}"
        else:
            section += "\n- *No entries yet*"

        content_sections.append(section)

    content = "\n\n".join(content_sections)

    # The Contents section is the engine's job: make toc writes it after this.
    readme_content = template.format(content=content)
    
    # Write the README, or wherever --out points, which the tests use.
    out_file = README_FILE
    if "--out" in sys.argv:
        out_file = sys.argv[sys.argv.index("--out") + 1]

    with open(out_file, 'w') as f:
        f.write(readme_content)

    print(f"Wrote {os.path.relpath(out_file, ROOT_DIR)}")


if __name__ == "__main__":
    generate_readme()
