# Bank System (Копанов Антон Б05-223)

Bank System это мой проект по предмету технологии программирования, симулирующий банковскую
систему.

## Необходимое для запуска

Для запуска проекта необходим python версии не ниже 3.11 и Graphviz.

## Установка

После установки репозитория себе запустите файл setup.py в корневой папке проекта, он установит
необходимые библиотеки и
создаст UML по проекту(для того чтобы создать UML, может понадобиться установить Graphviz вручную,
в этом случае скрипт
выдаст ошибку). После того как скрипт setup.py завершил свою работу нужно запустить файл
src/python_code/main.py.

## Использование

Клиент заходит на главную и может зарегистрироваться или войти. При регистрации у него спрашивают
имя и фамилию, адрес и
паспорт. При входе спрашивается только имя и фамилия. После входа клиент может увидеть свои счета,
создать новый счёт,
совершить транзакцию или выйти.
При создании счета нужно выбрать тип счёта и данные для этого счета. Для транзакции нужно выбрать
тип и сумму.

## Архитектура и паттерны

Для создания клиента используется паттерн Builder(ветку его наследников можно посмотреть на
диаграмме классов). Для
создания счетов используется Factory Method(AccountCreator и Account и их наследники). Для работы с
данными используется
Adapter(DataAdapter). При работе с пользователем используется класс SessionFacade, у которого есть
классы-ассистенты(например, TransactionAssistant). Данные пользователей хранятся в data/data.json.

## UML

UML диаграмма классов расположена в папке uml/classes.puml. Use-case диаграмма находится в папке
uml/use-case.
