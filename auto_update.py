import os
import openai
from dotenv import load_dotenv
from git import Repo
from pathlib import Path


load_dotenv()
openai.api_key = os.getenv('MyKey')

filepath = 'C:\\Users\\alexg\\OneDrive\\Documents\\GitHub\\justalexok.github.io\\.git'

PATH_TO_BLOG_REPO  = Path(filepath)

PATH_TO_BLOG = PATH_TO_BLOG_REPO.parent

PATH_TO_CONTENT = PATH_TO_BLOG/"content"

PATH_TO_CONTENT.mkdir(exist_ok=True, parents=True)

def update_blog(commit_message='Updates blog'):

	repo = Repo(PATH_TO_BLOG_REPO)
	repo.git.add(all=True)
	repo.index.commit(commit_message)
	origin = repo.remote(name='origin')
	origin.push()

with open(PATH_TO_BLOG/'index.html','w+') as f:
	f.write(f"Follow this page!")

def create_new_blog(title,content,cover_image):

	cover_image = Path(cover_image)

	files = len(list(PATH_TO_CONTENT.glob("*.html")))
	new_title = f"{files+1}.html"
	path_to_new_content = PATH_TO_CONTENT/new_title

	shutil.copy(cover_image,path_to_new_content)
	if not os.path.exists(path_to_new_content):
		with open(path_to_new_content,"w") as f:
			f.write("<!DOCTYPE html>\n")
			f.write("<html>\n")
			f.write("<head>\n")
			f.write(f"<title> {title} </title>\n")
			f.write("</head>\n")

			f.write("<body>\n")
			f.write(f"<img src='{cover_image.name}' alt='Cover Image'> <br />\n")
			f.write(f"<h1> {title} </h1>")
			f.write(content.replace("\n", "<br />\n"))
			f.write("</body>\n")
			f.write("</html>\n")
			print("Blog created")
			return path_to_new_content
	else:
		raise FileExistsError("File already exist! Abort")

update_blog()