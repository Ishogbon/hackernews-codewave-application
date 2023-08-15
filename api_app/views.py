from datetime import datetime
from itertools import chain
import json
from operator import attrgetter
from django.forms import ValidationError
from django.http import HttpResponseServerError, JsonResponse
from django.core.serializers import serialize
from django.core.validators import URLValidator
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt

from content_manager_app.models import CodeWaveComment, CodeWaveJob, CodeWavePoll, CodeWavePollOption, CodeWaveStory, HackerNewsComment, HackerNewsJob, HackerNewsPoll, HackerNewsPollOption, HackerNewsStory
from . import responses
# Control the maximum amount of items that the api can return
ITEMS_RETURN_LENGTH = 100

@require_GET
def fetch_items_by_type(request, item_type='all') -> JsonResponse:
    items = []
    if item_type == 'all':
        items.append(HackerNewsStory.objects.all())
        items.append(CodeWaveStory.objects.all())
        items.append(HackerNewsJob.objects.all())
        items.append(CodeWaveJob.objects.all())
        items.append(HackerNewsComment.objects.all())
        items.append(CodeWaveComment.objects.all())
        items.append(HackerNewsPoll.objects.all())
        items.append(CodeWavePoll.objects.all())
        items.append(HackerNewsPollOption.objects.all())
        items.append(CodeWavePollOption.objects.all())
    elif item_type == 'stories':
        items.append(HackerNewsStory.objects.all())
        items.append(CodeWaveStory.objects.all())
    elif item_type == 'jobs':
        items.append(HackerNewsJob.objects.all())
        items.append(CodeWaveJob.objects.all())
    elif item_type == 'comments':
        items.append(HackerNewsComment.objects.all())
        items.append(CodeWaveComment.objects.all())
    elif item_type == 'polls':
        items.append(HackerNewsPoll.objects.all())
        items.append(CodeWavePoll.objects.all())
    elif item_type == 'pollopts':
        items.append(HackerNewsPollOption.objects.all())
        items.append(CodeWavePollOption.objects.all())
    else:
        return JsonResponse(responses.INVALID_ITEM_QUERY)
        
    items = chain(*items)
    
    # By default items will be returned starting from the latest
    items = sorted(
        items, 
        key=attrgetter('item_id'),
        reverse=True
    )
    
    return JsonResponse(generate_response(items[:ITEMS_RETURN_LENGTH], 'item_id', 'TYPE', 'SOURCE'), safe=False)

@require_GET
def fetch_items_by_source(request, item_source='hns') -> JsonResponse:
    items = []
    if item_source == 'hns':
        items.append(HackerNewsStory.objects.all())
        items.append(HackerNewsJob.objects.all())
        items.append(HackerNewsComment.objects.all())
        items.append(HackerNewsPoll.objects.all())
        items.append(HackerNewsPollOption.objects.all())
    elif item_source == 'cwe':
        items.append(CodeWaveStory.objects.all())
        items.append(CodeWaveJob.objects.all())
        items.append(CodeWaveComment.objects.all())
        items.append(CodeWavePoll.objects.all())
        items.append(CodeWavePollOption.objects.all())
    else:
        return JsonResponse(responses.INVALID_SOURCE)
    
        
    items = chain(*items)
    
    # By default items will be returned starting from the latest
    items = sorted(
        items, 
        key=attrgetter('item_id'),
        reverse=True
    )
    
    return JsonResponse(generate_response(items[:ITEMS_RETURN_LENGTH], 'item_id', 'TYPE'), safe=False)

