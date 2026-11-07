"""Providers never persist prompts or responses."""
import asyncio
import ipaddress
import json
from urllib.parse import urlsplit
import httpx

class MockProvider:
    def __init__(self, text='Quiet Glasses is ready. A little information, only when you ask.', delay=0.02):
        self.text, self.delay = text, delay

    async def stream(self, prompt):
        for word in self.text.split():
            await asyncio.sleep(self.delay)
            yield word + ' '

class LocalProvider:
    """OpenAI-compatible SSE endpoint, restricted to literal loopback addresses."""
    def __init__(self, url='http://127.0.0.1:8080/v1/chat/completions', model='local'):
        parts = urlsplit(url)
        try:
            local = ipaddress.ip_address(parts.hostname).is_loopback
        except ValueError:
            local = False
        if parts.scheme != 'http' or not local or parts.username or parts.password or parts.fragment:
            raise ValueError('Use an http endpoint with a literal loopback IP')
        self.url, self.model = url, model

    async def stream(self, prompt):
        async with httpx.AsyncClient(trust_env=False, follow_redirects=False,
                                     timeout=httpx.Timeout(30, connect=2)) as client:
            async with client.stream('POST', self.url, json={
                'model': self.model, 'stream': True, 'max_tokens': 512,
                'reasoning_effort': 'low',
                'messages': [{'role': 'system', 'content': 'Answer briefly in plain text.'},
                             {'role': 'user', 'content': prompt}]}) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if not line.startswith('data:'): continue
                    data = line[5:].strip()
                    if data == '[DONE]': return
                    chunk = json.loads(data)
                    text = chunk['choices'][0].get('delta', {}).get('content')
                    if text: yield text

                raise RuntimeError('Local stream ended without DONE')


async def choose_provider(mode, endpoint, model):
    if mode == 'mock':
        return MockProvider(), 'MOCK (synthetic response)'
    provider = LocalProvider(endpoint, model)
    if mode == 'local':
        return provider, f'LOCAL {model} at {endpoint}'
    try:
        # A small reachability check only; it does not send any question.
        models_url = endpoint.rsplit('/chat/completions', 1)[0] + '/models'
        async with httpx.AsyncClient(trust_env=False, follow_redirects=False, timeout=2) as client:
            response = await client.get(models_url)
            response.raise_for_status()
            available = {item['id'] for item in response.json()['data']}
            if model not in available:
                raise ValueError('configured model not available')
        return provider, f'LOCAL {model} at {endpoint}'
    except (httpx.HTTPError, ValueError, KeyError):
        return MockProvider(), 'MOCK FALLBACK (local endpoint/model unavailable)'
