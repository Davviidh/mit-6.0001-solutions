# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import threading
from pathlib import Path
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def _parse_pubdate(pubdate):
    """Return an aware datetime for an RSS or Atom publication timestamp."""
    try:
        parsed = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
        return parsed.replace(tzinfo=pytz.timezone("GMT"))
    except ValueError:
        pass

    try:
        return datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")
    except ValueError:
        pass

    # Atom feeds use ISO 8601/RFC 3339 timestamps. ``fromisoformat`` does not
    # understand a trailing Z on older Python 3 releases, so normalize it.
    iso_pubdate = pubdate[:-1] + "+00:00" if pubdate.endswith("Z") else pubdate
    parsed = datetime.fromisoformat(iso_pubdate)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=pytz.utc)
    return parsed


def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        pubdate = _parse_pubdate(pubdate)

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1
class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
        
    def get_guid(self):
        return self.guid
        
    def get_title(self):
        return self.title
        
    def get_description(self):
        return self.description
        
    def get_link(self):
        return self.link
        
    def get_pubdate(self):
        return self.pubdate
    
    
#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase.lower()
        
    def is_phrase_in(self, text):
        text = text.lower()
        cleaned_text = ''
        for i in text:
            if i in string.punctuation:
                cleaned_text += ' '
            else:
                cleaned_text += i
        text_list = cleaned_text.split()
        phrase_words = self.phrase.split()
        phrase_len = len(phrase_words)
        for i in range(len(text_list) - phrase_len + 1):
            if text_list[i:i+phrase_len] == phrase_words:
                return True
        return False
    

# Problem 3
class TitleTrigger(PhraseTrigger):
    def evaluate(self, story):
        return self.is_phrase_in(story.get_title())

# Problem 4
class DescriptionTrigger(PhraseTrigger):
    def evaluate(self, story):
        return self.is_phrase_in(story.get_description())

# TIME TRIGGERS

# Problem 5
class TimeTrigger(Trigger):
    def __init__(self, time_str):
        naive_datetime = datetime.strptime(time_str, "%d %b %Y %H:%M:%S")
        self.time = pytz.timezone("EST").localize(naive_datetime)

# Problem 6
class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
        pubdate = story.get_pubdate()
        if pubdate.tzinfo is None:
            pubdate = pytz.timezone("EST").localize(pubdate)
        else:
            pubdate = pubdate.astimezone(pytz.timezone("EST"))
        return pubdate < self.time

class AfterTrigger(TimeTrigger):
    def evaluate(self, story):
        pubdate = story.get_pubdate()
        if pubdate.tzinfo is None:
            pubdate = pytz.timezone("EST").localize(pubdate)
        else:
            pubdate = pubdate.astimezone(pytz.timezone("EST"))
        return pubdate > self.time

# COMPOSITE TRIGGERS

# Problem 7
class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger
        
    def evaluate(self, story):
        return not self.trigger.evaluate(story)

# Problem 8
class AndTrigger(Trigger):
    def __init__(self, t1, t2):
        self.t1 = t1
        self.t2 = t2
        
    def evaluate(self, story):
        return self.t1.evaluate(story) and self.t2.evaluate(story) 

# Problem 9
class OrTrigger(Trigger):
    def __init__(self, t1, t2):
        self.t1 = t1
        self.t2 = t2
        
    def evaluate(self, story):
        return self.t1.evaluate(story) or self.t2.evaluate(story) 


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    filtered_stories = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                filtered_stories.append(story)
                break
    return filtered_stories


#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    config_path = Path(filename)
    if not config_path.is_absolute() and not config_path.exists():
        config_path = Path(__file__).resolve().parent / config_path

    lines = []
    with config_path.open('r', encoding='utf-8') as trigger_file:
        for line in trigger_file:
            line = line.rstrip()
            if not (len(line) == 0 or line.startswith('//')):
                lines.append(line)
            
    trigger_map = {}
    active_triggers = []
    
    for line in lines:
        parts = line.split(',')
        if parts[0] == 'ADD':
            for name in parts[1:]:
                active_triggers.append(trigger_map[name])
        else:
            trig_name = parts[0]
            trig_type = parts[1]
            if trig_type == 'TITLE':
                trigger_map[trig_name] = TitleTrigger(parts[2])
            elif trig_type == 'DESCRIPTION':
                trigger_map[trig_name] = DescriptionTrigger(parts[2])
            elif trig_type == 'BEFORE':
                trigger_map[trig_name] = BeforeTrigger(parts[2])
            elif trig_type == 'AFTER':
                trigger_map[trig_name] = AfterTrigger(parts[2])
            elif trig_type == 'NOT':
                trigger_map[trig_name] = NotTrigger(trigger_map[parts[2]])
            elif trig_type == 'AND':
                trigger_map[trig_name] = AndTrigger(trigger_map[parts[2]], trigger_map[parts[3]])
            elif trig_type == 'OR':
                trigger_map[trig_name] = OrTrigger(trigger_map[parts[2]], trigger_map[parts[3]])

    return active_triggers


SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master, stop_event=None):
    if stop_event is None:
        stop_event = threading.Event()

    try:
        # Problem 11
        triggerlist = read_trigger_config('triggers.txt')
        
        # Draws the popup window that displays the filtered stories
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT, fill=Y)

        t = "Google Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica", 14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        def close_window():
            stop_event.set()
            master.destroy()

        button = Button(frame, text="Exit", command=close_window)
        button.pack(side=BOTTOM)
        guidShown = []
        
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while not stop_event.is_set():
            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("https://news.google.com/rss") 

            if stop_event.is_set():
                break

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)

            print("Sleeping...")
            stop_event.wait(SLEEPTIME)

    except Exception as e:
        if not stop_event.is_set():
            print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    stop_event = threading.Event()

    def close_window():
        stop_event.set()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", close_window)
    t = threading.Thread(target=main_thread, args=(root, stop_event), daemon=True)
    t.start()
    root.mainloop()
    stop_event.set()
    t.join(timeout=1)
