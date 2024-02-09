import pytest
import time

@pytest.fixture(autouse=True, scope='session')
def footer_session_scope():
    """Сообщает время в конце session(сеанса)."""
    yield
    now = time.time()
    print('--')
    print('finished : {}'.format(time.strftime('%d %b %X', time.localtime(now))))
    print('-----------------')