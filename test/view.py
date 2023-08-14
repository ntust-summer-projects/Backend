from django.shortcuts import render, redirect
from test.dataGenerator import *

def showTestPage(request, createObj = None):
    
    match createObj:
        case 'company':
            createCompany()
        case 'tag':
            createTag()
        case 'normalUser':
            createNormalUser()
        case 'product':
            createProduct()
        case _:
            return render(request, 'test/templates/test.html')
            
    return redirect('/test')