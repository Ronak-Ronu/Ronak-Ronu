import os
import json
import requests

BLOG_API_URL = os.getenv('BLOG_API_URL', '')  
def create_blog_post_card(post):
    title = post.get("title", "No Title")
    body = post.get("bodyofcontent", "No content available")[:100] + "..." if len(post.get("bodyofcontent", "")) > 100 else post.get("bodyofcontent", "No content available")
    link = post.get("link", "#") or "#"
    image_url = post.get("imageUrl", "")
    created_at = post.get("createdAt", "Unknown date")

    card = f"""<pre>
        <div style="border: 1px solid #ddd; border-radius: 8px; padding: 10px; margin: 10px 0; max-width: 500px;">
            <img src="{image_url}" width="50" style="float: left; margin-right: 10px;">
            <h4 style="margin: 0; font-size: 16px;">{title}</h4>
            <p style="font-size: 12px; color: #555;">Posted on: {created_at[:10]}</p>
            <p style="font-size: 14px;">{body}</p>
            <a href="{link}" target="_blank" style="text-decoration: none; color: #1a73e8;">Read More</a>
        </div>
        </pre>"""
    return card

def fetch_recent_posts(api_url, count=1):
    try:
        response = requests.get(api_url, params={"per_page": count})
        response.raise_for_status()
        posts = response.json()
        formatted_posts = []
        for post in posts:
            formatted_post = {
                "title": post.get("title", {}).get("rendered", post.get("title", "No Title")),
                "bodyofcontent": post.get("content", {}).get("rendered", post.get("bodyofcontent", "No content")),
                "link": post.get("link", "#"),
                "imageUrl": post.get("imageUrl", ""),
                "createdAt": post.get("date", post.get("createdAt", "Unknown date"))
            }
            formatted_posts.append(formatted_post)
        return formatted_posts
    except requests.exceptions.RequestException as e:
        print(f"Error fetching posts: {e}")
        return []

with open('Readme.md', 'r') as file:
    readme_content = file.read()

recent_posts = fetch_recent_posts(BLOG_API_URL, count=1)
blog_post_card = create_blog_post_card(recent_posts[0]) if recent_posts else "<pre>No new blog posts available.</pre>"

start_index = readme_content.find("#### Recent Blog Posts")
end_index = readme_content.find("#### Top users who merges their thoughts.")

if start_index != -1 and end_index != -1:
    existing_blog_content = readme_content[start_index:end_index]
    new_blog_content = "#### Recent Blog Posts\n" + blog_post_card + "\n" + existing_blog_content[existing_blog_content.find("\n") + 1:]
    new_content = readme_content[:start_index] + new_blog_content + readme_content[end_index:]
else:
    start_index_comments = readme_content.find("#### Top users who merges their thoughts.")
    if start_index_comments != -1:
        new_content = (
            readme_content[:start_index_comments]
            + "#### Recent Blog Posts\n"
            + blog_post_card
            + "\n\n"
            + readme_content[start_index_comments:]
        )
    else:
        print("Comments section not found. Appending blog section at the end.")
        new_content = readme_content + "\n#### Recent Blog Posts\n" + blog_post_card + "\n"

with open('Readme.md', 'w') as file:
    file.write(new_content)