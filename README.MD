# FastAPI Phone Address Service #testtask

Cервис на FastAPI для управления телефонными адресами. Он позволяет записывать новые адреса, обновлять существующие и проверять данные по номеру телефона.

## Установка и запуск

### Зависимости

Перед запуском убедитесь, что у вас установлены следующие компоненты:
- Docker
- Docker Compose

### Шаги

1. Склонируйте репозиторий:

2. Перейдите в директорию проекта:

3. Запустите приложение с помощью Docker Compose:
```bash
  docker-compose up --build


После выполнения этих шагов, ваше приложение будет доступно по localhost:80.


API предоставляет следующие конечные точки:
```
- **POST /write_data**: Запись нового адреса по номеру телефона.
- **PATCH /write_data**: Обновление адреса по номеру телефона.
- **GET /check_data**: Получение адреса по номеру телефона.


Пример использования:
```bash
  curl -X POST -H "Content-Type: application/json" -d '{"phone": "1234567890", "address": "address123"}' http://localhost/write_data
```

## Дополнительная информация

- В директории `tests` находятся модульные и интеграционные тесты для проверки функциональности.
- Файл `docker-compose.yml` содержит описание сервисов, необходимых для запуска проекта.
- Для настройки Nginx используется файл `nginx.conf`.


#### Ответ на задание 2

```bash
WITH temp_names AS (
    SELECT
        fn.name AS full_name,
        sn.name AS short_name,
        sn.status AS short_status
    FROM
        full_names fn
    JOIN
        short_names sn ON sn.name = split_part(fn.name, '.', 1)
)
UPDATE full_names fn
SET status = tn.short_status
FROM temp_names tn
WHERE fn.name = tn.full_name;


UPDATE full_names fn
SET status = (
    SELECT sn.status
    FROM short_names sn
    WHERE sn.name = split_part(fn.name, '.', 1)
)
WHERE EXISTS (
    SELECT 1
    FROM short_names sn
    WHERE sn.name = split_part(fn.name, '.', 1)
);

Предпочтительней будет вариан с использованием временной таблицы (CTE)
Количество запросов к базе данных будет меньше, так как CTE позволяет организовать запрос в виде логических блоков, избегая множественных подзапросов.
