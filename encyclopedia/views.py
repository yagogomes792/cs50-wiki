from django.shortcuts import render
from django import forms
from . import util
from markdown2 import Markdown
from django.http import HttpResponse, HttpResponseRedirect
import random

markdown = Markdown()


class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)


class CreateForm(forms.Form):
    title = forms.CharField(label='Title')
    body = forms.CharField(label='Content', widget=forms.Textarea(attrs={'rows':1, 'cols': 15}))


class EditForm(forms.Form):
    title = forms.CharField(label='Edit title')
    body = forms.CharField(label='Edit content', widget=forms.Textarea(attrs={'rows':1, 'cols': 15}))



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entries(request, title):
    t = util.get_entry(title)
    if t is None:
        form = SearchForm()
        content = "Page not found"
        return render(request, 'encyclopedia/error.html', {'form': form, 'content': content})
    else:
        form = SearchForm()
        md = util.get_entry(title)
        html = markdown.convert(md)
        return render(request,'encyclopedia/entries.html', {
            'title': title, 'content': html, 'form': form
        })

def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data.get('query')
            pre = False
            for entry in util.list_entries():
                if data == entry:
                    md = util.get_entry(data)
                    html = markdown.convert(md)
                    pre = True
                    break
            if pre:
                return render(request, 'encyclopedia/entries.html', {'content': html, 'form': form, 'title': data})
            else:
                entry_list = []
                for entry in util.list_entries():
                    if data in entry:
                        entry_list.append(entry)
                if len(entry_list) == 0:
                    form = SearchForm()
                    content = "This content doesn't exists"
                    return render(request, 'encyclopedia/error.html', {'form': form, 'content': content})
                else:
                    return render(request, 'encyclopedia/index.html', {'entries': entry_list, 'form': form})
    else:
        form = SearchForm()
        content = "Search"
        return render(request, 'encyclopedia/error.html', {'form': form, 'content': content})

def new(request):
    if request.method == 'POST':
        createform = CreateForm(request.POST)
        if createform.is_valid():
            title = createform.cleaned_data.get('title')
            body = createform.cleaned_data.get('body')
            pre = False
            for entry in util.list_entries():
                if title == entry:
                    pre = True
                    break
            if pre:
                content = 'This content already exists'
                form = SearchForm()
                return render(request, 'encyclopedia/error.html', {'form': form, 'content': content})
            else:
                util.save_entry(title, body)
                form = SearchForm()
                md = util.get_entry(title)
                html = markdown.convert(md)
                return render(request, 'encyclopedia/entries.html', {'title': title, 'content': html, 'form': form})
    else:
        form = SearchForm()
        createform = CreateForm()
        return render(request, 'encyclopedia/new.html', {'form': form, 'createform': createform})


def editContent(request, title):
    if request.method == 'POST':
        editContent = EditForm(request.POST)
        if editContent.is_valid():
            title = editContent.cleaned_data.get('title')
            body = editContent.cleaned_data.get('body')
            util.save_entry(title, body)
            form = SearchForm()
            html = markdown.convert(body)
            return render(request, 'encyclopedia/entries.html', {
                'title': title, 'content': html, 'form': form
            })
    else:
        form = SearchForm()
        editform = EditForm({'title': title, 'body': util.get_entry(title)})
        return render(request, 'encyclopedia/edit.html', {'form': form, 'editform': editform})


def randomContent(request):
    entries = util.list_entries()
    n = len(entries)
    entry = random.randint(0, n-1)
    title = entries[entry]
    md = util.get_entry(title)
    html = markdown.convert(md)
    form = SearchForm()
    return render(request, 'encyclopedia/random.html', {'form': form, 'title': title, 'content': html})