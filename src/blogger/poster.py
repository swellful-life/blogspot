import requests

class BloggerPoster:
    def __init__(self, client_id, client_secret, refresh_token, blog_id):
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.blog_id = blog_id

    def get_access_token(self):
        response = requests.post(
            "https://oauth2.googleapis.com/token",
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": self.refresh_token,
                "grant_type": "refresh_token",
            },
        )

        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            raise Exception(f"Failed to get access token: {response.json()}")


    def post_to_blogger(self, title, content):
        post_data = {
            "kind": "blogger#post",
            "title": title,
            "content": content,
        }
        url = f"https://www.googleapis.com/blogger/v3/blogs/{self.blog_id}/posts/"
        headers = {
            "Authorization": f"Bearer {self.get_access_token()}",
            "Content-Type": "application/json",
        }

        response = requests.post(url, json=post_data, headers=headers)
        if response.status_code == 200:
            print("Post successfully published to Blogger:", response.json())
        else:
            raise Exception(f"Error posting to Blogger: {response.json()}")
