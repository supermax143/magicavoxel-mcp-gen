# Установка и использование MagicaVoxel MCP Server

## Быстрая установка

1. **Клонируйте репозиторий:**
```bash
git clone <repository-url>
cd magicavoxel-mcp-gen
```

2. **Установите зависимости:**
```bash
pip install -r requirements.txt
```

3. **Запустите тест для проверки:**
```bash
python test_mcp.py
```

## Интеграция с MCP клиентом

Добавьте в конфигурацию вашего MCP клиента (например, в Claude Desktop):

```json
{
  "mcpServers": {
    "magicavoxel-mcp-gen": {
      "command": "python",
      "args": ["server.py"]
    }
  }
}
```

**Важно:** Укажите полный путь к `server.py` если необходимо.

## Доступные функции

### Примитивы
- `create_cube` - Создание куба
- `create_sphere` - Создание сферы  
- `create_cylinder` - Создание цилиндра
- `create_pyramid` - Создание пирамиды

### Визуализация
- `visualize_vox` - Визуализация VOX файла

## Примеры запросов

### Создать красный куб 5x5x5
```json
{
  "tool": "create_cube",
  "arguments": {
    "size": 5,
    "color": [255, 0, 0],
    "filename": "red_cube.vox"
  }
}
```

### Создать зеленую сферу радиусом 3
```json
{
  "tool": "create_sphere", 
  "arguments": {
    "radius": 3,
    "color": [0, 255, 0],
    "filename": "green_sphere.vox"
  }
}
```

### Визуализировать созданный файл
```json
{
  "tool": "visualize_vox",
  "arguments": {
    "filename": "red_cube.vox"
  }
}
```

## Особенности

✅ **Использует MagicaVoxel палитру** - 255 точных цветов  
✅ **Избегает индекса 0** - предотвращает "вырезание" вокселей  
✅ **Автоподбор цветов** - находит ближайший цвет в палитре  
✅ **Визуализация** - встроенная визуализация через midvoxio  
✅ **Тестирование** - полный набор тестов для всех примитивов  

## Структура файлов

```
magicavoxel-mcp-gen/
├── server.py              # MCP сервер
├── test_mcp.py           # Тесты
├── palette_utils.py      # Утилиты палитры
├── magica_palette.json    # MagicaVoxel палитра
├── requirements.txt      # Зависимости
├── README_MCP.md         # Подробная документация
└── mcp_config.json       # Пример конфигурации
```

## Поиск проблем

Если что-то не работает:

1. **Проверьте зависимости:**
```bash
pip install -r requirements.txt
```

2. **Запустите тесты:**
```bash
python test_mcp.py
```

3. **Проверьте наличие палитры:**
```bash
ls magica_palette.json
```

4. **Проверьте путь в конфигурации MCP клиента**

## Поддерживаемые форматы

- **Вход:** JSON параметры через MCP
- **Выход:** VOX файлы (MagicaVoxel формат)
- **Палитра:** 255 цветов MagicaVoxel
- **Визуализация:** midvoxio

## Ограничения

- Максимальный размер примитивов: 64x64x64 вокселей
- Максимальный радиус сферы/цилиндра: 32 вокселя
- Используются только цвета из MagicaVoxel палитры
- Визуализация требует графического окружения