@require_GET
def retrieve_item(request, item_source='hns', item_type='story', item_id=None) -> JsonResponse:
    if not isinstance(item_id, int):
        return JsonResponse(responses.INVALID_ITEM)
    elif item_id < 1:
        return JsonResponse(responses.INVALID_ID)       
    item = None
    if item_source == 'hns':
        if item_type == 'story':
            item = HackerNewsStory.objects.filter(item_id=item_id)
        elif item_type == 'job':
            item = HackerNewsJob.objects.filter(item_id=item_id)
        elif item_type == 'comment':
            item = HackerNewsComment.objects.filter(item_id=item_id)
        elif item_type == 'poll':
            item = HackerNewsPoll.objects.filter(item_id=item_id)
        elif item_type == 'pollopt':
            item = HackerNewsPollOption.objects.filter(item_id=item_id)
        else:
            return JsonResponse(responses.UNSPECIFIED_ITEM)    
    elif item_source == 'cwe':
        if item_type == 'story':
            item = CodeWaveStory.objects.filter(item_id=item_id)
        elif item_type == 'job':
            item = CodeWaveJob.objects.filter(item_id=item_id)
        elif item_type == 'comment':
            item = CodeWaveComment.objects.filter(item_id=item_id)
        elif item_type == 'poll':
            item = CodeWavePoll.objects.filter(item_id=item_id)
        elif item_type == 'pollopt':
            item = CodeWavePollOption.objects.filter(item_id=item_id)
        else:
            return JsonResponse(responses.UNSPECIFIED_ITEM)
    else:
        return JsonResponse(responses.INVALID_SOURCE)
    
    if not item.exists():
        return JsonResponse(responses.INVALID_ITEM)
    
    try:
        item = serialize('json', item)
        item = json.loads(item)[0]['fields']
        
        # The information below will only be used for internal purposes
        del item['entry_time']
        del item['hash']

        # Since timezone is by default in UTC, conversion won't be ncessary
        item['time'] = int(datetime.strptime(item.get('time'), "%Y-%m-%dT%H:%M:%SZ").timestamp())
    
    except: # The nature of the serialize, and json.loads in this context warrants the use of a generic exception handler
       return HttpResponseServerError(responses.INTERNAL_ERROR)
        
    return JsonResponse(item, safe=False)

