import json
import requests

    

class PostCollection:
    def __init__(self):
        self.posts = []
    
    def get_posts(self, tags: list):
        url = 'https://api.hatchways.io/assessment/blog/posts?tag={}'
        id_set = {}
        for tag in tags:
            r = requests.get(url.format(tag)).json()
            result = r['posts']
            #Remove duplicate posts
            for post in result:
                key = (post['authorId'], post['id'])
                if key not in id_set.keys():
                    id_set[key] = post
        self.posts = list(id_set.values())


    def sort(self, sortBy, direction):
        if sortBy == 'id' and direction == 'asc':
            pass
        if self.posts:
            self.posts.sort(key=lambda k: k[sortBy], reverse=True if direction == 'desc' else False)

if __name__ == '__main__':
    p = PostCollection()
    p.get_posts(tags=['tech'])
    p.sort('reads', 'desc')
    print(p.posts)