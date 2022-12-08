import os
from flask import Flask, request, jsonify
import requests as req

app = Flask(__name__)
COMMENTS_ENDPOINT = "https://jsonplaceholder.typicode.com/comments"
POSTS_ENDPOINT= "https://jsonplaceholder.typicode.com/posts"

def post_translator(post: dict) -> dict: # To get the desired
    """ Gets the desired attribute name for each post """
    translated_post                             = {}
    translated_post["post_id"]                  = post["id"]
    translated_post["post_title"]               = post["title"]
    translated_post["post_body"]                = post["body"]
    translated_post["total_number_of_comments"] = 0
    return translated_post

@app.route('/topPosts')
def get_top_posts() -> str:
    """ Gets top posts by comment count
        Usage: /topPosts
    """
    comments    = req.get(COMMENTS_ENDPOINT , timeout=10).json()
    posts       = req.get(POSTS_ENDPOINT    , timeout=10).json()
    resp_list   = []

    for post in posts:
        translated_post = post_translator(post)
        for comment in comments[:]:
            if comment["postId"] == post["id"] :
                translated_post["total_number_of_comments"] += 1
                comments.remove(comment)    # For better performance with a large number of comments
        resp_list.append(translated_post)

    resp_list.sort(key=lambda x: x["total_number_of_comments"])
    return jsonify(resp_list)

@app.route('/search')
def search() -> str:
    """ Gets comments by filter
        Usage: /search?filterName=<Attribute>&filterValue=<Value>
        where filterName can be postId, id, name, email, body
        and filterValue can be any string
        examples:
        /search?filterName=name&filterValue=id%20labore%20ex%20et%20quam%20laborum
        /search?filterName=postId&filterValue=3
        /search?filterName=email&filterValue=Nikita@garfield.biz
    """
    comments    = req.get(COMMENTS_ENDPOINT, timeout=10).json()
    filter_name  = request.args.get('filterName', default = "postId", type = str)
    filter_value = request.args.get('filterValue', default = "1", type = str)
    output_dict = [x for x in comments if str(x[filter_name]) == filter_value]
    return jsonify(output_dict)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
