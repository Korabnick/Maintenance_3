import json
from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt

def load_data(filepath="data.json"):
    """Загружает данные из JSON-файла."""
    with open(filepath, "r") as file:
        return json.load(file)

def calculate_open_durations(issues):
    """Вычисляет время, проведенное задачей в открытом состоянии."""
    durations = []
    for issue in issues["issues"]:
        created = datetime.strptime(issue["fields"]["created"], "%Y-%m-%dT%H:%M:%S.%f%z")
        updated = datetime.strptime(issue["fields"]["updated"], "%Y-%m-%dT%H:%M:%S.%f%z")
        duration = (updated - created).total_seconds() / 3600  # Время в часах
        durations.append(duration)
    return durations

def calculate_time_in_states(issues):
    """Вычисляет время, проведенное задачами в различных состояниях."""
    state_durations = {}
    
    for issue in issues["issues"]:
        changelog = issue.get("changelog", {}).get("histories", [])
        for i, change in enumerate(changelog):
            if "items" not in change:
                continue
            status_change = next((item for item in change["items"] if item["field"] == "status"), None)
            if not status_change:
                continue
            current_status = status_change["toString"]
            created_time = datetime.strptime(change["created"], "%Y-%m-%dT%H:%M:%S.%f%z")
            next_time = (
                datetime.strptime(changelog[i + 1]["created"], "%Y-%m-%dT%H:%M:%S.%f%z")
                if i + 1 < len(changelog)
                else datetime.strptime(issue["fields"]["resolutiondate"], "%Y-%m-%dT%H:%M:%S.%f%z")
                if issue["fields"]["resolutiondate"]
                else None
            )
            if next_time:
                duration = (next_time - created_time).total_seconds() / 3600
                state_durations[current_status] = state_durations.get(current_status, 0) + duration
    return state_durations

def calculate_daily_stats(issues):
    """Рассчитывает статистику заведенных и закрытых задач по дням."""
    daily_created = defaultdict(int)
    daily_closed = defaultdict(int)

    for issue in issues["issues"]:
        created_date = datetime.strptime(issue["fields"]["created"], "%Y-%m-%dT%H:%M:%S.%f%z").date()
        daily_created[created_date] += 1

        closed_date = issue["fields"].get("resolutiondate")
        if closed_date:
            closed_date = datetime.strptime(closed_date, "%Y-%m-%dT%H:%M:%S.%f%z").date()
            daily_closed[closed_date] += 1

    # Сортируем даты для накопительного итога
    all_dates = sorted(set(daily_created.keys()).union(set(daily_closed.keys())))

    cumulative_created = []
    cumulative_closed = []
    total_created = 0
    total_closed = 0

    for date in all_dates:
        total_created += daily_created[date]
        total_closed += daily_closed[date]
        cumulative_created.append((date, total_created))
        cumulative_closed.append((date, total_closed))

    return daily_created, daily_closed, cumulative_created, cumulative_closed

def calculate_user_activity(issues):
    """Рассчитывает активность пользователей: созданные и закрытые задачи."""
    user_created = defaultdict(int)
    user_closed = defaultdict(int)

    for issue in issues["issues"]:
        reporter = issue["fields"].get("reporter", {}).get("displayName", "Неизвестный пользователь")
        user_created[reporter] += 1

        assignee = issue["fields"].get("assignee")
        if assignee:  # Проверка на None
            assignee_name = assignee.get("displayName", "Неизвестный пользователь")
        else:
            assignee_name = "Неизвестный пользователь"

        resolution_date = issue["fields"].get("resolutiondate")
        if resolution_date:
            user_closed[assignee_name] += 1

    return user_created, user_closed

def calculate_duration_from_creation(issues):
    """Вычисляет длительность выполнения задачи на основе дат создания и закрытия."""
    durations = []

    for issue in issues["issues"]:
        created = issue["fields"].get("created")
        resolution_date = issue["fields"].get("resolutiondate")

        if created and resolution_date:
            created_date = datetime.strptime(created, "%Y-%m-%dT%H:%M:%S.%f%z")
            resolved_date = datetime.strptime(resolution_date, "%Y-%m-%dT%H:%M:%S.%f%z")

            duration_hours = (resolved_date - created_date).total_seconds() / 3600
            durations.append(duration_hours)

    return durations

def calculate_priority_distribution(issues):
    """Рассчитывает распределение задач по приоритетам."""
    priority_counts = defaultdict(int)

    for issue in issues["issues"]:
        priority = issue["fields"].get("priority", {}).get("name", "Не указан")
        priority_counts[priority] += 1

    return priority_counts

