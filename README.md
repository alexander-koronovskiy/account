# Первоначальные вводные данные 
{
  "org_inn": "string", // ИНН Оганизации
  "bg_type": "int", // Сведения о банковской гарантии
  "order_number": "string", // Реестровый номер торгов
  "auction_type": "int", // Тип аукциона 
  "auction_url": "string", // Ссылка на тенде в интенете
  "auction_date": "YYYY-MM-DD", // Дата тендера
  "auction_goal": "string", // Предмет закупки
  "auction_code": "string", // Идентификационный код закупки
  "guaranty_date": "YYYY-MM-DD", // Дата начала гарантии
  "guaranty_period": "YYYY-MM-DD", // Срок гарантии на исполнение
  "guaranty_amount": "float", // Сумма гарантии 
  "guaranty_amount_release": "float", // Сумма гарантии на исполнение
  "lots": [
    {
      "number": "int", // Номер лота
      "amount": "float" // НМЦК
    }
  ],
}
auction_type:
1 - Открытый
2 - Закрытый

bg_type:
1 - Обеспечение гарантийного периода
2 - Обеспечение заявки на участие в торгах
3 - Обеспечение исполнения обязательств по контракту
4 - Обеспечение на возврат аванса

# БД

Концепция такая что мы не сохраняем данные у себя и они находятся временно в очереди.
Возможно использовать как MySQL так и MongoDB.

### guaranty table

id: unsignedBigInteger
provider: enum (alpha) провайдер один по умолчанию
status: enum 
  - new // Новая в очереди
  - process // В процессе создания 
  - done // Создана
  - error // Ошибка обработки
uuid: string(64)|nullable index // ID заявки в системе провайдеа
link: string(255)|nullable // Ссылка на заявку в системе провайдеа
error_message: String(255)|nullable
created_at: DateTime

### guaranty_jobs

Данная таблица работает как очередь задач

id: unsignedBigInteger
guaranty_id: unsignedBigInteger
data: JSON // Вводные данные для обработки
created_at: DateTime

# Сервис

Сервис должен содержать следующие методы:

## 404 NotFound

Header Status Code : 404

{
  result: False,
  error_message: "NotFound"
}

## Создание заявки на банковскую гарантию

[POST] /api/guaranty/create

Метод принимает JSON с вводными данными, и запускает процесс в очереди с заполнением формы /tasks/?add-task=bg-pa. GUARANTY_TASK.
Метод должен возвращать ID задачи из guaranty.

{
  id: "guaranty.id",
  - OR - 
  error: Bool,
  error_message: ""
}

- Создаем БГ guaranty
- Создаем задачу в очереди guaranty_jobs c присланными данными которые храним в поле data


## Проверка задачи в очереди

[GET] /api/guaranty/get/:id

Метод принимает ID созданной заявки и возващает ответ в зависимости от статуса

### NotFound

Ответ что и в 404 ошибке если заявка с таким ID не найдена.

### Задача в очереди

{
  id: "guaranty.id"
  status: Status(ENUM),
  uuid: "guaranty.uuid" // ID заявки в системе провайдеа
  link: "guaranty.link" // Ссылка на заявку в системе провайдеа
  error_message: ""
  created_at: ""
}

## Очередь

После того как задача попадает в очередь, она поступает в обработку.
Необходимо в фоне (возможно череез Selenuim) заполнить поля /tasks/?add-task=bg-pa. 
Данные для заполнения полей хранятся в поле data в очереди.
По завершении задачи положить в таблицу guaranty полученные link и uuid + обновить статус.
В случае ошибки, заполнить сведения о ней.
Если обработка завершилась успешно без ошибок, удалить задачу guaranty_jobs из очереди задач, иначе пометить guaranty.status = error.