from datetime import datetime
from json import JSONDecodeError
import time
from typing import Callable, Union

import requests
    
from django.utils import timezone
from django.core.management.base import BaseCommand

from content_manager_app.models import HackerNewsComment, EntryTracker, HackerNewsJob, HackerNewsPoll, HackerNewsPollOption, HackerNewsStory


def fetch_hackernews_item(item_id: int) -> Union[dict, None]:
    """
    Fetches item data from hackernews api.

    Args:
        item_id (int): The id of the hackernews item you are trying to fetch.

    Returns:
        dict or None: Fetched data as a dictionary if successful, None on failure.
    """
    url = f'https://hacker-news.firebaseio.com/v0/item/{item_id}.json?print=pretty'
    
    # Make a get request on the url, If something goes wrong while making GET request to server, return None
    try:
        response = requests.get(url)
    except requests.RequestException:
        return None
    
    # If server returns an okay http_response, Parse json string response to dictionary
    if response.status_code == 200:
        try:
            data = response.json()
            # Hash the response and add to a new entry called hash
            data['hash'] = hash(response.text)
            return data
        # If code fails while parsing the json string response to a dictionary
        except JSONDecodeError:
            return None
    else:
        return None 
    
    
def fetch_hackernews_largest_item_id() -> Union[int, None]:
    """
    Fetches the largest item id from hackernews api

    Returns:
        int or None: Fetched data as a dictionary if successful, None on failure.
    """
    url = 'https://hacker-news.firebaseio.com/v0/maxitem.json'
    
    # Make a get request on the url, If something goes wrong while making GET request to server, return None
    try:
        response = requests.get(url)
    except requests.RequestException:
        return None
    
    # If server returns an ok http_response code, cast string to int, then return
    if response.status_code == 200:
        return int(response.text)
    else:
        return None
    
def fetch_hackernews_items_by_range(start_item_id: int, end_item_id: int, callback: Callable[[dict, bool], bool]=None) -> Union[list, None]:
    """
    Takes a start_id, and an end_id, and fetches all items via the ids between the ranges

    Args:
        start_item_id (int): The id of the item you want as the starting point 
        end_item_id (int): THe id of the item as the end point
        callback (Callable[[dict, bool], bool], optional): A callback function to execute if you want to process each item individually. Defaults to None.

    Returns:
        Union[list, None]: returns None if callback is present, else return a list of items
    """
    # Fetch hacker news items and store in an array to return
    def use_array(start_item_id: int, end_item_id: int):
        items = []
        while start_item_id <= end_item_id:
            item = fetch_hackernews_item(start_item_id)
            if isinstance(item, dict):
                items.append(item)
            start_item_id += 1
        return items

    # Send each item to a callback function to process
    def act_on_callback(start_item_id: int, end_item_id: int, callback: Callable):
        while start_item_id <= end_item_id:
            item = fetch_hackernews_item(start_item_id)
            if isinstance(item, dict):
                callback(item)
            start_item_id += 1
    
    # If a callable function is present, use, else call use_array
    if callable(callback):
        return act_on_callback(start_item_id, end_item_id, callback)
    else:
        return use_array(start_item_id, end_item_id)
        
        
def fetch_latest_hackernews_item_id_from_tracker(latest_item_id: int) -> int:
    """_summary_

    Args:
        latest_item_id (int): The now latest item id fetched, to be stored for later use

    Returns:
        int: returns the latest item id from the last run, indicating only an update is requeired.
        returns 0 if there was never a last run indicating the items table is empty, indicating the need for a complete synchronization instead of an update.
    """
    entry_tracker = EntryTracker.objects.first()
    EntryTracker.objects.update_or_create(pk='X', defaults={'item_id': latest_item_id})
    if isinstance(entry_tracker, EntryTracker):
        return entry_tracker.item_id
    else:
        return 0

