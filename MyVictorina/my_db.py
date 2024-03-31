import sqlite3

db_name = 'quiz.db'

def open(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    return conn, cursor

def close(conn, cursor):
    cursor.close()
    conn.close()

def do(conn, cursor, query):
    cursor.execute(query)
    conn.commit()

def create():
    create_quiz = '''CREATE TABLE IF NOT EXISTS quiz (
        id INTEGER PRIMARY KEY,
        name VARCHAR(50)
    )'''
    create_question = '''CREATE TABLE IF NOT EXISTS question (
        id INTEGER PRIMARY KEY,
        question VARCHAR(200),
        answer VARCHAR(50),
        wrong1 VARCHAR(50), 
        wrong2 VARCHAR(50), 
        wrong3 VARCHAR(50)
    )'''
    create_content = '''CREATE TABLE IF NOT EXISTS quiz_content (
        id INTEGER PRIMARY KEY,
        quiz_id INTEGER,
        question_id INTEGER,
        FOREIGN KEY (quiz_id) REFERENCES quiz (id),
        FOREIGN KEY (question_id) REFERENCES question (id)
    )'''

    conn, cursor = open(db_name)
    cursor.execute('''PRAGMA foreign_keys=on''')
    do(conn, cursor, create_quiz)
    do(conn, cursor, create_question)
    do(conn, cursor, create_content)
    close(conn, cursor)

def clear_db():
    conn, cursor = open(db_name)
    query = 'DROP TABLE IF EXISTS quiz_content'
    do(conn, cursor, query)
    query = 'DROP TABLE IF EXISTS quiz'
    do(conn, cursor, query)
    query = 'DROP TABLE IF EXISTS question'
    do(conn, cursor, query)
    close(conn, cursor)

def show(table):
    query = 'SELECT * FROM ' + table
    conn, cursor = open(db_name)
    cursor.execute(query)
    print(table, cursor.fetchall())
    close(conn, cursor)

def show_tables():
    show('question')
    show('quiz')
    show('quiz_content')

def add_questions():
    questions = [
        ('Сколько месяцев в году имеют 28 дней?', 'Все', 'Один', 'Ни одного', 'Два'),
        ('Каким станет зеленый утес, если упадет в Красное море?', 'Мокрым?', 'Красным', 'Не изменится', 'Фиолетовым'),
        ('Какой рукой лучше размешивать чай?', 'Ложкой', 'Правой', 'Левой', 'Любой'),
        ('Что не имеет длины, глубины, ширины, высоты, а можно измерить?', 'Время', 'Глупость', 'Море', 'Воздух'),
        ('Когда сетью можно вытянуть воду?', 'Когда вода замерзла', 'Когда нет рыбы', 'Когда уплыла золотая рыбка', 'Когда сеть порвалась'),
        ('Что больше слона и ничего не весит?', 'Тень слона', 'Воздушный шар', 'Парашют', 'Облако'),
        ('Что такое у меня в кармашке?', 'Кольцо', 'Кулак', 'Дырка', 'Бублик'),
        ('Что следует за ночью?', 'День', 'Ночь', 'Бабайка', 'Четыре')
    ]
    conn, cursor = open(db_name)
    cursor.executemany('''INSERT INTO question (question, answer, wrong1, wrong2, wrong3)
                       VALUES (?,?,?,?,?)''', questions)
    conn.commit()
    close(conn, cursor)

def add_quiz():
    quizes = [
        ('Викторина 1', ),
        ('Викторина 2', ),
        ('Викторина-непоймикакая', )
    ]
    conn, cursor = open(db_name)
    cursor.executemany('''INSERT INTO quiz (name) VALUES (?)''', quizes)
    conn.commit()
    close(conn, cursor)

def add_links():
    conn, cursor = open(db_name)
    cursor.execute('''PRAGMA foreign_keys=on''')
    query = "INSERT INTO quiz_content (quiz_id, question_id) VALUES (?,?)"
    answer = input("Добавить связь (y / n)?")
    while answer != 'n':
        quiz_id = int(input("id викторины: "))
        question_id = int(input("id вопроса: "))
        cursor.execute(query, [quiz_id, question_id])
        conn.commit()
        answer = input("Добавить связь (y / n)?")
    close(conn, cursor)


def get_quises():
    ''' возвращает список викторин (id, name) 
    можно брать только викторины, в которых есть вопросы, но пока простой вариант '''
    query = 'SELECT * FROM quiz ORDER BY id'
    conn, cursor = open(db_name)
    cursor.execute(query)
    result = cursor.fetchall()
    close(conn, cursor)
    return result


def check_answer(q_id, ans_text):
    query = '''
            SELECT question.answer 
            FROM quiz_content, question 
            WHERE quiz_content.id = ? 
            AND quiz_content.question_id = question.id
        '''
    conn, cursor = open(db_name)
    cursor.execute(query, [str(q_id)])
    result = cursor.fetchone()
    close(conn, cursor)    
    # print(result)
    if result is None:
        return False # не нашли
    else:
        if result[0] == ans_text:
            # print(ans_text)
            return True # ответ совпал
        else:
            return False # нашли, но ответ не совпал


def get_question_after(last_id=0, vict_id=1):
    ''' возвращает следующий вопрос после вопроса с переданным id
    для первого вопроса передается значение по умолчанию '''
    conn, cursor = open(db_name)
    query = '''
    SELECT quiz_content.id, question.question, question.answer, question.wrong1, question.wrong2, question.wrong3
    FROM question, quiz_content 
    WHERE quiz_content.question_id == question.id
    AND quiz_content.id > ? AND quiz_content.quiz_id == ? 
    ORDER BY quiz_content.id '''
    cursor.execute(query, [last_id, vict_id] )

    result = cursor.fetchone()
    close(conn, cursor)
    return result 


# clear_db()
# create()
# add_questions()
# add_quiz()
# add_links()
# show_tables()

