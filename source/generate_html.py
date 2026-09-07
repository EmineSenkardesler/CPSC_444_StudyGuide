#!/usr/bin/env python3
"""Generate comprehensive HTML study guide from markdown files"""

import re
import os

BASE_PATH = '/home/emine2/cpsc444-study-guide'

# Module files in order
MODULES = [
    ('home', 'README.md', '🏠 Home & Overview'),
    ('paths', 'Study_Paths.md', '🗺️ Study Paths'),
    ('module1', 'Module_01_Foundations.md', '📚 Module 01: Foundations'),
    ('module2', 'Module_02_Statistical_Foundations.md', '📊 Module 02: Statistical Foundations'),
    ('module3', 'Module_03_Geospatial_Fundamentals.md', '🗺️ Module 03: Geospatial Fundamentals'),
    ('module4', 'Module_04_Spatial_Statistics.md', '📈 Module 04: Spatial Statistics'),
    ('module5', 'Module_05_Advanced_Regression.md', '🔬 Module 05: Advanced Regression'),
    ('module6', 'Module_06_Mixed_Models.md', '🏗️ Module 06: Mixed Models'),
    ('module7', 'Module_07_Machine_Learning.md', '🤖 Module 07: Machine Learning'),
    ('module8', 'Module_08_Specialized_Applications.md', '🌾 Module 08: Specialized Applications'),
    ('reference', 'Quick_Reference.md', '📖 Quick Reference'),
]

def convert_md_to_html(md_text):
    """Convert markdown to HTML with proper formatting"""
    lines = md_text.split('\n')
    html_lines = []
    in_code_block = False
    in_list = False
    code_lang = ''

    i = 0
    while i < len(lines):
        line = lines[i]

        # Handle code blocks
        if line.strip().startswith('```'):
            if not in_code_block:
                in_code_block = True
                code_lang = line.strip()[3:].strip()
                html_lines.append('<pre><code>')
            else:
                in_code_block = False
                html_lines.append('</code></pre>')
            i += 1
            continue

        if in_code_block:
            # Escape HTML in code
            line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            html_lines.append(line)
            i += 1
            continue

        # Handle headers
        if line.startswith('# ') and not line.startswith('## '):
            html_lines.append(f'<h1>{line[2:].strip()}</h1>')
        elif line.startswith('## '):
            html_lines.append(f'<h2>{line[3:].strip()}</h2>')
        elif line.startswith('### '):
            html_lines.append(f'<h3>{line[4:].strip()}</h3>')
        elif line.startswith('#### '):
            html_lines.append(f'<h4>{line[5:].strip()}</h4>')

        # Handle horizontal rules
        elif line.strip() == '---':
            html_lines.append('<hr>')

        # Handle lists
        elif line.strip().startswith('- [ ]'):
            if not in_list:
                html_lines.append('<ul class="checkbox-list">')
                in_list = True
            content = line.strip()[5:].strip()
            content = apply_inline_formatting(content)
            html_lines.append(f'<li>{content}</li>')
        elif line.strip().startswith('- '):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            content = line.strip()[2:].strip()
            content = apply_inline_formatting(content)
            html_lines.append(f'<li>{content}</li>')
        elif line.strip().startswith('1. ') or (len(line) > 2 and line[0].isdigit() and line[1:3] == '. '):
            if not in_list:
                html_lines.append('<ol>')
                in_list = 'ol'
            content = re.sub(r'^\d+\.\s+', '', line.strip())
            content = apply_inline_formatting(content)
            html_lines.append(f'<li>{content}</li>')

        # Handle empty lines (close lists)
        elif not line.strip():
            if in_list:
                html_lines.append('</ol>' if in_list == 'ol' else '</ul>')
                in_list = False
            html_lines.append('')

        # Regular paragraphs
        else:
            if in_list and not line.startswith('  '):
                html_lines.append('</ol>' if in_list == 'ol' else '</ul>')
                in_list = False

            content = apply_inline_formatting(line.strip())
            if content and not content.startswith('<'):
                html_lines.append(f'<p>{content}</p>')
            elif content:
                html_lines.append(content)

        i += 1

    # Close any open lists
    if in_list:
        html_lines.append('</ol>' if in_list == 'ol' else '</ul>')

    return '\n'.join(html_lines)

def apply_inline_formatting(text):
    """Apply inline markdown formatting"""
    # Links
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)

    # Bold
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)

    # Italic
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)

    # Inline code
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)

    return text

