from django.shortcuts import render

from . import util
from markdown2 import Markdown


def convert(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    if content == None: 
        content = util.get_entry(title.capitalize())
    if content == None: 
        content = util.get_entry(title.upper())
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
                "search results": search_results
            })