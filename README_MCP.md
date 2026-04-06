# MagicaVoxel MCP Server

MCP сервер для генерации воксельных моделей из примитивов с использованием pyvox и MagicaVoxel палитры.

## Установка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Убедитесь, что файл `magica_palette.json` находится в корневой директории проекта.

## Запуск сервера

```bash
python server.py
```

## Доступные инструменты

### create_cube
Создает воксельный куб.

**Параметры:**
- `size` (integer): Размер куба (1-64)
- `color` (array): RGB цвет [r, g, b] (0-255)
- `position` (array, опционально): Позиция [x, y, z] (по умолчанию [0, 0, 0])
- `filename` (string, опционально): Имя файла (по умолчанию "cube.vox")

**Пример:**
```json
{
  "size": 5,
  "color": [255, 0, 0],
  "position": [0, 0, 0],
  "filename": "red_cube.vox"
}
```

### create_sphere
Создает воксельную сферу.

**Параметры:**
- `radius` (integer): Радиус сферы (1-32)
- `color` (array): RGB цвет [r, g, b] (0-255)
- `position` (array, опционально): Позиция [x, y, z] (по умолчанию [0, 0, 0])
- `filename` (string, опционально): Имя файла (по умолчанию "sphere.vox")

**Пример:**
```json
{
  "radius": 3,
  "color": [0, 255, 0],
  "filename": "green_sphere.vox"
}
```

### create_cylinder
Создает воксельный цилиндр.

**Параметры:**
- `radius` (integer): Радиус цилиндра (1-32)
- `height` (integer): Высота цилиндра (1-64)
- `color` (array): RGB цвет [r, g, b] (0-255)
- `position` (array, опционально): Позиция [x, y, z] (по умолчанию [0, 0, 0])
- `filename` (string, опционально): Имя файла (по умолчанию "cylinder.vox")

**Пример:**
```json
{
  "radius": 4,
  "height": 8,
  "color": [0, 0, 255],
  "filename": "blue_cylinder.vox"
}
```

### create_pyramid
Создает воксельную пирамиду.

**Параметры:**
- `base_size` (integer): Размер основания пирамиды (1-64)
- `height` (integer): Высота пирамиды (1-64)
- `color` (array): RGB цвет [r, g, b] (0-255)
- `position` (array, опционально): Позиция [x, y, z] (по умолчанию [0, 0, 0])
- `filename` (string, опционально): Имя файла (по умолчанию "pyramid.vox")

**Пример:**
```json
{
  "base_size": 6,
  "height": 4,
  "color": [255, 255, 0],
  "filename": "yellow_pyramid.vox"
}
```

### visualize_vox
Визуализирует VOX файл.

**Параметры:**
- `filename` (string): Путь к VOX файлу

**Пример:**
```json
{
  "filename": "red_cube.vox"
}
```

## Интеграция с MCP клиентом

Добавьте сервер в конфигурацию MCP клиента:

```json
{
  "mcpServers": {
    "magicavoxel-mcp-gen": {
      "command": "python",
      "args": ["path/to/magicavoxel-mcp-gen/server.py"],
      "cwd": "path/to/magicavoxel-mcp-gen"
    }
  }
}
```

## Особенности

- Использует извлеченную палитру MagicaVoxel для точного соответствия цветов
- Избегает индекса 0 (пустые воксели) для предотвращения "вырезания" модели
- Автоматически подбирает ближайший цвет из палитры MagicaVoxel
- Поддерживает визуализацию созданных моделей через midvoxio

## Примеры использования

### Создание красного куба 5x5x5
```python
# Через MCP клиент
create_cube({
  "size": 5,
  "color": [255, 0, 0],
  "filename": "red_cube.vox"
})
```

### Создание зеленой сферы с радиусом 3
```python
# Через MCP клиент
create_sphere({
  "radius": 3,
  "color": [0, 255, 0],
  "filename": "green_sphere.vox"
})
```

### Визуализация созданной модели
```python
# Через MCP клиент
visualize_vox({
  "filename": "red_cube.vox"
})
```

## Структура проекта

```
magicavoxel-mcp-gen/
├── server.py              # Основной MCP сервер
├── palette_utils.py       # Утилиты для работы с палитрой
├── magica_palette.json    # Извлеченная палитра MagicaVoxel
├── requirements.txt       # Зависимости Python
├── README_MCP.md         # Документация MCP сервера
└── Pallet/               # Оригинальные файлы палитры
    └── pallet.png
```

## Зависимости

- `pyvox`: Создание VOX файлов
- `midvoxio`: Визуализация VOX файлов
- `mcp`: MCP фреймворк
- `numpy`: Математические операции
- `Pillow`: Обработка изображений
- `matplotlib`: Дополнительная визуализация
