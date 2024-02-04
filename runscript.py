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


def create_comment(issue_author_avatar,issue_name,issue_body):
    createcontent=f"""
                    <pre>
                <div style="display: flex; align-items: center; justify-content: space-between;">
                <img src={issue_author_avatar} width="40" style="margin-right: 10px;"> 
                <p style="margin: 0;">{issue_name}</p>
                <p style="margin: 0;">{issue_body}</p>
                </div>
                </pre>
            """
    return createcontent


with open('Readme.md', 'r') as file:
    readme_content = file.read()
        
start_index = readme_content.find("#### Top users who merges their thoughts.")
end_index = readme_content.find("THANK YOU")

generate_comment=create_comment()

updated_readme_content = readme_content[:start_index] + generate_comment + readme_content[end_index:]


with open('Readme.md', 'a') as file:
    file.write(updated_readme_content)