@require_POST
@csrf_exempt
def store_item(request) -> JsonResponse:
    item_hash = hash(request.body)
    try:
        item = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(responses.JSON_DECODE_ERROR)
    
    item_id = 0
    
    # If item is not a dictionary
    if not isinstance(item, dict):
        return JsonResponse(responses.JSON_DECODE_ERROR)
    
    # Check if 'by' field is present and is a string
    if 'by' not in item or not isinstance(item['by'], str):
        return JsonResponse(responses.generate_missing_or_invalid_field_error('by'))
    
    # Check if 'type' field is present and is within the allowed types
    if 'type' not in item or item['type'] not in ['story', 'job', 'comment', 'poll', 'pollopt']:
        return JsonResponse(responses.MISSING_INVALID_TYPE_FIELD)
    
    
    def validate_url(item):
        if 'url' in item:
            validator = URLValidator()
            try:
                validator(item.get('url'))
            except ValidationError:
                return True
    
    def validate_title(item):
        if 'title' not in item or not isinstance(item['title'], str) or len(item['title']) < 1:
            return True
        
    def validate_text(item):
        if 'text' not in item or not isinstance(item['text'], str) or len(item['text']) < 1:
            return True
            

    if item.get('type') == 'story':
        if validate_url(item):
            return JsonResponse(responses.INVALID_URL)
        if validate_title(item):
            return JsonResponse(responses.generate_missing_or_invalid_field_error('title'))
        # Fetch highest id in table 
        latest_entry = CodeWaveStory.objects.order_by('-item_id').first()
        next_id = 1 if latest_entry is None else latest_entry.item_id + 1
        story = CodeWaveStory(item_id=next_id, by=item.get('by'), 
                              kids=[], title=item.get('title'),
                              url=item.get('url', ""), hash=item_hash, 
                              descendants=0, text=item.get('text', ""))
        story.save()
    elif item.get('type') == 'job':
        if validate_url(item):
            return JsonResponse(responses.INVALID_URL)
        if validate_title(item):
            return JsonResponse(responses.generate_missing_or_invalid_field_error('title'))
        latest_entry = CodeWaveJob.objects.order_by('-item_id').first()
        next_id = 1 if latest_entry is None else latest_entry.item_id + 1
        job = CodeWaveJob(item_id=next_id, by=item.get('by'), 
                              kids=[], title=item.get('title'),
                              url=item.get('url', ""), hash=item_hash, 
                              text=item.get('text', ""))
        job.save()
    elif item.get('type') == 'comment':
        if validate_text(item):
            return JsonResponse(responses.generate_missing_or_invalid_field_error('text'))
        # Makes sure parent is present in comment
        if 'parent' not in item or not isinstance(item['parent'], int) or item['parent'] < 1:
            return JsonResponse(responses.generate_missing_or_invalid_field_error('parent'))
        if 'parent_type' not in item or item['parent_type'] not in ['job', 'story', 'poll', 'comment']:
            return JsonResponse(responses.generate_missing_or_invalid_field_error('parent_type'))
        
        latest_entry = CodeWaveComment.objects.order_by('-item_id').first()
        next_id = 1 if latest_entry is None else latest_entry.item_id + 1
        
        parent_model = CodeWaveStory
        if item['parent_type'] == 'comment':
            parent_model = CodeWaveComment
        elif item['parent_type'] == 'job':
            parent_model = CodeWaveJob
        elif item['parent_type'] == 'poll':
            parent_model = CodeWavePoll
        
        # Fetches the parent kids by id
        parent = parent_model.objects.filter(item_id=item['parent']) 
        if not parent.exists():
            return JsonResponse(responses.PARENT_NO_EXISTS)
        parent = parent.get()
        parent_kids = parent.kids   
        # Check if the kids is null, replace with list if null
        if not parent_kids:
            parent_kids = []       
        # add comment id to it
        parent_kids.append(next_id)
        parent.kids = parent_kids
        parent.save()
        
        comment = CodeWaveComment(item_id=next_id, by=item.get('by'), 
                              kids=[], hash=item_hash,
                              text=item.get('text'), parent=item.get('parent'))
        comment.save()
    elif item.get('type') == 'poll':
        if validate_title(item):
            return JsonResponse(responses.generate_missing_or_invalid_field_error('title'))
        latest_entry = CodeWavePoll.objects.order_by('-item_id').first()
        next_id = 1 if latest_entry is None else latest_entry.item_id + 1
        poll = CodeWavePoll(item_id=next_id, by=item.get('by'), 
                              kids=[], title=item.get('title'),
                              parts=[], hash=item_hash, 
                              descendants=0, text=item.get('text', ""))
        poll.save()
    elif item.get('type') == 'pollopt':
        if validate_text(item):
            return JsonResponse(responses.generate_missing_or_invalid_field_error('text'))
        # Makes sure poll is present in pollopt
        if 'poll' not in item or not isinstance(item['poll'], int) or item['poll'] < 1:
            return JsonResponse(responses.generate_missing_or_invalid_field_error('poll'))
        latest_entry = CodeWavePollOption.objects.order_by('-item_id').first()
        next_id = 1 if latest_entry is None else latest_entry.item_id + 1
        
        # Fetches the parent parts by id
        parent = CodeWavePoll.objects.filter(item_id=item['poll']) 
        if not parent.exists():
            return JsonResponse(responses.PARENT_NO_EXISTS)
        parent = parent.get()
        parent_parts = parent.parts
        # Check if the kids is null, replace with list if null
        if not parent_parts:
            parent_kids = []       
        # add comment id to it
        parent_parts.append(next_id)
        # increment the descendants
        parent.descendants = parent.descendants + 1
        parent.parts = parent_parts
        parent.save()
        pollopt = CodeWavePollOption(item_id=next_id, by=item.get('by'), 
                              kids=[], hash=item_hash, 
                              text=item.get('text'), poll=item.get('poll'))
        pollopt.save()

    return JsonResponse(responses.ITEM_POST_SUCCESS)

@csrf_exempt
def no_api(request):
    return JsonResponse(responses.NO_API)

# THis is an helper function to generate a response
def generate_response(items, *args) -> list:
    generated_response = []
    for item in items:
        if len(args) > 1:
            generated_response_sub = []
            for arg in args:
                try: # This error will occur if the user did not properly study the models and its attributes
                    generated_response_sub.append(getattr(item, arg))
                except AttributeError:
                    return {responses.PROCESS_ERROR}
            generated_response.append(generated_response_sub)
        else:
            try:
                generated_response.append(getattr(item, args[0]))
            except AttributeError:
                return {responses.PROCESS_ERROR}
            
    return generated_response