import json
import httpx
import pytest
from quiet_glasses.providers import LocalProvider

async def test_local_sse(monkeypatch):
    seen = []
    def handle(request):
        seen.append(json.loads(request.content))
        return httpx.Response(200, text=': ping\n\ndata: {"choices":[{"delta":{"content":"Hello"}}]}\n\ndata: [DONE]\n\n')
    real_client = httpx.AsyncClient
    monkeypatch.setattr(httpx, 'AsyncClient', lambda **kwargs:
        real_client(transport=httpx.MockTransport(handle), **kwargs))
    assert [t async for t in LocalProvider().stream('test')] == ['Hello']
    assert seen[0]['stream'] is True
    assert seen[0]['messages'][-1]['content'] == 'test'

@pytest.mark.parametrize('status,body', [(500, 'bad'), (200, 'data: broken\n'),
    (302, ''), (200, '')])
async def test_invalid_local_stream(monkeypatch, status, body):
    real_client = httpx.AsyncClient
    monkeypatch.setattr(httpx, 'AsyncClient', lambda **kwargs:
        real_client(transport=httpx.MockTransport(lambda request:
            httpx.Response(status, text=body)), **kwargs))
    with pytest.raises(Exception):
        _ = [t async for t in LocalProvider().stream('test')]

@pytest.mark.parametrize('available', [True, False])
async def test_auto_provider_and_mock_fallback(monkeypatch, available):
    from quiet_glasses.providers import choose_provider, MockProvider
    real_client = httpx.AsyncClient
    monkeypatch.setattr(httpx, 'AsyncClient', lambda **kwargs:
        real_client(transport=httpx.MockTransport(lambda request:
            httpx.Response(200, json={'data': [{'id': 'demo'}] if available else []})), **kwargs))
    provider, label = await choose_provider('auto', 'http://127.0.0.1:11434/v1/chat/completions', 'demo')
    assert isinstance(provider, LocalProvider if available else MockProvider)
    assert ('LOCAL' if available else 'MOCK FALLBACK') in label
