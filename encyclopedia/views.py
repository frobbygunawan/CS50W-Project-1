from django.shortcuts import render

from . import util

# For redirecting
from django.urls import reverse
from django.http import HttpResponseRedirect

import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    md_content = util.get_entry(title)
    if md_content == None:
        return render(request, "encyclopedia/error.html", {
            "message": "Sorry, your entry does not exist yet."
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "md_content": markdown2.markdown(md_content)
        })

# Might need tuning for the case sensitive problem
def search(request):
    entry_title = request.GET['q']
    if util.get_entry(entry_title) == None:
        close_match = []
        for entry in util.list_entries():
            if entry.find(entry_title) != -1:
                close_match.append(entry)
        return render(request, "encyclopedia/search.html", {
            "close_match": close_match,
            "entry_title":entry_title
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "md_content": markdown2.markdown(util.get_entry(entry_title))
        })

# Should test this first
def new_entry(request):
    new_title = request.POST["new_title"]
    new_desc = request.POST["new_desc"]
    if request.method == POST:
        if util.get_entry(new_title) != None:
            return render(request, "encyclopedia/error.html", {
            "message": "Sorry, the entry already exist."
        })
        else:
            util.save_entry(new_title, new_desc)
            return render(request, "encyclopedia/entry.html", {
                "md_content": markdown2.markdown(util.get_entry(new_title))
            })
    return render(request, "encyclopedia/new_entry.html")