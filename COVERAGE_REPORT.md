# Coverage Report

## Текущее покрытие кода: 96%

### Файлы и их покрытие:
- `src/__init__.py`: 100%
- `src/models.py`: 96% (пропущены строки 85-88 - интерактивный ввод цены)

### Требования:
- ✅ Требуемое покрытие: >75%
- ✅ Фактическое покрытие: 96%

### Отчеты:
- HTML отчет: `htmlcov/index.html`
- XML отчет: `coverage.xml`
- Терминальный отчет: доступен через `poetry run pytest --cov=src --cov-report=term`

### Команда для проверки покрытия:
```bash
poetry run pytest tests/tests_models.py --cov=src --cov-report=term-missing
```

### Результат выполнения команды:
```
---------- coverage: platform win32, python 3.13.5-final-0 -----------
Name              Stmts   Miss  Cover   Missing
-----------------------------------------------
src\__init__.py       0      0   100%
src\models.py       110      4    96%   85-88
-----------------------------------------------
TOTAL               110      4    96%
```

**Вывод:** Требование по покрытию кода тестами (>75%) выполнено.
