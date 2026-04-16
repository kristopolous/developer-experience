import click
import httpx
import re
import html
from datetime import datetime
from typing import List, Optional

BASE_URL = "https://hacker-news.firebaseio.com/v0"
VERSION = "1.0.0"

class HNClient:
    def __init__(self):
        self.client = httpx.Client()

    def get_stories(self, story_type: str = "top", limit: int = 10) -> List[dict]:
        url = f"{BASE_URL}/{story_type}stories.json"
        response = self.client.get(url)
        response.raise_for_status()
        story_ids = response.json()[:limit]
        
        stories = []
        for story_id in story_ids:
            stories.append(self.get_item(story_id))
        return stories

    def get_item(self, item_id: int) -> dict:
        url = f"{BASE_URL}/item/{item_id}.json"
        response = self.client.get(url)
        response.raise_for_status()
        return response.json()

    def get_comments(self, story_id: int, limit: int = 10) -> List[dict]:
        story = self.get_item(story_id)
        comment_ids = story.get("kids", [])[:limit]
        comments = []
        for comment_id in comment_ids:
            comments.append(self.get_item(comment_id))
        return comments

hn = HNClient()

@click.group()
@click.version_option(VERSION)
def cli():
    """ HackerNews CLI - for hackers """
    pass

@cli.command()
@click.option('--sort_by', '-s', default='top',
              type=click.Choice(['top', 'new', 'best']), help='sort type')
@click.option('--limit', '-l', default=10, type=click.INT,
              help='number of top stories to show')
def stories(sort_by: str, limit: int):
    """ list stories """
    try:
        results = hn.get_stories(story_type=sort_by, limit=limit)

        if results:
            click.echo(click.style('      when      | comments |   id    | title', fg='yellow'))
        else:
            click.echo(click.style('no stories found!', fg='red'))

        for story in results:
            if not story:
                continue
            
            time_str = datetime.fromtimestamp(story.get('time', 0)).strftime('%Y-%m-%d %H:%M')
            comments_count = story.get('descendants', 0)
            story_id = story.get('id', '')
            title = story.get('title', 'No Title')

            click.echo(click.style(time_str.center(15), fg='magenta') + ' | ', nl=False)
            click.echo(click.style(str(comments_count).center(8), fg='red') + ' | ', nl=False)
            click.echo(click.style(str(story_id), fg='green') + ' | ', nl=False)
            click.echo(click.style(title, fg='white'))
    except Exception as e:
        click.echo(click.style(f"Error: {e}", fg='red'), err=True)

@cli.command()
@click.argument('story_id', type=click.INT, required=True)
def go(story_id: int):
    """ go to the story on HackerNews """
    try:
        story = hn.get_item(story_id)
        url = story.get('url') or f"https://news.ycombinator.com/item?id={story_id}"
        click.launch(url)
    except Exception as e:
        click.echo(click.style(f"Error: {e}", fg='red'), err=True)

@cli.command()
@click.argument('story_id', type=click.INT, required=True)
@click.option('--limit', '-l', default=10, type=click.INT, help='number of comments to show')
def comments(story_id: int, limit: int):
    """ show comments for the story """
    try:
        results = hn.get_comments(story_id, limit=limit)

        if not results:
            click.echo(click.style('no comments for story found!', fg='red'))

        for comment in results:
            if not comment:
                continue
            
            time_str = datetime.fromtimestamp(comment.get('time', 0)).strftime('%Y-%m-%d %H:%M')
            user = comment.get('by', 'unknown')
            body = comment.get('text', '')
            
            # Remove HTML tags and unescape entities
            body = html.unescape(re.sub('<[^<]+?>', '', body))


            click.echo(click.style(time_str.center(15), fg='magenta'), nl=False)
            click.echo('by ' + click.style(str(user), fg='cyan'))
            click.echo(body)
            click.echo("-" * 20)
    except Exception as e:
        click.echo(click.style(f"Error: {e}", fg='red'), err=True)

@cli.command()
@click.argument('story_id', type=click.INT, required=True)
def comment(story_id: int):
    """ comment story on HackerNews """
    url = f"https://news.ycombinator.com/item?id={story_id}"
    click.launch(url)

if __name__ == '__main__':
    cli()
