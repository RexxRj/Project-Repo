from django.shortcuts import render
from django.http import HttpResponse,HttpResponseNotFound, HttpResponseRedirect

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


def monthly_challenge_by_number(request,month):
    try:
        assert month <= len(monthly_challenges), "Month doesn't exist"
        months = list(monthly_challenges.keys())
        return HttpResponseRedirect(months[month-1])
    except Exception as e:
        return HttpResponseNotFound(e)

def monthly_challenge(request,month):
    try:
        assert month in monthly_challenges.keys(), "Month doesn't exist"    
        return HttpResponse(monthly_challenges[month]);

    except Exception as e:
        return HttpResponseNotFound(e)