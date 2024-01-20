from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import MyData

import os
import subprocess
import requests
import json

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset
from torch.utils.data import DataLoader

# Create your views here.

def home(request):
    return render(request, 'home.html', {})

@csrf_exempt
def runJavaAPI (request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        ticker = request.POST.get('ticker', 'null')
        ticker = str(ticker).upper()
        print("TICKER JAVA: " + ticker + "!!!")
        print("Current Working Directory:", os.getcwd())
    try:
        command = ["java", "-cp", "java_lib/*:java_src", "Main", ticker]
        print(command)
        result = subprocess.run(command, cwd='.', capture_output=True, text=True, check=True)
        output = result.stdout
        return JsonResponse({'status': 'success', 'output': output})
    except Exception as e:
        print("SOMETHING WRONG")
        print(e.stderr)
        print(e)
        return JsonResponse({'status': 'error', 'output': 'err'})


@csrf_exempt
def get_stock_data(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        ticker = request.POST.get('ticker', 'null')
        ticker = ticker.upper()
        print("TICKER STOCK: " + ticker + "!!!")

        try:
            ticker_data = MyData.objects.filter(symbol=ticker).order_by('timestamp')  
            timestamps = []
            open_prices = []
            high_prices = []
            low_prices = []
            close_prices = []
            volumes = []
            for entry in ticker_data:
                timestamps.append(entry.timestamp)
                open_prices.append(entry.open)
                high_prices.append(entry.high)
                low_prices.append(entry.low)
                close_prices.append(entry.close)
                volumes.append(entry.volume)
            data_dict = {
                'timestamps': timestamps,
                'open_prices': open_prices,
                'high_prices': high_prices,
                'low_prices': low_prices,
                'close_prices': close_prices,
                'volumes': volumes,
            }
            return JsonResponse(data_dict)
        except MyData.DoesNotExist:
            pass
    else:
        message = "Not ajax"
        return HttpResponse(message)