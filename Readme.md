# CodeWave - A Better Application Interface for The HackerNews Website

CodeWave is a Python/Django web application that synchronizes the hackernews database to itself and displays the items to users in a more appeasing and navigatable manner.

## Notes

- PostgreSQL was used for the database server during developement. It has been reverted to sqlite for the project purpose
- Because of the simplicity of this test, Unit tests wasn't used, and this package wasn't setup to a python installation.
- All items have an hash, this was done in response to the possiblity that items might need to be updated from requested API
- The database tables is horizontally sharded by source and item type
- Debug was purposely left true for testing

## Features

- Fetches a specified amount of items from the hackernews api
- Subsequently synchronizes any new item from the hackernews api
- CodeWave also exposes APIs so you can perform CRUD operations on items with a restriction exempting the hackernews items
- CodeWave has a Stylized web interface where users can interact with items

## installation & Startup

- Create a venv in this directory and activate it
- Install all dependencies in the requirements.txt (pip3 install -r requirements.txt)
- Then run application (python manage.py runserver)

## Run HackerNews Synchronizer
``` bash
python manage.py hackernews_synchronizer
```
For more information, run:
``` bash
python manage.py hackernews_synchronizer --help
```

## API Documentation
- Host: 127.0.0.1
- Fetch Items by Type: ./type/
- Fetch Items by Source: ./source/
- Retrieve Item Information ./item/<str:item_source>/<str:item_type>/<int:item_id>
- Store Item ./store_item/
_Item requirements_
``` python
{
    item_type: AnyOf['story', 'job', 'comment', 'poll', 'pollopt'] (required)
    by: str (required)
    title: str
    url: str
    text: str
     In Addition For Comments
     {
         parent: int(required) # parent id
         parent_type: str(required) # Item type of the parent
     }
     In Addition For Polls
     {
         poll: int(required) # poll id
     }
}
```
- Update Item ./update_item/
```
    Poll and Pollopts:
    {
        id: int(required) # id of the item to edit
        # items values you can change
        score: int
        deleted: int
    }
    Comment:
    {
        id: int(required) # id of the item to edit
        # items values you can change
        score: int
        text: str
        deleted: int
    }
    Job and Story:
    {
        id: int(required) # id of the item to edit
        # items values you can change
        score: int
        title: str
        text: str
        deleted: int
    }
```