from django.shortcuts import render

# Create your views here.

def index(request):
    """
    Index page
    """
    posts = [
        {
            "author": "Damian",
            "link": "www.someurl.com",
            "date": "2012-12-12"
        },
        {
            "author": "zettie",
            "link": "www.another-url.com",
            "date": "2020-9-12"
        }
    ]
    return render(request,
                  "gify/home.html",
                  {"section": "index", "posts": posts})

