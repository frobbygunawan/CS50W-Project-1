from django.shortcuts import render

from . import util

# For redirecting
from django.urls import reverse
from django.http import HttpResponseRedirect

import markdown2
import random

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
            "md_content": markdown2.markdown(md_content),
            "title":title
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
            "md_content": markdown2.markdown(util.get_entry(entry_title)),
            "title": entry_title
        })

# Should test this first
def new_entry(request):
    if request.method == "POST":
        new_title = request.POST["new_title"]
        new_desc = request.POST["new_desc"]
        if util.get_entry(new_title) != None:
            return render(request, "encyclopedia/error.html", {
            "message": "Sorry, the entry already exist."
        })
        else:
            util.save_entry(new_title, new_desc)
            return render(request, "encyclopedia/entry.html", {
                "md_content": markdown2.markdown(util.get_entry(new_title)),
                "title":new_title
            })
    return render(request, "encyclopedia/new_entry.html")

def edit(request, title):
    if request.method == "GET":
        entry_title = title
        entry_content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": entry_title,
            "md_content": entry_content
        })
    elif request.method == "POST":
        util.save_entry(request.POST["edit_title"], request.POST["edit_desc"])
        return render(request, "encyclopedia/entry.html", {
                "md_content": markdown2.markdown(util.get_entry(request.POST["edit_title"])),
                "title":request.POST["edit_title"]
        })

def random_entry(request):
    entries = util.list_entries()
    rand_number = random.randint(0, len(entries) - 1)
    rand_entry = entries[rand_number]
    return render(request, "encyclopedia/entry.html", {
                "md_content": markdown2.markdown(util.get_entry(rand_entry)),
                "title":rand_entry
        })
