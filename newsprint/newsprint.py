import feedparser
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from bs4 import BeautifulSoup
import re
import textwrap

# Load the Jinja2 template
env = Environment(loader=FileSystemLoader("."))
template = env.get_template("newspaper_template.j2")

# List of RSS feed URLs
feed_urls = [
    "http://feeds.bbci.co.uk/news/rss.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
    "https://www.theguardian.com/us/rss",
    "https://feeds.feedburner.com/TechCrunch/",
    "https://www.reddit.com/r/news/.rss"
]

# Prepare articles data
total_articles = 10  # Total articles to display
max_summary_length = 400  # Maximum characters in the summary
max_lines = 5  # Maximum lines for the summary
articles_per_feed = total_articles // len(feed_urls)  # Articles to fetch from each feed

articles = []

def clean_html(content):
    """Remove HTML tags from the given content using BeautifulSoup."""
    soup = BeautifulSoup(content, "html.parser")
    return soup.get_text()

def clean_reddit_submission(submission_text):
    """Remove '[link] [comments]' part from the Reddit submission text."""
    return re.sub(r'\s+\[link\]\s+\[comments\]', '', submission_text).strip()

def wrap_summary(text, max_length, max_lines):
    """Wrap text to specified maximum length and maximum lines, adding ellipsis if truncated."""
    wrapped = textwrap.fill(text, width=80)  # Wrap at 80 characters
    lines = wrapped.splitlines()  # Split into lines

    if len(lines) > max_lines:
        wrapped_text = "\n".join(lines[:max_lines]) + "..."  # Add ellipsis if truncated
    else:
        wrapped_text = "\n".join(lines)  # No truncation, return full wrapped text

    return wrapped_text

for feed_url in feed_urls:
    # Parse the RSS feed
    feed = feedparser.parse(feed_url)

    # Get the number of articles to fetch from this feed
    num_articles = min(articles_per_feed, len(feed.entries))  # Don't exceed available entries

    for entry in feed.entries[:num_articles]:
        # Check for summary or description
        summary = entry.summary if 'summary' in entry else entry.description if 'description' in entry else "No summary available."
        
        # Clean HTML tags
        summary = clean_html(summary)

        # If the entry is from Reddit, clean the submission text further
        if 'reddit.com' in entry.link:
            summary = clean_reddit_submission(summary)
        
        # Wrap the summary to a maximum length and lines
        wrapped_summary = wrap_summary(summary, max_summary_length, max_lines)

        articles.append({
            "headline": entry.title,
            "summary": wrapped_summary,
            "url": entry.link
        })

# Check if we need more articles in case total is less than expected
if len(articles) < total_articles:
    for feed_url in feed_urls:
        if len(articles) >= total_articles:
            break
        # Fetch additional articles if we still need more
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[len(articles):]:
            # Check for summary or description
            summary = entry.summary if 'summary' in entry else entry.description if 'description' in entry else "No summary available."
            
            # Clean HTML tags
            summary = clean_html(summary)

            # If the entry is from Reddit, clean the submission text further
            if 'reddit.com' in entry.link:
                summary = clean_reddit_submission(summary)

            # Wrap the summary to a maximum length and lines
            wrapped_summary = wrap_summary(summary, max_summary_length, max_lines)

            articles.append({
                "headline": entry.title,
                "summary": wrapped_summary,
                "url": entry.link
            })
            if len(articles) >= total_articles:
                break

# Prepare data for rendering
data = {
    "newspaper_name": "Combined News Sources",
    "date": datetime.now().strftime("%Y-%m-%d"),
    "articles": articles[:total_articles]  # Ensure we only take the first 10 articles
}

# Render the template with the data
output = template.render(data)

# Check total length and adjust if necessary
max_page_length = 3000  # Maximum character length for A4 page

if len(output) > max_page_length:
    print("Warning: Output exceeds maximum A4 page length.")
    # You may want to truncate or adjust the articles further here

# Save the rendered text to a file
with open("newspaper_page.txt", "w") as f:
    f.write(output)

print(output)
