import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from process_data import (
    calculate_open_durations,
    calculate_time_in_states,
    calculate_daily_stats,
    calculate_user_activity,
    calculate_priority_distribution,
)

# Пример данных задач
mock_issues = {
    "issues": [
        {
            "fields": {
                "created": "2024-01-01T12:00:00.000+0000",
                "updated": "2024-01-02T12:00:00.000+0000",
                "priority": {"name": "High"},
                "reporter": {"displayName": "User1"},
                "assignee": {"displayName": "User2"},
                "resolutiondate": "2024-01-02T14:00:00.000+0000",
            },
            "changelog": {
                "histories": [
                    {
                        "created": "2024-01-01T18:00:00.000+0000",
                        "items": [{"field": "status", "toString": "In Progress"}],
                    },
                    {
                        "created": "2024-01-02T10:00:00.000+0000",
                        "items": [{"field": "status", "toString": "Done"}],
                    },
                ]
            },
        },
        {
            "fields": {
                "created": "2024-01-03T08:00:00.000+0000",
                "updated": "2024-01-03T20:00:00.000+0000",
                "priority": {"name": "Medium"},
                "reporter": {"displayName": "User3"},
                "assignee": {"displayName": "User4"},
                "resolutiondate": None,  # Задача не завершена
            },
            "changelog": {"histories": []},
        },
    ]
}

# Тест 1: Проверка вычисления времени в открытом состоянии
def test_calculate_open_durations():
    durations = calculate_open_durations(mock_issues)
    assert len(durations) == 2
    assert durations[0] == 24.0  # Первая задача: 24 часа
    assert durations[1] == 12.0  # Вторая задача: 12 часов

# Тест 2: Проверка вычисления времени по состояниям
def test_calculate_time_in_states():
    state_durations = calculate_time_in_states(mock_issues)
    assert "In Progress" in state_durations
    assert "Done" in state_durations
    assert state_durations["In Progress"] == 16.0  # Время в "In Progress"
    assert state_durations["Done"] == 4.0         # Время в "Done"

# Тест 3: Проверка статистики по дням
def test_calculate_daily_stats():
    daily_created, daily_closed, cumulative_created, cumulative_closed = calculate_daily_stats(mock_issues)
    assert daily_created[datetime(2024, 1, 1).date()] == 1
    assert daily_closed[datetime(2024, 1, 2).date()] == 1
    assert cumulative_created[-1][1] == 2  # Накопительный итог созданных задач
    assert cumulative_closed[-1][1] == 1  # Накопительный итог закрытых задач

# Тест 4: Проверка активности пользователей
def test_calculate_user_activity():
    user_created, user_closed = calculate_user_activity(mock_issues)
    assert user_created["User1"] == 1
    assert user_created["User3"] == 1
    assert user_closed["User2"] == 1  # User2 закрывал задачи
    assert user_closed["User4"] == 0  # User4 не закрывал задачи

# Тест 5: Проверка распределения по приоритетам
def test_calculate_priority_distribution():
    priority_distribution = calculate_priority_distribution(mock_issues)
    assert priority_distribution["High"] == 1
    assert priority_distribution["Medium"] == 1
    assert priority_distribution["Low"] == 0
