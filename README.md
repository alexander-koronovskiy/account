# Первоначальные вводные данные 

```json
{
  "org_inn": "string", 
  "bg_type": "int", 
  "order_number": "string", 
  "auction_type": "int", 
  "auction_url": "string", 
  "auction_date": "YYYY-MM-DD",
  "auction_goal": "string",
  "auction_code": "string", 
  "guaranty_date": "YYYY-MM-DD", 
  "guaranty_period": "YYYY-MM-DD", 
  "guaranty_amount": "float",
  "guaranty_amount_release": "float",
  "lots": [
    {
      "number": "int",
      "amount": "float" 
    }
  ]
}
```

<table>
    <thead>
        <tr>
            <td><b>Название</b></td>
            <td><b>Описание</b></td>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><b>org_inn</b></td>
            <td>ИНН Организации</td>
        </tr>
        <tr>
            <td><b>bg_type</b></td>
            <td>Сведения о банковской гарантии</td>
        </tr>
        <tr>
            <td><b>order_number</b></td>
            <td>Реестровый номер торгов</td>
        </tr>
        <tr>
            <td><b>auction_type</b></td>
            <td>Тип аукциона</td>
        </tr>
        <tr>
            <td><b>auction_url</b></td>
            <td>Ссылка на тендер в интернете</td>
        </tr>
        <tr>
            <td><b>auction_date</b></td>
            <td>Дата тендера</td>
        </tr>
        <tr>
            <td><b>auction_goal</b></td>
            <td>Предмет закупки</td>
        </tr>
        <tr>
            <td><b>auction_code</b></td>
            <td>Идентификационный код закупки</td>
        </tr>
        <tr>
            <td><b>guaranty_date</b></td>
            <td>Дата начала гарантии</td>
        </tr>
        <tr>
            <td><b>guaranty_period</b></td>
            <td>Срок гарантии на исполнение</td>
        </tr>
        <tr>
            <td><b>guaranty_amount</b></td>
            <td>Сумма гарантии</td>
        </tr>
        <tr>
            <td><b>guaranty_amount_realise</b></td>
            <td>Сумма гарантии на исполнение</td>
        </tr>
        <tr>
            <td><b>lots</b></td>
            <td>Содержащаяся о лоте информация</td>
        </tr>
        <tr>
            <td><b>number</b></td>
            <td>Номер лота</td>
        </tr>
        <tr>
            <td><b>amount</b></td>
            <td>НМЦК</td>
        </tr>
    </tbody>
</table>

> Дополнительно

auction_type:

1 - Открытый

2 - Закрытый


bg_type:

1 - Обеспечение гарантийного периода

2 - Обеспечение заявки на участие в торгах

3 - Обеспечение исполнения обязательств по контракту

4 - Обеспечение на возврат аванса

# БД

Концепция такая что ДАННЫЕ НЕ СОХРАНЯЮТСЯ 
и они находятся временно в очереди.
В качестве базы данных будет использоваться MONGO_DB.

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

> Успешный ответ 

{
  id: "guaranty.id"
}

> В случае возникновения ошибки сервис возвращает ответ

{
  error: Bool,
  error_message: ""
}

Метод сервиса 
- Создает БГ guaranty
- Создает задачу в очереди guaranty_jobs c присланными данными, 
которые храним в поле data


## Проверка задачи в очереди

[GET] /api/guaranty/get/<id>

Метод принимает ID созданной заявки и возвращает ответ 
в зависимости от статуса

> Успешный ответ 


В случае возникновения ошибки метод возвращает ошибку 404

### Представление задачи в очереди

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

В фоне (с помощью Selenuim) заполняются поля /tasks/?add-task=bg-pa. 

Данные для заполнения полей хранятся в поле data в очереди.

По завершении задачи помещается в таблицу guaranty
полученные link и uuid + обновляется статус.

В случае ошибки, заполняются сведения о ней.

Если обработка завершилась успешно без ошибок, 
задача guaranty_jobs удаляется из очереди задач, 
иначе пометить guaranty.status = error.
