# %%
#main
def create_schedule_html(schedule_data):
    html = """<!DOCTYPE html>
    <html lang="ru">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=0.5">
    <title>Расписание занятий</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: Arial, sans-serif;
            height: 100vh;
            overflow: hidden;
            background: white;
        }
        
        .schedule-container {
            width: 100vw;
            height: 100vh;
            overflow: auto;
            position: relative;
        }
        
        table {
            border-collapse: separate;
            border-spacing: 0;
            width: max-content;
            min-width: 100%;
        }
        
        th, td {
            padding: 8px;
            text-align: center;
            vertical-align: middle;
        }
        
        /* Заголовки шапки - перекрывают всё */
        .header-overlay {
            background-color: #e8f4f8;
            font-weight: bold;
            position: sticky;
            top: 0;
            z-index: 100; /* Самый высокий z-index */
            height: 40px;
            white-space: nowrap;
            border-bottom: 2px solid #ccc;
            min-width: 200px;
            border: 1px solid #ddd;
            border-right: 1px solid #000;
            border-left: 1px solid #000;
            border-bottom: 2px solid #000;
        }
        
        /* Специальные заголовки для первых двух колонок */
        .day-header-overlay {
            position: sticky;
            top: 0;
            left: 0;
            z-index: 110; /* Выше чем обычные фиксированные колонки */
            background-color: #e8f4f8;
            font-weight: bold;
            width: 40px;
            min-width: 40px;
            max-width: 40px;
            border-bottom: 2px solid #000;
        }
        
        .time-header-overlay {
            position: sticky;
            top: 0;
            left: 40px;
            z-index: 110; /* Выше чем обычные фиксированные колонки */
            background-color: #e8f4f8;
            font-weight: bold;
            width: 45px;
            min-width: 45px;
            max-width: 45px;
            border-right: 2px solid #000;
            border-bottom: 2px solid #ccc;
        }
        
        /* Дни недели - фиксированные */
        .day-header {
            background-color: #f0f8f0;
            font-weight: bold;
            position: sticky;
            left: 0;
            z-index: 50;


            width: 40px;
            min-width: 40px;
            max-width: 40px;
            padding: 15px 4px;
            border: 1px solid #ddd;
            border-right: 2px solid #999;
        }

        .box_rotate {
            -webkit-transform: rotate(-90deg); /* Для Safari */
            -ms-transform: rotate(-90deg);     /* Для IE 9 */
            transform: rotate(-90deg);         /* Для прочих браузеров */
        }
        
        /* Номера пар - фиксированные */
        .time-slot {
            background-color: #f9f9f9;
            position: sticky;
            left: 40px;
            z-index: 50;
            width: 45px;
            min-width: 45px;
            max-width: 45px;
            font-weight: bold;
            border: 1px solid #ddd;
            border-right: 2px solid #000;
        }
        
        /* Основные ячейки с занятиями */
        .lesson-cell {
            text-align: center;
            vertical-align: middle;
            min-width: 200px;
            max-width: 300px;
            font-size: 14px;
            line-height: 1.3;
            padding: 10px;
            border: 1px solid #ddd;
            border-right: 1px solid #000;
            border-left: 1px solid #000;
            position: relative;
            z-index: 10;
        }
        
        /* отделение одного дня от другого*/
        .day-separartor{
            border-bottom: 10px solid #000;
        }

        .empty-slot {
            background-color: #f5f5f5;
            color: #999;
            font-style: italic;
        }
        
        /* Контейнер для многострочного текста */
        .lesson-content {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            min-height: 60px;
        }
        
        /* Многострочный текст */
        .multiline-text {
            white-space: pre-line;
            text-align: center;
        }
        
        /* Скрытые ячейки для выравнивания */
        .hidden-cell {
            visibility: hidden;
            border: none !important;
            padding: 0 !important;
            height: 0 !important;
        }
    </style>
</head>
<body>
    <div class="schedule-container">
        <table>
            <thead>
                <tr>
                    <th class="day-header-overlay"></th>
                    <th class="time-header-overlay"></th>"""
    
    # Добавляем заголовки групп
    groups = list(schedule_data.keys())
    for group in groups:
        html += f'<th class="header-overlay">{group.upper()}</th>'

    html += """
                </tr>
            </thead>
            <tbody>"""

    # Дни недели в правильном порядке
    days_order = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    days_russian = {
        'monday': 'Понедельник',
        'tuesday': 'Вторник',
        'wednesday': 'Среда',
        'thursday': 'Четверг',
        'friday': 'Пятница',
        'saturday': 'Суббота'
    }

    # Создаем строки таблицы
    for day in days_order:
        # Находим максимальное количество пар в этот день среди всех групп
        max_pairs = 0
        for group in groups:
            if day in schedule_data[group]:
                pairs = schedule_data[group][day]
                # Считаем все пары, включая пустые
                max_pairs = max(max_pairs, len(pairs))
        
        if max_pairs > 0:
            # Добавляем пары для этого дня
            for pair_num in range(max_pairs - 1):
                html += '<tr>'
                
                # Первая ячейка - день недели (только для первой пары)
                if pair_num == 0:
                    html += f'<td class="day-header day-separartor" rowspan="{max_pairs}"> <div class="box_rotate">{days_russian[day]}</div></td>'

                # Вторая ячейка - номер пары
                html += f'<td class="time-slot">{pair_num + 1}</td>'
                
                # Данные для каждой группы
                for group in groups:
                    if day in schedule_data[group] and pair_num < len(schedule_data[group][day]):
                        lesson = schedule_data[group][day][pair_num]
                        if lesson == 'None':
                            html += '<td class="empty-slot lesson-cell">-</td>'
                        else:
                            lesson_html = lesson.replace('\n', '<br>')
                            html += f'<td class="lesson-cell"><div class="lesson-content"><span class="multiline-text">{lesson_html}</span></div></td>'
                    else:
                        html += '<td class="empty-slot lesson-cell">-</td>'
                
                html += '</tr>'
            # шатал я этот ваш DRY
            ########################################
            pair_num = max_pairs - 1
            html += '<tr>'
                
            html += f'<td class="time-slot day-separartor">{pair_num + 1}</td>'
                
            # Данные для каждой группы
            for group in groups:
                if day in schedule_data[group] and pair_num < len(schedule_data[group][day]):
                    lesson = schedule_data[group][day][pair_num]
                    if lesson == 'None':
                        html += '<td class="empty-slot lesson-cell day-separartor">-</td>'
                    else:
                        lesson_html = lesson.replace('\n', '<br>')
                        html += f'<td class="lesson-cell day-separartor"><div class="lesson-content"><span class="multiline-text">{lesson_html}</span></div></td>'
                else:
                    html += '<td class="empty-slot lesson-cell day-separartor"">-</td>'
            
            html += '</tr>'
            ########################################

    html += """
            </tbody>
        </table>
    </div>
</body>
</html>"""
    
    return html

# # Создаем HTML
# html_content = create_schedule_html(schedule)

# # Сохраняем в файл
# with open('schedule.html', 'w', encoding='utf-8') as f:
#     f.write(html_content)

# print("HTML файл успешно создан: schedule.html")