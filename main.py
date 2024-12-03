from task_manager import TaskManager

def main():
    manager = TaskManager("tasks.json")

    while True:
        print("\nМенеджер задач")
        print("1. Просмотр всех задач")
        print("2. Добавить задачу")
        print("3. Редактировать задачу")
        print("4. Отметить задачу выполненной")
        print("5. Удалить задачу")
        print("6. Поиск задач")
        print("7. Выход")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            manager.display_tasks()
        elif choice == "2":
            title = input("Название: ")
            description = input("Описание: ")
            category = input("Категория: ")
            due_date = input("Срок выполнения (ГГГГ-ММ-ДД): ")
            priority = input("Приоритет (низкий, средний, высокий): ")
            manager.add_task(title, description, category, due_date, priority)
        elif choice == "3":
            task_id = int(input("ID задачи: "))
            print("Оставьте поля пустыми, если хотите оставить их без изменений.")
            title = input("Новое название: ")
            description = input("Новое описание: ")
            category = input("Новая категория: ")
            due_date = input("Новый срок выполнения (ГГГГ-ММ-ДД): ")
            priority = input("Новый приоритет (низкий, средний, высокий): ")
            manager.edit_task(task_id, title, description, category, due_date, priority)
        elif choice == "4":
            task_id = int(input("ID задачи: "))
            task = manager.find_task_by_id(task_id)
            if task:
                task.mark_as_done()
                manager.save_tasks()
            else:
                print(f"Задача с ID {task_id} не найдена.")
        elif choice == "5":
            task_id = input(
                "Введите ID задачи (или оставьте пустым для удаления по категории): "
            )
            category = None
            if not task_id:
                category = input("Введите категорию: ")
                manager.delete_task(category=category)
            else:
                manager.delete_task(task_id=int(task_id))
        elif choice == "6":
            keyword = input("Ключевое слово: ")
            category = input("Категория: ")
            status = input("Статус (выполнена/не выполнена): ")
            results = manager.search_tasks(keyword, category, status)
            manager.display_tasks(results)
        elif choice == "7":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
