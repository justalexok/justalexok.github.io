import os
import openai
from dotenv import load_dotenv
from git import Repo
from pathlib import Path
import shutil
import requests
from bs4 import BeautifulSoup as Soup
from PIL import Image

load_dotenv()
openai.api_key = os.getenv('MyKey')

filepath = 'C:\\Users\\alexg\\OneDrive\\Documents\\GitHub\\justalexok.github.io\\.git'

PATH_TO_BLOG_REPO  = Path(filepath)

PATH_TO_BLOG = PATH_TO_BLOG_REPO.parent

PATH_TO_CONTENT = PATH_TO_BLOG/"content"

#PATH_TO_CONTENT.mkdir(exist_ok=True, parents=True)

def update_blog(commit_message='Updates blog'):

	repo = Repo(PATH_TO_BLOG_REPO)
	repo.git.add(all=True)
	repo.index.commit(commit_message)
	origin = repo.remote(name='origin')
	origin.push()

# with open(PATH_TO_BLOG/'index.html','w+') as f:
# 	f.write(f"Follow this page!")

def create_new_blog(title,content):


	files = len(list(PATH_TO_CONTENT.glob("*.html")))
	new_title = f"{files+1}.html"
	path_to_new_content = PATH_TO_CONTENT/new_title

	shutil.copy(PATH_TO_CONTENT, path_to_new_content)
	if not os.path.exists(path_to_new_content):
		with open(path_to_new_content,"w") as f:
			f.write("<!DOCTYPE html>\n")
			f.write("<html>\n")
			f.write("<head>\n")
			f.write(f"<title> {title} </title>\n")
			f.write("</head>\n")
			f.write("<body>\n")
			f.write(f"<h1> {title} </h1>")
			f.write(content.replace("\n", "<br />\n"))
			f.write("</body>\n")
			f.write("</html>\n")
			print("Blog created")
			return path_to_new_content
	else:
		raise FileExistsError("File already exist! Abort")


def check_for_duplicate_links(path_to_new_content, links):
	urls = [str(link.get('href')) for link in links]
	content_path = str(Path(*path_to_new_content.parts[-2:])) #final two parts of the path
	#'content\1.html' for eg
	return content_path in urls

def write_to_index(path_to_new_content):



	with open(PATH_TO_BLOG/"index.html") as index:
		soup = Soup(index.read(), 'html.parser')

	links = soup.find_all("a")
	
	last_link = links[-1]

	if check_for_duplicate_links(path_to_new_content,links):
		raise ValueError("Link already exists")

	link_to_new_blog = soup.new_tag("a", href=Path(*path_to_new_content.parts[-2:])) #content/1.html
	link_to_new_blog.string = PATH_TO_CONTENT.name.split(".")[0]
	last_link.insert_after(link_to_new_blog)

	# for link in links:
	# 	link.extract()

	with open(PATH_TO_BLOG/"index.html","w") as f:
		f.write(str(soup.prettify(formatter='html')))



blog_title = 'Privacy Report'

blog_content = "Testing 123"

path_to_new_content = create_new_blog(blog_title,blog_content)

write_to_index(path_to_new_content)

update_blog()
