import httpx
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import ollama

client = TestClient(app)

@pytest.fixture
def upstream(monkeypatch):
    monkeypatch.setenv('OLLAMA_BASE_URL', 'http://ollama.test:11434/')
    for key in ('OLLAMA_DEFAULT_MODEL', 'OLLAMA_CODE_MODEL', 'OLLAMA_REASON_MODEL'):
        monkeypatch.delenv(key, raising=False)
    real_client = httpx.AsyncClient
    calls = []
    state = {'status': 200, 'body': {'message': {'role': 'assistant', 'content': 'Hello'}, 'done': True}}
    def handler(request):
        import json
        calls.append((str(request.url), json.loads(request.content)))
        if 'exception' in state:
            raise state['exception']('failed', request=request)
        if 'raw' in state:
            return httpx.Response(state['status'], content=state['raw'])
        return httpx.Response(state['status'], json=state['body'])
    monkeypatch.setattr(ollama.httpx, 'AsyncClient', lambda **kw: real_client(transport=httpx.MockTransport(handler), **kw))
    return calls, state

def test_health_and_docs():
    assert client.get('/').json() == {'status': 'Adaptive AI Backend Running'}
    assert client.get('/docs').status_code == 200
    assert {'/', '/models/chat', '/commands/run'} <= set(client.get('/openapi.json').json()['paths'])

def test_chat(upstream):
    calls, state = upstream
    response = client.post('/models/chat', json={'model': 'local:test', 'prompt': 'Hi'})
    assert response.status_code == 200
    assert response.json() == state['body']
    assert calls == [('http://ollama.test:11434/api/chat', {'model': 'local:test', 'messages': [{'role': 'user', 'content': 'Hi'}], 'stream': False})]

@pytest.mark.parametrize('command,model', [('Write CODE', 'qwen2.5-coder'), ('create a script', 'qwen2.5-coder'), ('Analyze a lead', 'deepseek-r1'), ('reason about it', 'deepseek-r1'), ('hello', 'llama3.1'), ('analyze code', 'qwen2.5-coder')])
def test_command_routing(upstream, command, model):
    calls, _ = upstream
    response = client.post('/commands/run', json={'command': command, 'context': {'city': 'Austin'}})
    assert response.status_code == 200
    assert response.json()['selected_model'] == model
    assert calls[0][1]['model'] == model
    assert 'Austin' in calls[0][1]['messages'][0]['content']

@pytest.mark.parametrize('command,key', [('hello', 'OLLAMA_DEFAULT_MODEL'), ('code', 'OLLAMA_CODE_MODEL'), ('analyze', 'OLLAMA_REASON_MODEL')])
def test_model_override(upstream, monkeypatch, command, key):
    monkeypatch.setenv(key, 'installed:latest')
    assert client.post('/commands/run', json={'command': command}).json()['selected_model'] == 'installed:latest'

@pytest.mark.parametrize('path,body', [('/models/chat', {'model': '', 'prompt': 'hi'}), ('/models/chat', {'model': 'test', 'prompt': '  '}), ('/commands/run', {'command': '  '}), ('/commands/run', {'command': 'hi', 'context': []})])
def test_invalid_input(path, body):
    assert client.post(path, json=body).status_code == 422

@pytest.mark.parametrize('error,expected', [(httpx.ConnectError, 503), (httpx.ReadTimeout, 504)])
@pytest.mark.parametrize('path,body', [('/models/chat', {'model': 'test', 'prompt': 'hi'}), ('/commands/run', {'command': 'hi'})])
def test_connection_errors(upstream, error, expected, path, body):
    _, state = upstream
    state['exception'] = error
    assert client.post(path, json=body).status_code == expected

@pytest.mark.parametrize('status,body', [(404, {'error': 'missing'}), (500, {'error': 'failure'}), (200, {'error': 'oops'}), (200, []), (200, {'message': {}})])
def test_upstream_errors(upstream, status, body):
    _, state = upstream
    state.update(status=status, body=body)
    assert client.post('/models/chat', json={'model': 'test', 'prompt': 'hi'}).status_code == 502

def test_invalid_json(upstream):
    _, state = upstream
    state['raw'] = b'not json'
    assert client.post('/models/chat', json={'model': 'test', 'prompt': 'hi'}).status_code == 502
