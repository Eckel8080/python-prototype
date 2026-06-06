from collections.abc import Generator

import pytest

import my_project.users.services as user_module
from my_project.users.services import USERS_DB


@pytest.fixture(scope="function", autouse=True)
def clean_db() -> Generator[None, None, None]:
    """每次测试前清空模拟内存数据库，并重置计数器。"""
    USERS_DB.clear()
    user_module._id_counter = 0
    yield
