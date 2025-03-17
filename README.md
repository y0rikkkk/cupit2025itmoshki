В данном репозитории вам предлагается решение кейса от команды itmoshki. В корневой директории располагаются следующие файлы 

- ObjectClasses.py  
- filters.py  
- main.py  
- parser.py
- station\_finder.py  
- stations\_list.json

Представленный сервис решает задачу по оптимизации поиска маршрута из точки А в точку Б, учитывая возможности ввода промежуточных точек следования и учитывая предпочтения пользователя по длительности пребывания в точке пересадки. За основу для получения информации взята открытая API Яндекс расписаний. 
API ключ располагается напрямую в файле main.py, дополнительно вводить ничего не нужно.

Для того чтобы воспользоваться данным сервисом необходимо скачать все данные из корневой директории, включая station\_list.json. Поместить скачанные файлы необходимо в одну папку, созданную при инициализации виртуального окружения Python. Если вы хотите создать новое виртуальное окружение, сделать это можно выполнив следующие шаги.

1. Откройте терминал или командную строку  
2. Перейдите в каталог, где вы хотите создать виртуальное окружение  
3. Введите следующую команду:  

~~~
python3 -m venv myenv 
~~~

После того как вы перешли в папку вашей виртуального окружения или инициализировали его необходимо установить необходимые библиотеки. Сделать это можно следующей командой  

~~~
pip install requests 
~~~

Далее необходимо открыть файл main.py и запустить выполнение кода. Необходимо ввести город отправления, далее будет предложено выбрать конкретную точку в городе, повторить операцию и для точки прибытия. Следуйте указаниям появляющимся в вашем терминале.

N.B. файлы, предоставляемые компанией Яндекс неидеальны и не всегда содержат корректные коды локаций, в результате чего может приходить следующая ошибка 
~~~
{'error': {'text': 'Не нашли объект по yandex коду s9868736', 'http\_code': 404, 'error\_code'}
~~~
В таком случае просто попробуйте выбрать соседний пункт на этапе утверждения точной локации.

Механизмы фильтрации включают в себя 
- выбор типов используемого транспорта
- приоритезация прямых маршрутов
- возможность выбора продолжительности пересадки
- возможность найти билеты только нерабочее время
- варианты ранжирования маршрутов, прошедщих фильтрацию:
    - по времени отправления
    - по времени прибытия
    - по продолжительности поездки
 
Желаем вам хорошего дня и приятного использования данного сервиса 

----
**itmoshki team**
- Вербицкий Артемий - тимлид / государь
- Куприянова Арина - продуктовый и проектный менеджер
- Смелик Пелагея - UX/UI дизайнер
- Ишбаев Эрнест - backend разработчик
- Михалевич Максим - DS/ML инженер 

