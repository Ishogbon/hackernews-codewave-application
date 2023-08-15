from itertools import chain

from operator import attrgetter
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.core.paginator import Paginator
from django.core.serializers import serialize

from content_manager_app.models import CodeWaveComment, CodeWaveJob, CodeWavePoll, CodeWaveStory, HackerNewsComment, HackerNewsJob, HackerNewsPoll, HackerNewsStory

def homepage(request, page=1) -> HttpResponse:
    text_filter = request.GET.get('text_filter')
    # By default, django query sets are lazy, so do not worry about executing unnecessary SQL statements
    hackernews_story_list_query_set = HackerNewsStory.objects.filter(deleted=False, dead=False)
    codewave_story_list_query_set = CodeWaveStory.objects.filter(deleted=False, dead=False)
    hackernews_job_list_query_set = HackerNewsJob.objects.filter(deleted=False, dead=False)
    codewave_job_list_query_set = CodeWaveJob.objects.filter(deleted=False, dead=False)
    hackernews_comment_list_query_set = HackerNewsPoll.objects.filter(deleted=False, dead=False)
    codewave_comment_list_query_set = CodeWavePoll.objects.filter(deleted=False, dead=False)
    
    if text_filter:
        hackernews_story_list_query_set = hackernews_story_list_query_set.filter(title__icontains=text_filter)
        codewave_story_list_query_set = codewave_story_list_query_set.filter(title__icontains=text_filter)
        hackernews_job_list_query_set = hackernews_job_list_query_set.filter(title__icontains=text_filter)
        codewave_job_list_query_set = codewave_job_list_query_set.filter(title__icontains=text_filter)
        hackernews_comment_list_query_set = hackernews_comment_list_query_set.filter(title__icontains=text_filter)
        codewave_comment_list_query_set = codewave_comment_list_query_set.filter(title__icontains=text_filter)
        
    
    item_list_query_set = chain(hackernews_story_list_query_set, codewave_story_list_query_set, hackernews_job_list_query_set, 
                                codewave_job_list_query_set, hackernews_comment_list_query_set, codewave_comment_list_query_set)

    item_list_query_set = sorted(
        item_list_query_set, 
        key=attrgetter('time'),  # Replace with the actual timestamp field
        reverse=True
    )
    paginator = Paginator(item_list_query_set, 7)
    

    page_object = paginator.get_page(page)
    return render(request, 'homepage.html', {'page_object':page_object})

def stories(request, page=1) -> HttpResponse:
    text_filter = request.GET.get('text_filter')

    hackernews_story_list_query_set = HackerNewsStory.objects.filter(deleted=False, dead=False)
    codewave_story_list_query_set = CodeWaveStory.objects.filter(deleted=False, dead=False)
    
    if text_filter:
        hackernews_story_list_query_set = HackerNewsStory.objects.filter(deleted=False, dead=False).filter(title__icontains=text_filter)
        codewave_story_list_query_set = CodeWaveStory.objects.filter(deleted=False, dead=False).filter(title__icontains=text_filter)
        
    
    item_list_query_set = chain(hackernews_story_list_query_set, codewave_story_list_query_set)

    item_list_query_set = sorted(
        item_list_query_set, 
        key=attrgetter('time'),  # Replace with the actual timestamp field
        reverse=True
    )
    paginator = Paginator(item_list_query_set, 7)
    

    page_object = paginator.get_page(page)
    return render(request, 'homepage.html', {'page_object':page_object})

def jobs(request, page=1) -> HttpResponse:
    text_filter = request.GET.get('text_filter')
    
    hackernews_job_list_query_set = HackerNewsJob.objects.filter(deleted=False, dead=False)
    codewave_job_list_query_set = CodeWaveJob.objects.filter(deleted=False, dead=False)
    
    if text_filter:
        hackernews_job_list_query_set = HackerNewsJob.objects.filter(deleted=False, dead=False).filter(title__icontains=text_filter)
        codewave_job_list_query_set = CodeWaveJob.objects.filter(deleted=False, dead=False).filter(title__icontains=text_filter)
        
    
    item_list_query_set = chain(hackernews_job_list_query_set, codewave_job_list_query_set)

    item_list_query_set = sorted(
        item_list_query_set, 
        key=attrgetter('time'),  # Replace with the actual timestamp field
        reverse=True
    )
    
    paginator = Paginator(item_list_query_set, 7)
    

    page_object = paginator.get_page(page)
    return render(request, 'homepage.html', {'page_object':page_object})

