from flask import Flask, render_template
import requests
import os
import dotenv

dotenv.load_dotenv('.env')

username = os.environ.get('USERNAME')
token = os.environ.get('TOKEN')

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_projects():
    try:
        url = "https://api.github.com/users/waPAO/repos"
        headers = {"Accept":"application/vnd.github.mercy-preview+json"}
        repos = requests.get(url, headers=headers, auth=(username,token)).json()
        projects = []
        for repo in repos:
            if repo["homepage"]:
                project = {
                    "id": repo["id"],
                    "name": repo["name"],
                    "url": repo["html_url"],
                    "description": repo["description"],
                    "topics":repo["topics"],
                    "links": repo["homepage"].split(";")
                }
                projects.append(project)
        return render_template('index.html', projects=projects)
    except Exception as e:
        return {"error": True, "message": str(e)}, 500
    

if __name__ == "__main__":
    app.run(debug=True)