from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import MyData

import requests
import json

# Create your views here.

def home(request):
    return render(request, 'home.html', {})

@csrf_exempt
def get_stock_data(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        ticker = request.POST.get('ticker', 'null')
        ticker = ticker.upper()

        try:
            ticker_data = MyData.objects.filter(symbol=ticker).order_by('timestamp')  
            timestamps = []
            open_prices = []
            high_prices = []
            low_prices = []
            close_prices = []
            volumes = []
            for entry in ticker_data:
                print("Debug: entry.timestamp =", entry.timestamp)  # Debugging
                if entry.timestamp is not None:
                    timestamps.append(entry.timestamp.strftime('%Y-%m-%d %H:%M:%S'))
                else:
                    # Handle the case where entry.timestamp is None
                    print("Warning: entry.timestamp is None for entry", entry)
                    break
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

        