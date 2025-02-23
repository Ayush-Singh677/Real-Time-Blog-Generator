import os
import shutil
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, HTTPServer
import webbrowser

def get_user_input():
    print("Welcome to the Blog Generator!")
    title = "Hello"
    category = "General"
    content = "This is a sample blog post. Replace this with your content."
    return title, category, content

def inject_content_into_html(template_path, title, category, content):
    current_date = datetime.now().strftime("%B %d, %Y")
    with open(template_path, "r", encoding="utf-8") as file:
        html_template = file.read()

    html_content = html_template.format(
        title=title,
        category=category,
        date=current_date,
        content=content
    )
    return html_content

def create_temp_files(html_content, template_dir, temp_dir):
    os.makedirs(temp_dir, exist_ok=True)

    with open(os.path.join(temp_dir, "index.html"), "w", encoding="utf-8") as html_file:
        html_file.write(html_content)

    css_path = os.path.join(template_dir, "styles.css")
    if os.path.exists(css_path):
        shutil.copy(css_path, os.path.join(temp_dir, "styles.css"))
    else:
        print("Warning: styles.css not found. Skipping CSS file.")

    js_path = os.path.join(template_dir, "script.js")
    if os.path.exists(js_path):
        shutil.copy(js_path, os.path.join(temp_dir, "script.js"))
    else:
        print("Warning: script.js not found. Skipping JS file.")

    image_path = "sample.png"
    if os.path.exists(image_path):
        shutil.copy(image_path, os.path.join(temp_dir, "sample.png"))
    else:
        print(f"Warning: Image file '{image_path}' not found. The image will not be displayed.")

    return temp_dir

def preview_webpage(temp_dir):
    os.chdir(temp_dir)
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"Preview your blog at http://localhost:8000")
    webbrowser.open("http://localhost:8000")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()

# def deploy_webpage(temp_dir):
#     print("Deploying the webpage...")
#     repo_name = input("Enter the GitHub repository name: ")
#     os.system(f"cd {temp_dir} && git init && git add . && git commit -m 'Deploy Blog'")
#     os.system(f"cd {temp_dir} && git branch -M main && git remote add origin https://github.com/yourusername/{repo_name}.git")
#     os.system(f"cd {temp_dir} && git push -u origin main")
#     print(f"Webpage deployed to https://{repo_name}.github.io")

def main():
    template_dir = "templates"
    html_template_path = os.path.join(template_dir, "index.html")
    if not os.path.exists(html_template_path):
        print(f"Error: HTML template file '{html_template_path}' not found.")
        return
    title, category, content = get_user_input()
    html_content = inject_content_into_html(html_template_path, title, category, content)
    temp_dir = "temp_blog"
    temp_dir = create_temp_files(html_content, template_dir, temp_dir)

    preview_webpage(temp_dir)
    deploy_choice = input("Do you want to deploy the webpage? (yes/no): ").lower()
    if deploy_choice == "no":
        pass
        # deploy_webpage(temp_dir)
    else:
        print("Webpage not deployed. Temporary files are saved in:", temp_dir)

if __name__ == "__main__":
    main()