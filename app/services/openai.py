import json
import logging
import re
import unicodedata
from dataclasses import dataclass

import requests
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone as tz

from app.data import SPACE_X_PROMPT
from app.services.apft import APFTCalculator

logger = logging.getLogger('app.consumer') 


DAILY_TOKENS_CACHE_KEY = 'open_ai_tokens_{0}'


def has_budget() -> bool:
    """Returns True if the daily limit of OpenAI tokens has not been reached."""
    used_tokens = cache.get(DAILY_TOKENS_CACHE_KEY.format(tz.localdate().isoformat()), 0)
    return used_tokens < settings.OPENAI_DAILY_MAX_TOKENS


def clean_string(string: str) -> str:
    """Cleans a string by removing accents and special characters.

    NFD (Normalization Form Canonical Decomposition) splits accented characters into a base
    character and a combining character.
    Mn (Mark, Nonspacing) signifies that the character is a nonspacing combining character.
    """
    response = ''.join(
        c for c in unicodedata.normalize('NFD', string) if unicodedata.category(c) != 'Mn'
    )
    return re.sub(r'[^A-Za-z 0-9\.\:]+', '', response)


@dataclass
class OpenAI:
    """OpenAI service."""

    def __post_init__(self) -> None:
        self._app_key: str = settings.OPENAI_API_KEY
        self._session: requests.Session = requests.Session()

    def _request(self, **kwargs: dict) -> str:
        headers = kwargs.pop('headers', {})
        headers.update(
            {
                'Authorization': f'Bearer {self._app_key}',
                'content-type': 'application/json',
            }
        )

        try:
            response = self._session.request(
                method='post',
                url=settings.OPENAI_REQUEST_URL,
                headers=headers,
                **kwargs,
            )

            response.raise_for_status()
            # Update the daily tokens cache
            response_json = response.json()
            cache_key = DAILY_TOKENS_CACHE_KEY.format(tz.localdate().isoformat())
            total_tokens = cache.get(cache_key, 0) + response_json['usage']['total_tokens']
            cache.set(cache_key, total_tokens, timeout=None)

            return response_json['choices'][0]['message']['content']
        except requests.RequestException as exc:
            try:
                message = exc.response.json()
                logger.info(f'OpenAI request failed: {message}')
            except json.JSONDecodeError:
                logger.info(f'OpenAI request failed: {exc}')

        return ''

    def _create_request_body(self, messages) -> dict:
        return {
            'top_p': 0,
            'frequency_penalty': 0,
            'presence_penalty': 0,
            'max_tokens': settings.OPENAI_REQUEST_MAX_TOKENS,
            'temperature': settings.OPENAI_TEMPERATURE,
            'model': settings.OPENAI_MODEL,
            'messages': messages,
        }


@dataclass
class AssistantSpaceX(OpenAI):
    """SpaceX assistant."""

    thread: list[dict]

    def _create_messages(self) -> list[dict]:
        messages = [
            {
                'role': 'system',
                'content': [
                    {
                        'type': 'text',
                        'text': SPACE_X_PROMPT,
                    }
                ],
            }
        ]
        for item in self.thread:
            messages.extend(
                [
                    {
                        'role': item['role'],
                        'content': [{'type': 'text', 'text': clean_string(item['message'])}],
                    },
                ]
            )
        return messages

    def get_next_question(self) -> str:
        messages = self._create_messages()
        return self._request(json=self._create_request_body(messages))


@dataclass
class InsuranceCalculator:
    """Insurance calculator."""

    evaluation: dict

    def _get_psychology_test(self) -> int:
        effective_balance = self.evaluation['positive_affect'] - self.evaluation['negative_affect']
        if effective_balance > 5:
            return 1
        if 0 <= effective_balance <= 5:
            return 2
        return 3

    def _get_physical_test(self) -> int:
        calculator = APFTCalculator(
            gender=self.evaluation['gender'],
            age=self.evaluation['age'],
            pushups=self.evaluation['push-ups'],
            situps=self.evaluation['sit-ups'],
            run=self.evaluation['run'],
        )
        total_score = calculator.calculate_score()

        if total_score > 250:
            return 1
        if 150 <= total_score <= 250:
            return 2
        return 3

    def _get_risk_level(self) -> int:
        apft_score = self._get_physical_test()
        panas_score = self._get_psychology_test()

        return (apft_score + panas_score) // 2

    def get_insurance_value(self) -> tuple[int, str]:
        risk_level = self._get_risk_level()
        risk_level_display = 'High'
        risk_level_display = 'Low' if risk_level == 1 else 'Medium'
        return risk_level, risk_level_display