def read_module(filename):
    """Read module file content"""
    filepath = os.path.join(BASE_PATH, filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"<p>Error loading content: {e}</p>"

def generate_nav_items():
    """Generate navigation menu items"""
    nav_html = []
    for module_id, filename, title in MODULES:
        # Extract difficulty from file if it's a module
        difficulty_html = ''
        if 'Module_' in filename:
            content = read_module(filename)
            if '⭐' in content[:500]:
                # Extract difficulty line
                for line in content.split('\n')[:20]:
                    if 'Difficulty' in line or '⭐' in line:
                        difficulty_html = f'<span class="difficulty">{line.strip().replace("**", "").replace("Difficulty:", "").replace("Time Estimate:", "| Time:").strip()}</span>'
                        break

        nav_html.append(f'''                <li class="nav-item">
                    <a class="nav-link{' active' if module_id == 'home' else ''}" onclick="showSection('{module_id}')">
                        {title}
                        {difficulty_html}
                    </a>
                </li>''')

    return '\n'.join(nav_html)

def generate_content_sections():
    """Generate all content sections"""
    sections_html = []

    for idx, (module_id, filename, title) in enumerate(MODULES):
        content = read_module(filename)
        html_content = convert_md_to_html(content)

        # Determine navigation buttons
        prev_btn = ''
        next_btn = ''

        if idx > 0:
            prev_id, _, prev_title = MODULES[idx - 1]
            prev_btn = f'<button class="btn btn-secondary" onclick="showSection(\'{prev_id}\')">← {prev_title.split(":")[0].replace("🏠", "Home").replace("🗺️", "Paths").replace("📖", "Reference")}</button>'
        else:
            prev_btn = '<button class="btn btn-secondary" disabled>← Previous</button>'

        if idx < len(MODULES) - 1:
            next_id, _, next_title = MODULES[idx + 1]
            next_btn = f'<button class="btn btn-primary" onclick="showSection(\'{next_id}\')">{next_title.split(":")[0].replace("🏠", "Home").replace("🗺️", "Paths").replace("📖", "Reference")} →</button>'
        else:
            next_btn = '<button class="btn btn-primary" onclick="showSection(\'home\')">Back to Home</button>'

        section_html = f'''
            <!-- {title.upper()} -->
            <section id="{module_id}" class="content-section{' active' if module_id == 'home' else ''}">
                {html_content}

                <div class="nav-buttons">
                    {prev_btn}
                    {next_btn}
                </div>
            </section>'''

        sections_html.append(section_html)

    return '\n'.join(sections_html)

# Read the CSS and JavaScript from the template
HTML_TEMPLATE_HEAD = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CPSC 444 Study Guide - Complete Course</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }

        .container {
            display: flex;
            height: 100vh;
            overflow: hidden;
        }

        /* Sidebar Navigation */
        .sidebar {
            width: 300px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            overflow-y: auto;
            box-shadow: 2px 0 10px rgba(0,0,0,0.1);
        }

        .sidebar-header {
            padding: 20px;
            background: rgba(0,0,0,0.2);
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }

        .sidebar-header h1 {
            font-size: 1.4em;
            margin-bottom: 5px;
        }

        .sidebar-header p {
            font-size: 0.85em;
            opacity: 0.9;
        }

        .nav-menu {
            list-style: none;
            padding: 10px 0;
        }

        .nav-item {
            margin: 2px 10px;
        }

        .nav-link {
            display: block;
            padding: 12px 15px;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            transition: all 0.3s ease;
            cursor: pointer;
            font-size: 0.95em;
        }

        .nav-link:hover {
            background: rgba(255,255,255,0.15);
            transform: translateX(5px);
        }

        .nav-link.active {
            background: rgba(255,255,255,0.25);
            font-weight: 600;
        }

        .nav-link .difficulty {
            display: block;
            font-size: 0.8em;
            opacity: 0.8;
            margin-top: 3px;
        }

        /* Main Content Area */
        .main-content {
            flex: 1;
            overflow-y: auto;
            background: white;
        }

        .content-section {
            display: none;
            padding: 40px 60px;
            max-width: 1000px;
            margin: 0 auto;
            animation: fadeIn 0.3s ease-in;
        }

        .content-section.active {
            display: block;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Typography */
        h1 {
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 10px;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }

        h2 {
            color: #764ba2;
            font-size: 2em;
            margin-top: 30px;
            margin-bottom: 15px;
        }

        h3 {
            color: #555;
            font-size: 1.5em;
            margin-top: 25px;
            margin-bottom: 12px;
        }

        h4 {
            color: #666;
            font-size: 1.2em;
            margin-top: 20px;
            margin-bottom: 10px;
        }

        p {
            margin-bottom: 15px;
            text-align: justify;
        }

        hr {
            margin: 30px 0;
            border: none;
            border-top: 2px solid #eee;
        }

        /* Lists */
        ul, ol {
            margin: 15px 0 15px 30px;
        }

        li {
            margin-bottom: 8px;
        }

        /* Code Blocks */
        pre {
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 20px 0;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            line-height: 1.5;
        }

        code {
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            color: #d63384;
            font-size: 0.9em;
        }

        pre code {
            background: transparent;
            padding: 0;
            color: #f8f8f2;
        }

        /* Checkboxes */
        .checkbox-list {
            list-style: none;
            margin-left: 0;
        }

        .checkbox-list li:before {
            content: "☐ ";
            color: #667eea;
            font-weight: bold;
            margin-right: 8px;
        }

        /* Navigation Buttons */
        .nav-buttons {
            display: flex;
            justify-content: space-between;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #eee;
        }

        .btn {
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1em;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
        }

        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }

        .btn-secondary {
            background: #6c757d;
            color: white;
        }

        .btn-secondary:hover {
            background: #5a6268;
            transform: translateY(-2px);
        }

        .btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        /* Scrollbar Styling */
        ::-webkit-scrollbar {
            width: 10px;
        }

        ::-webkit-scrollbar-track {
            background: #f1f1f1;
        }

        ::-webkit-scrollbar-thumb {
            background: #667eea;
            border-radius: 5px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #764ba2;
        }

        /* Progress indicator */
        .progress-bar {
            position: fixed;
            top: 0;
            left: 300px;
            right: 0;
            height: 4px;
            background: #e0e0e0;
            z-index: 1000;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            width: 0%;
            transition: width 0.3s ease;
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .container {
                flex-direction: column;
            }

            .sidebar {
                width: 100%;
                height: auto;
                max-height: 200px;
            }

            .content-section {
                padding: 20px;
            }

            .nav-buttons {
                flex-direction: column;
                gap: 10px;
            }

            .progress-bar {
                left: 0;
            }
        }

        /* Links */
        a {
            color: #667eea;
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }

        /* Strong/Bold */
        strong {
            color: #764ba2;
            font-weight: 600;
        }

        /* Emphasis/Italic */
        em {
            font-style: italic;
            color: #555;
        }
    </style>
