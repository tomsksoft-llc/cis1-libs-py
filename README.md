# ci-py-lib
CI Python utilities library for CI purpose

Эта библиотека содержит набор Python утилит, предназначенных для использования в системах Continuous Integration.
Каждая утилита - находится в отдельном файле и предназначена для выполнения конкретных задач.
Утилита может быть запущена из командной строки как команда ОС, или использована как подключаемый файл к Python программе.
Документация на утилиту находится внутри нее, и может быть получена как в командной строке, так и с помощью Pydoc.

Полная документация на библиотеку автоматически формируется в момент сборки.

Каждая утилита тестируется в момент сборки с помощью тестовых скриптов, которые находятся в данном репозитарии, но частью самих утилит не являются.

Библиотека поддерживает обратную совместимость как минимум внутри мажорной версии.

Библиотека является кросплафторменной.

Инструкция для разработчиков библиотеки находится в файле [docs/devguide.md](docs/devguide.md) данного репозитария.
