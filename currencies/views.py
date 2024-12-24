from django.shortcuts import render,redirect
import os
import json
from django.conf import settings
from django.views import View
from .models import Currencies
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.utils.decorators  import method_decorator


class IndexView(View):
    def get_user_preference(self, user):
        if Currencies.objects.filter(user=user).exists():
            return Currencies.objects.get(user=user)
        return None

    @method_decorator(never_cache)
    def get(self, request):
        currency_data = []
        path = os.path.join(settings.BASE_DIR, 'currencies.json')
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for single_data in data:
                currency_data.append({'cc': single_data['cc'], 'symbol': single_data['symbol'], 'name': single_data['name']})


        user_preference = self.get_user_preference(request.user)
        return render(request, 'currencies/index.html', {
            'currencies': currency_data,
            'user_preference': user_preference
        })
    @method_decorator(never_cache)
    def post(self, request):
        user_preference = self.get_user_preference(request.user)
        currency = request.POST['currency']

        if user_preference:
            user_preference.currency = currency
            user_preference.save()
            messages.success(request, "Changes Saved")
        else:
            Currencies.objects.create(user=request.user, currency=currency)

        return redirect('currencies')

