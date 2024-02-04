import os
import json


event_path = os.getenv('GITHUB_EVENT_PATH')


if not event_path:
    print("GitHub event data not found.")
    exit(1)


with open(event_path, 'r') as file:
    event_data = json.load(file)


issue_author = event_data['issue']['user']['login']
issue_title =event_data['issue']['title']
issue_author_avatar = event_data['issue']['user']['avatar_url']
issue_body= event_data['issue']['body']


def create_comment(issue_author_avatar,issue_title,issue_body):
    createcontent=f"<pre><img src={issue_author_avatar} width=\"30\">{issue_title}<br/>{issue_body}</pre>"
    return createcontent


with open('Readme.md', 'r') as file:
    readme_content = file.read()
        

generate_comment=create_comment(issue_author_avatar,issue_title,issue_body)
start_index = readme_content.find("#### Top users who merges their thoughts.")
end_index = readme_content.find("THANK YOU")
updated_readme_content = readme_content[:start_index] + generate_comment + readme_content[end_index:]

with open('Readme.md', 'a') as file:
    file.write(updated_readme_content)