def polls(request, page=1) -> HttpResponse:
    text_filter = request.GET.get('text_filter')

    hackernews_comment_list_query_set = HackerNewsPoll.objects.filter(deleted=False, dead=False)
    codewave_comment_list_query_set = CodeWavePoll.objects.filter(deleted=False, dead=False)
    
    if text_filter:
        hackernews_comment_list_query_set = HackerNewsPoll.objects.filter(deleted=False, dead=False).filter(title__icontains=text_filter)
        codewave_comment_list_query_set = CodeWavePoll.objects.filter(deleted=False, dead=False).filter(title__icontains=text_filter)
        
    
    item_list_query_set = chain(hackernews_comment_list_query_set, codewave_comment_list_query_set)

    item_list_query_set = sorted(
        item_list_query_set, 
        key=attrgetter('time'),  # Replace with the actual timestamp field
        reverse=True
    )
    paginator = Paginator(item_list_query_set, 7)
    

    page_object = paginator.get_page(page)
    return render(request, 'homepage.html', {'page_object':page_object})

# This is an helper function meant to process comments
def process_comments(comment_list: list, comment_source='hns', indent=0.5):
    if not isinstance(comment_list, list) or len(comment_list) < 1:
        return False
    comment_models = {'hns': HackerNewsComment, 'cwe': CodeWaveComment}
    processed_comments = []
    for comment_id in comment_list:
        comment = comment_models.get(comment_source, HackerNewsComment).objects.filter(deleted=False, dead=False, item_id=comment_id)
        if comment.exists():
            comment = comment.get()
            comment = {'text': comment.text, 'by': comment.by, 'score': comment.score, 'indent': indent, 'kids': comment.kids}
            processed_comments.append(comment)
            inner_comments = process_comments(comment.get('kids', None), comment_source, indent+1)
            if inner_comments:
                # If you want a tree structure just overwrite the kids like this comment['kids'] = inner_comments
                for inner_comment in inner_comments:
                    processed_comments.append(inner_comment)
            else:
                del comment['kids']
    return processed_comments

# This is an helper function to process poll options
def process_pollopts(pollopt_list: list, pollopt_source='hns'):
    if not isinstance(pollopt_list, list) or len(pollopt_list) < 1:
        return False
    pollopt_models = {'hns': HackerNewsComment, 'cwe': CodeWaveComment}
    processed_pollopts = []
    for pollopt_id in pollopt_list:
        pollopt = pollopt_models.get(pollopt_source, HackerNewsComment).objects.filter(deleted=False, dead=False, item_id=pollopt_id)
        if pollopt.exists():
            pollopt = pollopt.get()
            pollopt = {'text': pollopt.text, 'score': pollopt.score}
            processed_pollopts.append(pollopt)
    return processed_pollopts
            

def item_page(request, item_source, item_type, item_id):
    item_model = None
    
    if item_source == 'hns':
        if item_type == 'story':
            item_model = HackerNewsStory
        elif item_type == 'job':
            item_model = HackerNewsJob
        elif item_type == 'poll':
            item_model = HackerNewsPoll
    elif item_source == 'cwe':
        if item_type == 'story':
            item_model = CodeWaveStory
        elif item_type == 'job':
            item_model = CodeWaveJob
        elif item_type == 'poll':
            item_model = CodeWavePoll
        
    if item_model:
        item = item_model.objects.filter(deleted=False, dead=False, item_id=item_id)
        if not item.exists():
            raise Http404('Item not found')
        item = item.get()
        item_comments = process_comments(item.kids, item_source)
        
        # Ensures item_comments is a list
        if not isinstance(item_comments, list):
            item_comments = []
        item_pollopts = None
        if item_type == 'poll':
            item_pollopts = process_pollopts(item.parts, item_source)
            # ensures item_pollopts is a list
            if not isinstance(item_pollopts, list):
                item_pollopts = []
            
        return render(request, 'item.html', {'item':item, 'comments': item_comments, 'pollopts': item_pollopts})
        
    