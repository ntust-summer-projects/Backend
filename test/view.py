from django.shortcuts import render, redirect
from test.dataGenerator import *

def showTestPage(request, createObj = None):
    
    result = ""
    
    match createObj:
        case 'company':
            result = "Company: " + createCompany()
        case 'tag':
            createTag()
            result = "Tag"
        case 'normalUser':
            result = "NormalUser: " + createNormalUser()
        case 'product':
            result = "Product: " + createProduct()
        case 'announcement':
            result = 'Announcement: ' + createAnnouncement()

    return render(request, 'test/templates/test.html', {'result': result})
            