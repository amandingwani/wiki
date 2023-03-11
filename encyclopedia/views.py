from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
import markdown2
import random

from . import util, forms


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Displays the content of an entry
def entry(request, title):
    # get the entry
    entry = util.get_entry(title)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": markdown2.markdown(entry) if entry else None
        })

def search(request):
    # if the number of arguments is not 1
    if len(request.GET) != 1:
        return render(request, "encyclopedia/search.html", {
            "is_valid": False
        })
    
    q = request.GET["q"]

    subs = [] # list of entries with q as substring
    # check query with entries
    for entry in util.list_entries():
        q_lower = q.lower()
        en_lower = entry.lower()
        if q_lower in en_lower:
            subs.append(entry)
            if q_lower == en_lower:
                return HttpResponseRedirect(reverse("encyclopedia:entry", args=[q]))

    return render(request, "encyclopedia/search.html", {
        "is_valid": True,
        "entries" : subs
    })

# view for creating new entry
def new(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = forms.NewPageForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # check if entry already exists
            entry = util.get_entry(form.cleaned_data['title'])
            if entry:
                return render(request, "encyclopedia/new.html", {"exists": True})
            util.save_entry(form.cleaned_data['title'], form.cleaned_data['content'])
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('encyclopedia:entry', args=[form.cleaned_data['title']]))
        else:
            return render(request, "encyclopedia/new.html", {"form": form})
    else:
        form = forms.NewPageForm()
        return render(request, "encyclopedia/new.html", {"form": form, "exists": False})
    
def edit(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = forms.NewPageForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            util.save_entry(form.cleaned_data['title'], form.cleaned_data['content'])
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('encyclopedia:entry', args=[form.cleaned_data['title']]))
        else:
            return render(request, "encyclopedia/new.html", {"form": form})
    else:
        title = request.GET["q"]
        # get the entry
        entry = util.get_entry(title)

        # if the number of arguments is not 1 or title is not valid
        if len(request.GET) != 1 or not entry:
            return HttpResponseRedirect(reverse("encyclopedia:index"))
        
        # content = util.get_entry(q)
        form = forms.NewPageForm({"title": title, "content":entry})

        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "form": form
            })
    
def random_page(request):
    entry = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse('encyclopedia:entry', args=[entry]))