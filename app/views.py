import json

from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views import generic

from .services.openai import AssistantSpaceX, InsuranceCalculator

class SpaceXView(generic.TemplateView):
    template_name = 'chat.html'

    def post(self, request, *args, **kwargs):
        if not self.request.headers.get('HX-Request'):
            raise Http404('Should be an HTMX request')

        thread = request.POST.get('messages')
        if not thread:
            return JsonResponse({'error': 'Invalid payload'}, status=400)

        try:
            payload = json.loads(thread)
            next_question = AssistantSpaceX(thread=payload).get_next_question()
            try:
                evaluation = json.loads(next_question)
                risk_level_display, insurers = self._calculate_insurance(evaluation=evaluation)
                return render(
                    request,
                    '_response.html',
                    {
                        'risk_level': risk_level_display,
                        'insurers': insurers,
                        'booking_date': timezone.localdate() + timezone.timedelta(days=30),
                        'evaluation': evaluation,
                    },
                )

            except json.JSONDecodeError:
                return JsonResponse({'next_question': next_question})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON payload'}, status=400)

    def _calculate_insurance(self, evaluation: dict):
        risk_level, risk_level_display = InsuranceCalculator(
            evaluation=evaluation,
        ).get_insurance_value()

        insurers = [
            {
                'name': 'Northwestern Mutual',
                'price': int((0.5 * risk_level) * 1500),
                'number_of_beneficiaries': 2,
                'death_benefit': 2300000000,
                'icon': 'northwestern.webp',
            },
            {
                'name': 'MassMutual',
                'price': int((1.24 * risk_level) * 2000),
                'number_of_beneficiaries': 2,
                'death_benefit': 700000000,
                'icon': 'massmutual.jpg',
            },
            {
                'name': 'New York Life',
                'price': int((0.4 * risk_level) * 1000),
                'number_of_beneficiaries': 1,
                'death_benefit': 1200000000,
                'icon': 'newyorklife.png',
            },
            {
                'name': 'Prudential',
                'price': int((0.3 * risk_level) * 1000),
                'number_of_beneficiaries': 3,
                'death_benefit': 500000000,
                'icon': 'prudential.jpg',
            },
            {
                'name': 'MetLife',
                'price': int((1 * risk_level) * 900),
                'number_of_beneficiaries': 3,
                'death_benefit': 600000000,
                'icon': 'metlife.jpg',
            },
        ]

        return risk_level_display, insurers

