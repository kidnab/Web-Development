from django.shortcuts import render

from . import util
from markdown2 import Markdown

import random


def convert(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    html_content = convert(title)
    if html_content == None:
        return render(request, "encyclopedia/error.html",{ 
            "message": "This entry does not exist."
           })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })
   
def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        html_content = convert(entry_search)
        if html_content is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": entry_search,
                "content": html_content
            })
        else:
            entries = util.list_entries()
            search_results = []
            for entry in entries:
                if entry_search.lower() in entry.lower():
                    search_results.append(entry)
            return render(request, "encyclopedia/search.html", {
                "search_results": search_results
            })

    
def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        duplicate_title = util.get_entry(title)
        if duplicate_title is not None:
            return render(request, "encyclopedia/error.html", {
                "message": "Entry page already exists"
            })
        else:
            util.save_entry(title, content)
            html_content = convert(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": html_content
            })
    
            
def edit(request):
    if request.method == "POST":
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
           "title": title, 
           "content": content 
        })
        
def save_edit(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        html_content = convert(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })
        
def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    html_content = convert(random_entry)
    return render(request, "encyclopedia/entry.html", {
        "title" : random_entry,
        "content" : html_content
    })