from typing import List, Optional
import json
from task_viewer import Task


class TaskManager:
    def __init__(self, storage_file: str):
        self.storage_file = storage_file
        self.tasks: List[Task] = []
        self.load_tasks()

    def load_tasks(self):
        try:
            with open(self.storage_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.tasks = [Task.from_dict(task) for task in data]
        except FileNotFoundError:
            self.tasks = []
        except json.JSONDecodeError:
            print("Ошибка чтения файла данных. Начинаем с пустого списка задач.")

    def save_tasks(self):
        with open(self.storage_file, "w", encoding="utf-8") as file:
            json.dump(
                [task.to_dict() for task in self.tasks],
                file,
                indent=4,
                ensure_ascii=False,
            )

    def add_task(
        self, title: str, description: str, category: str, due_date: str, priority: str
    ):
        new_id = max((task.id for task in self.tasks), default=0) + 1
        self.tasks.append(
            Task(new_id, title, description, category, due_date, priority)
        )
        self.save_tasks()

    def edit_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        category: Optional[str] = None,
        due_date: Optional[str] = None,
        priority: Optional[str] = None,
    ):
        task = self.find_task_by_id(task_id)
        if task:
            if title:
                task.title = title
            if description:
                task.description = description
            if category:
                task.category = category
            if due_date:
                task.due_date = due_date
            if priority:
                task.priority = priority
            self.save_tasks()
        else:
            print(f"Задача с ID {task_id} не найдена.")

    def delete_task(
        self, task_id: Optional[int] = None, category: Optional[str] = None
    ):
        if task_id:
            self.tasks = [task for task in self.tasks if task.id != task_id]
        elif category:
            self.tasks = [task for task in self.tasks if task.category != category]
        self.save_tasks()

    def search_tasks(
        self,
        keyword: Optional[str] = None,
        category: Optional[str] = None,
        status: Optional[str] = None,
    ):
        results = self.tasks
        if keyword:
            results = [
                task
                for task in results
                if keyword.lower() in task.title.lower()
                or keyword.lower() in task.description.lower()
            ]
        if category:
            results = [
                task for task in results if task.category.lower() == category.lower()
            ]
        if status:
            results = [
                task for task in results if task.status.lower() == status.lower()
            ]
        return results

    def find_task_by_id(self, task_id: int) -> Optional[Task]:
        return next((task for task in self.tasks if task.id == task_id), None)

    def display_tasks(self, tasks: Optional[List[Task]] = None):
        tasks = tasks or self.tasks
        for task in tasks:
            print(
                f"[{task.id}] {task.title} ({task.category}) - {task.status}\n    "
                f"Описание: {task.description}\n    Дата завершения: {task.due_date}, Приоритет: {task.priority}"
            )