def plot_histogram(durations, bins=10):
    """Строит гистограмму времени задач в открытом состоянии."""
    plt.figure(figsize=(10, 6))
    plt.hist(durations, bins=bins, edgecolor="black")
    plt.title("Время задач в открытом состоянии")
    plt.xlabel("Время (часы)")
    plt.ylabel("Количество задач")
    plt.grid(axis="y")
    plt.show()

def plot_state_durations(state_durations):
    """Строит график времени, проведенного задачами в каждом состоянии."""
    states = list(state_durations.keys())
    durations = list(state_durations.values())

    plt.figure(figsize=(10, 6))
    plt.bar(states, durations, color="skyblue", edgecolor="black")
    plt.title("Распределение времени задач по состояниям")
    plt.xlabel("Состояние задачи")
    plt.ylabel("Время (часы)")
    plt.xticks(rotation=45)
    plt.grid(axis="y")
    plt.tight_layout()
    plt.show()

def plot_daily_stats(daily_created, daily_closed, cumulative_created, cumulative_closed):
    """Строит график заведенных и закрытых задач с накопительным итогом."""
    dates_created = sorted(daily_created.keys())
    counts_created = [daily_created[date] for date in dates_created]

    dates_closed = sorted(daily_closed.keys())
    counts_closed = [daily_closed[date] for date in dates_closed]

    cumulative_dates_created, cumulative_counts_created = zip(*cumulative_created)
    cumulative_dates_closed, cumulative_counts_closed = zip(*cumulative_closed)

    plt.figure(figsize=(12, 6))

    # Линии для заведенных и закрытых задач
    plt.plot(dates_created, counts_created, label="Заведенные задачи (в день)", color="blue")
    plt.plot(dates_closed, counts_closed, label="Закрытые задачи (в день)", color="red")

    # Линии для накопительного итога
    plt.plot(cumulative_dates_created, cumulative_counts_created, label="Накопительные заведенные задачи", linestyle="--", color="darkblue")
    plt.plot(cumulative_dates_closed, cumulative_counts_closed, label="Накопительные закрытые задачи", linestyle="--", color="darkred")

    plt.title("Количество заведенных и закрытых задач в день")
    plt.xlabel("Дата")
    plt.ylabel("Количество задач")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_user_activity(user_created, user_closed):
    """Строит график активности пользователей."""
    users = sorted(set(user_created.keys()).union(set(user_closed.keys())))
    created_counts = [user_created[user] for user in users]
    closed_counts = [user_closed[user] for user in users]

    x = range(len(users))

    plt.figure(figsize=(12, 6))
    plt.bar(x, created_counts, label="Созданные задачи", color="blue", alpha=0.7)
    plt.bar(x, closed_counts, label="Закрытые задачи", color="red", alpha=0.7, bottom=created_counts)
    plt.xticks(x, users, rotation=45, ha="right")
    plt.title("Активность пользователей")
    plt.xlabel("Пользователь")
    plt.ylabel("Количество задач")
    plt.legend()
    plt.tight_layout()
    plt.grid(axis="y")
    plt.show()

def plot_logged_time_histogram(logged_times, bins=10):
    """Строит гистограмму времени выполнения задач."""
    plt.figure(figsize=(10, 6))
    plt.hist(logged_times, bins=bins, edgecolor="black", color="lightblue")
    plt.title("Время выполнения задач (залогированное)")
    plt.xlabel("Время выполнения (часы)")
    plt.ylabel("Количество задач")
    plt.grid(axis="y")
    plt.show()

def plot_priority_distribution(priority_counts):
    """Строит график распределения задач по степени серьезности."""
    priorities = list(priority_counts.keys())
    counts = list(priority_counts.values())

    plt.figure(figsize=(10, 6))
    plt.bar(priorities, counts, color="orange", edgecolor="black")
    plt.title("Распределение задач по приоритетам")
    plt.xlabel("Приоритет")
    plt.ylabel("Количество задач")
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    data = load_data()

    durations = calculate_open_durations(data)
    state_durations = calculate_time_in_states(data)
    daily_created, daily_closed, cumulative_created, cumulative_closed = calculate_daily_stats(data)
    user_created, user_closed = calculate_user_activity(data)
    logged_times = calculate_duration_from_creation(data)
    priority_counts = calculate_priority_distribution(data)


    plot_histogram(durations, bins=20)
    plot_state_durations(state_durations)
    plot_daily_stats(daily_created, daily_closed, cumulative_created, cumulative_closed)
    plot_user_activity(user_created, user_closed)
    plot_logged_time_histogram(logged_times, bins=20)
    plot_priority_distribution(priority_counts)