def process_hackernews_item_to_respective_table(item: dict) -> bool:
    """
    Function processes an item dict, detects the type and processes it to respective db

    Args:
        item (dict): the item to process to the database

    Returns:
        bool: True if items is stored successfully
    """
    # convert item time timestamp to datetime that is timezone aware
    item['time'] = timezone.make_aware(datetime.fromtimestamp(item.get('time', 0)), timezone=timezone.utc)

    # type and id will always be required(present) as per the model schema documentation
    if item.get('type', None) == 'story' and item.get('id', None):
        item_id = item.get('id')
        # delete these values as they would generate a TypeError while unpacking
        del item['type']
        del item['id']
        # Unpacks item to model, refer to: https://docs.python.org/3/tutorial/controlflow.html#unpacking-argument-lists for more info
        HackerNewsStory(**item, item_id=item_id).save()
        return True
    
    elif item.get('type', None) == 'job' and item.get('id', None):
        item_id = item.get('id')
        
        del item['type']
        del item['id']
        HackerNewsJob(**item, item_id=item_id).save()
        return True
    
    elif item.get('type', None) == 'comment' and item.get('id', None):
        item_id = item.get('id')
        
        del item['type']
        del item['id']
        HackerNewsComment(**item, item_id=item_id).save()
        return True
    
    elif item.get('type', None) == 'poll' and item.get('id', None):
        item_id = item.get('id')
        
        del item['type']
        del item['id']
        HackerNewsPoll(**item, item_id=item_id).save()
        return True
    
    elif item.get('type', None) == 'pollopt' and item.get('id', None):
        item_id = item.get('id')
        
        del item['type']
        del item['id']
        HackerNewsPollOption(**item, item_id=item_id).save()
        return True
    return False
    

def synchronize_hackernews_items_to_database(items_length = 100) -> None:
    """
    Uses EntryTracker to determine if a a synchronization was done already, synchrnizes if it hasn't and updates subsequent items if it has

    Args:
        items_length (int, optional): The number of items you want to synchronize at first. Defaults to 100.

    Returns:
        _type_: _description_
    """
    latest_item_id_on_hackernews = fetch_hackernews_largest_item_id()
    latest_item_id_in_tables = fetch_latest_hackernews_item_id_from_tracker(latest_item_id_on_hackernews)
    # If no item is present in EntryTracker, Fetch and store, else synchronize
    if latest_item_id_in_tables == 0:
        # Handles the edge case of getting a value lesser than one as length
        items_length = max(1, items_length)
    
        # hackernews items starts from an id of 1, so start_id should not be lesser than 1
        start_item_id = max(1, latest_item_id_on_hackernews - items_length + 1)
        fetch_hackernews_items_by_range(start_item_id=start_item_id, end_item_id=latest_item_id_on_hackernews, callback=process_hackernews_item_to_respective_table)
        return items_length
    else:
        fetch_hackernews_items_by_range(start_item_id=latest_item_id_in_tables+1, end_item_id=latest_item_id_on_hackernews, callback=process_hackernews_item_to_respective_table)
        return f"{latest_item_id_on_hackernews - latest_item_id_in_tables}"
    
# 
def synchronize_hackernews_items_to_database_at_interval(items_length = 100, duration = 300, running_count = 1, command=None):
    """_summary_

    Args:
        items_length (int, optional): The number of items to fetch at first update. Defaults to 100.
        duration (int, optional): The number of seconds to wait for, before next synchroninization. Defaults to 300.
        running_count (int, optional): The number of times, synchronization has happened. Defaults to 1.
        command (_type_, optional): The command object. Defaults to None.
    """
    # The number of items updated into the database
    update_count = synchronize_hackernews_items_to_database(items_length)
    if update_count and isinstance(command, Command):
        command.stdout.write(command.style.SUCCESS(f'{update_count} records was synchronized, Synchronization run count: {running_count}'))
    time.sleep(duration)
    running_count += 1
    synchronize_hackernews_items_to_database_at_interval(duration=duration, running_count=running_count, command=command)

# The purpose of this object is to provide a Command Line Interface for the script
class Command(BaseCommand):
    help = 'Synchronizes HackerNews database to CodeWave\'s'

    def add_arguments(self, parser):
        parser.add_argument('-i', '--items-length', dest='items-length', type=int, help='Size of HackerNews items to fetch at first run, Default: 100')
        parser.add_argument('-w', '--wait-time', dest='wait-time', type=int, help='Time to wait before rerun in seconds, Default: 300(5 minutes)')

    def handle(self, *args, **options):
        items_length = options.get('items-length')
        if not items_length:
            items_length = 100
        wait_time = options.get('wait-time')
        if wait_time:
            synchronize_hackernews_items_to_database_at_interval(items_length, wait_time, command=self)
        else:
            self.stdout.write(self.style.SUCCESS(f'{synchronize_hackernews_items_to_database(items_length=items_length)} records was synchronized'))
        