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

	# cover_image = Path(cover_image)

	files = len(list(PATH_TO_CONTENT.glob("*.html")))
	# new_title = f"{files+1}.html"
	new_title = "ai-puzzle-privacy-report.html"
	path_to_new_content = PATH_TO_CONTENT/new_title

	# shutil.copy(cover_image,PATH_TO_CONTENT)
	if not os.path.exists(path_to_new_content):
		with open(path_to_new_content,"w") as f:
			f.write("<!DOCTYPE html>\n")
			f.write("<html>\n")
			f.write("<head>\n")
			f.write(f"<title> {title} </title>\n")
			f.write("</head>\n")
			f.write("<body>\n")
			# f.write(f"<img src='{cover_image.name}' alt='Cover Image'> <br />\n")
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



# def get_dalle_prompt(title):
# 	prompt = f"Cartoon of '{title}'"
# 	print(f'Dalle Prompt: {prompt}')
# 	return prompt

# def get_img_response(img_title):

# 	response = openai.Image.create(
# 		prompt = get_dalle_prompt(title = img_title),
# 									n=1,
# 									size='1024x1024'
# 	)
# 	return response

# def save_image(img_url, file_name):

# 	image_res = requests.get(img_url, stream = True)

# 	if image_res.status_code == 200:
# 		with open(file_name,'wb') as f:
# 			shutil.copyfileobj(image_res.raw,f)
# 	else:
# 		print('Error downloading image')
# 	return image_res.status_code




privacy_content = """
App Information:
App Name: AI Puzzle
App Store Connect ID: 6450428401
App Version: 1.0
Developer Name: Alex Goulder
Developer Contact Information: alex.goulder@outlook.com
Data Collection and Use:
AI Puzzle does not collect any personal information, user data, or any other identifiable information from its users. The app is designed to be privacy-focused, particularly when catering to children. We have taken great care to ensure that no sensitive data is collected, stored, or transmitted from within the app.

Third-Party Services:
AI Puzzle does not integrate or use any third-party services, such as analytics tools, advertising networks, or social media platforms that may collect user data. The app solely operates within its own standalone environment, providing a safe and secure experience for children.

Advertising and Tracking:
AI Puzzle does not include any advertising features or tracking mechanisms. We understand the importance of protecting children's privacy and have deliberately excluded any form of advertising, remarketing, or user tracking technologies within the app.

Account Creation and Login:
AI Puzzle does not require users to create an account or log in to access its features. Users can simply download and install the app from the App Store to start using it immediately, without providing any personal information.

Data Encryption and Security:
AI Puzzle incorporates industry-standard encryption and security measures to protect the integrity and confidentiality of user data. Despite not collecting any user data, we have implemented these measures to ensure the overall security of the app and its users."
"""

blog_title = 'Privacy Report'
# img_title = 'Cartoon Dog wearing a hat'

blog_content = privacy_content

# img_url = get_img_response(img_title)['data'][0]['url']
# print(img_url)

# save_image(img_url,'blog_image.png')

path_to_new_content = create_new_blog(blog_title,blog_content)

write_to_index(path_to_new_content)

update_blog()
