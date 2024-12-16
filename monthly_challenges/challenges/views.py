from django.shortcuts import render
from django.http import HttpResponse,HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse

# Create your views here.

monthly_challenges = {
    "january": "Eat no meat for the month",
    "february": "Walk 10 kms everyday",
    "march": "learn django for 20 mins",
    "april": "Eat no meat for the month",
    "may": "Walk 10 kms everyday",
    "june": "learn django for 20 mins",
    "july": "learn django for 20 mins",
    "august": "Eat no meat for the month",
    "september": "Walk 10 kms everyday",
    "october": "learn django for 20 mins",
    "november": "Eat no meat for the month",
    "december": "Walk 10 kms everyday"
}

def index(request):
    try:
        response_text = ""
        for key in monthly_challenges.keys():
            link = reverse("month-challenge",args=[key])
            response_text+= f"<li><a href = '{link}'>{key.capitalize()}</a></li>\n"
        
        response_text = f"<ul>{response_text}</ul>"
        
        return HttpResponse(response_text)
    except Exception as e:
        return HttpResponseNotFound(e)
    


def monthly_challenge_by_number(request,month):
    try:
        assert month <= len(monthly_challenges), "Month doesn't exist"
        months = list(monthly_challenges.keys())
        redirect_month = months[month-1]
        redirect_path = reverse("month-challenge", args=[redirect_month])
        return HttpResponseRedirect(redirect_path)
    except Exception as e:
        return HttpResponseNotFound(e)

def monthly_challenge(request,month):
    try:
        assert month in monthly_challenges.keys(), f"<h2>Month doesn't exist</h2>"
        challenge_text = monthly_challenges[month]
        challenge_text = f"<h2>{challenge_text}</h2>"    
        return HttpResponse(challenge_text)

    except Exception as e:
        return HttpResponseNotFound(e)