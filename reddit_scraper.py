import praw

def fetch_reddit_data(username):
    """
    Fetch latest comments and posts from a Reddit user.

    Args:
        username (str): Reddit username without 'u/' prefix.

    Returns:
        dict: Dictionary with keys 'comments' and 'posts'.
    """
    reddit = praw.Reddit(
        client_id="nmSGmXDGhBUEbweJB5x94A",
        client_secret="rzfNuNHKB0zYIdwpdge9ab7s4LK5fQ",
        user_agent="user_persona by u/aj_vish"
    )

    redditor = reddit.redditor(username)
    data = {"comments": [], "posts": []}

    # Fetch latest 100 comments
    for comment in redditor.comments.new(limit=100):
        data["comments"].append({
            "body": comment.body,
            "subreddit": str(comment.subreddit),
            "permalink": f"https://www.reddit.com{comment.permalink}"
        })

    # Fetch latest 50 posts
    for post in redditor.submissions.new(limit=50):
        data["posts"].append({
            "title": post.title,
            "selftext": post.selftext,
            "subreddit": str(post.subreddit),
            "url": f"https://www.reddit.com{post.permalink}"
        })

    return data
