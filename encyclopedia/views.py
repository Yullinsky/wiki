from django.shortcuts import render, redirect
from . import util
import markdown2
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry_content = util.get_entry(title)

    if entry_content:
        return render (request, "encyclopedia/entry.html",{
            "title":title,
            "content": markdown2.markdown(entry_content)
        })
    else:
        return render (request, "encyclopedia/error.html",{
            "message": "Requested page was not found."
        })

def search (request):
    query = request.GET.get("q", "")
    entries = util.list_entries ()  
    
    if query in entries:
        return redirect("entry", title=query)
    
    results = [entry for entry in entries if query.lower() in entry.lower()]
    
    return render (request, "encyclopedia/search.html", {
        "query" : query,
        "results" : results
    })

def create (request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()

        if not title or not content:
            return render(request, "encyclopedia/error.html", {
                "message": "Neither the title nor the content can be empty."
            })

        if any(entry.lower() == title.lower() for entry in util.list_entries()):
            return render(request, "encyclopedia/error.html", {
                "message" : f"Already exist an entry with that title '{title}' "
            })
        
        util.save_entry(title, content)
        return redirect("entry", title=title)

    return render(request, "encyclopedia/create.html")

def edit(request, title):
    if request.method == "GET":
        entry_content = util.get_entry(title)
        if entry_content is None:
            return(request, "encyclopedia/error.html",{
                "message": f"The '{title}' entry do not exist."
            })

        return render(request, "encyclopedia/edit.html", {
            "title" : title,
            "content" : entry_content
        })
    
    elif request.method == "POST":
        new_content = request.POST.get("content", "").strip()
        util.save_entry(title, new_content)
        return redirect("entry", title=title)
    
def random_page (request):
    entries = util.list_entries()
    random_title = random.choice(entries) 
    return redirect("entry", title=random_title)