</head>
<body>
    <div class="progress-bar">
        <div class="progress-fill" id="progressFill"></div>
    </div>

    <div class="container">
        <!-- Sidebar Navigation -->
        <nav class="sidebar">
            <div class="sidebar-header">
                <h1>CPSC 444</h1>
                <p>Spatial Statistics & Data Science</p>
            </div>
            <ul class="nav-menu">
'''

HTML_TEMPLATE_FOOT = '''
            </ul>
        </nav>

        <!-- Main Content Area -->
        <main class="main-content">
'''

HTML_TEMPLATE_END = '''
        </main>
    </div>

    <script>
        let currentSection = 'home';
        const sections = [''' + ', '.join([f"'{mid}'" for mid, _, _ in MODULES]) + '''];

        function showSection(sectionId) {
            // Hide all sections
            document.querySelectorAll('.content-section').forEach(section => {
                section.classList.remove('active');
            });

            // Show selected section
            const targetSection = document.getElementById(sectionId);
            if (targetSection) {
                targetSection.classList.add('active');
            }

            // Update navigation active state
            document.querySelectorAll('.nav-link').forEach(link => {
                link.classList.remove('active');
            });

            const clickedLink = event && event.target;
            if (clickedLink && clickedLink.classList.contains('nav-link')) {
                clickedLink.classList.add('active');
            }

            // Scroll to top
            document.querySelector('.main-content').scrollTop = 0;

            // Update progress bar
            const sectionIndex = sections.indexOf(sectionId);
            const progress = (sectionIndex / (sections.length - 1)) * 100;
            document.getElementById('progressFill').style.width = progress + '%';

            currentSection = sectionId;
        }

        // Keyboard navigation
        document.addEventListener('keydown', function(e) {
            const currentIndex = sections.indexOf(currentSection);

            if (e.key === 'ArrowRight' && currentIndex < sections.length - 1) {
                const nextSection = sections[currentIndex + 1];
                showSection(nextSection);
                updateNavActiveState(nextSection);
            } else if (e.key === 'ArrowLeft' && currentIndex > 0) {
                const prevSection = sections[currentIndex - 1];
                showSection(prevSection);
                updateNavActiveState(prevSection);
            }
        });

        function updateNavActiveState(sectionId) {
            document.querySelectorAll('.nav-link').forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('onclick').includes(sectionId)) {
                    link.classList.add('active');
                }
            });
        }

        console.log('CPSC 444 Study Guide loaded successfully!');
        console.log('Use arrow keys (← →) to navigate between sections');
        console.log('Total modules: ' + sections.length);
    </script>
</body>
</html>'''

def main():
    """Generate the complete HTML file"""
    print("Generating comprehensive HTML study guide...")

    # Build the HTML
    html_parts = [
        HTML_TEMPLATE_HEAD,
        generate_nav_items(),
        HTML_TEMPLATE_FOOT,
        generate_content_sections(),
        HTML_TEMPLATE_END
    ]

    full_html = ''.join(html_parts)

    # Write to file
    output_path = os.path.join(BASE_PATH, 'CPSC444_Complete_Study_Guide.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_html)

    file_size = len(full_html)
    print(f"\n✓ Successfully generated: {output_path}")
    print(f"✓ File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
    print(f"✓ Total sections: {len(MODULES)}")
    print(f"\nYou can now open this file in any web browser!")

if __name__ == '__main__':
    main()
