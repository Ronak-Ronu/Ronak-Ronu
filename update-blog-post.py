import os
import requests

BLOG_API_URL = os.getenv('BLOG_API_URL', '')

def create_blog_post_card(post):
    title = post.get("title", "No Title")
    body_raw = post.get("bodyofcontent", "No content available")
    body = body_raw[:200] + "..." if len(body_raw) > 200 else body_raw
    link = f"https://berony.web.app/read/{post.get('_id', '')}"
    image_url = post.get("imageUrl", "")
    created_at = post.get("createdAt", "Unknown date")

    card = f"""
<table style="border: 1px solid #ddd; border-radius: 8px; padding: 10px; margin: 10px 0; max-width: 500px; border-collapse: collapse;">
  <tr>
    <td style="vertical-align: top; padding: 5px;">
      <img src="{image_url}" width="50" style="margin-right: 10px;">
    </td>
    <td style="vertical-align: top; padding: 5px;">
<strong style="font-size: 14px; color: #333;">{title}</strong><br>
<small style="color: #666; font-size: 12px;">Posted on: {created_at[:10]}</small><br>
<p style="font-size: 14px; color: #444; margin: 8px 0; line-height: 1.5;">{body}</p>
<a href="{link}" target="_blank" style="color: #1a73e8; text-decoration: none; font-size: 14px;">Read More</a>    </td>
  </tr>
  <tr>
    <td colspan="2" style="padding: 5px;">
      <small style="color: #1a73e8;">#TechNotifications #RealTimeAlerts #BRRRmeme</small>
    </td>
  </tr>
</table>
"""
    return card

def fetch_recent_posts(api_url, count=1):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        posts = response.json()

        posts.sort(key=lambda x: x.get("createdAt", ""), reverse=True)
        return posts[:count]

    except requests.exceptions.RequestException as e:
        print(f"Error fetching posts: {e}")
        return []

with open('Readme.md', 'r') as file:
    readme_content = file.read()

recent_posts = fetch_recent_posts(BLOG_API_URL, count=1)
blog_post_card = create_blog_post_card(recent_posts[0]) if recent_posts else "No new blog posts available."

start_index = readme_content.find("#### Recent Blog Posts From Berony")
end_index = readme_content.find("#### Top users who merges their thoughts.")

if start_index != -1 and end_index != -1:
    new_content = (
        readme_content[:start_index] +
        '#### Recent Blog Posts From Berony <a href="https://berony.web.app" target="_blank">[Visit Berony]</a>\n' +
        blog_post_card + "\n\n" +
        readme_content[end_index:]
    )
else:
    insert_at = readme_content.find("#### Top users who merges their thoughts.")
    if insert_at != -1:
        new_content = (
            readme_content[:insert_at] +
            '#### Recent Blog Posts From Berony <a href="https://berony.web.app" target="_blank">[Visit Berony]</a>\n' +
            blog_post_card + "\n\n" +
            readme_content[insert_at:]
        )
    else:
        new_content = (
            readme_content + "\n" +
            '#### Recent Blog Posts From Berony <a href="https://berony.web.app" target="_blank">[Visit Berony]</a>\n' +
            blog_post_card + "\n"
        )

# Write the updated content back to the README
with open('Readme.md', 'w') as file:
    file.write(new_content)