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

with open(PATH_TO_BLOG/'index.html','w') as f:
	f.write("This is my blog, follow for more...")

update_blog()
