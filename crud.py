from sqlalchemy.orm import Session
from models import Yarn
from sqlalchemy import text

# Функция для создания таблиц в базе данных
def create_tables(engine):
    from models import Base
    Base.metadata.create_all(engine)

# Функция для добавления новой записи (ниток)
def add_yarn(session: Session, brand, name, country, color, quantity):
    new_yarn = Yarn(brand=brand, name=name, country=country, color=color, quantity=quantity)
    session.add(new_yarn)
    session.commit()
    print(f"Пряжа {name} успешно добавлена!")

# Функция для отображения всех ниток
def show_yarns(session: Session):
    return session.query(Yarn).all()

# Функция для удаления ниток по ID
def delete_yarn(session: Session, yarn_id):
    yarn = session.query(Yarn).get(yarn_id)
    if yarn:
        session.delete(yarn)
        session.commit()
        print(f"Пряжа с ID {yarn_id} удалена.")

def delete_all_yarns(session: Session):
    try:
        # Удаляем все записи из таблицы Yarn
        session.query(Yarn).delete()
        session.commit()
        # Сбрасываем последовательность для столбца id
        session.execute(text("ALTER SEQUENCE yarns_id_seq RESTART WITH 1"))
        session.commit()
        print("Вся пряжа успешно удалена.")
    except Exception as e:
        print(f"Ошибка при удалении всей пряжи: {e}")
        session.rollback()

# Функция для обновления ниток
def update_yarn(session: Session, yarn_id, brand, name, country, color, quantity):
    yarn = session.query(Yarn).get(yarn_id)
    if yarn:
        yarn.brand = brand
        yarn.name = name
        yarn.country = country
        yarn.color = color
        yarn.quantity = quantity
        session.commit()
        print(f"Пряжа с ID {yarn_id} успешно обновлена.")

# Функции для фильтрации и сортировки
def filter_yarns_by_brand(session: Session, brand):
    return session.query(Yarn).filter(Yarn.brand == brand).all()

def sort_yarns_by_quantity(session: Session, order: str):
    if order == '1':
        return session.query(Yarn).order_by(Yarn.quantity.asc()).all()
    else:  # 'desc'
        return session.query(Yarn).order_by(Yarn.quantity.desc()).all()

def sort_yarns_by_brand(session: Session):
    return session.query(Yarn).order_by(Yarn.brand).all()

# Функция для создания таблицы с фильтрованными или отсортированными данными
def create_filtered_table(session: Session, table_name: str, yarns):
    session.execute(text(f"DROP TABLE IF EXISTS {table_name}"))
    session.execute(text(f"CREATE TABLE {table_name} (LIKE yarns INCLUDING ALL)"))

    # Вставка данных в новую таблицу
    for yarn in yarns:
        session.execute(
            text(f"INSERT INTO {table_name} (brand, name, country, color, quantity) VALUES (:brand, :name, :country, :color, :quantity)"),
            {
                'brand': yarn.brand,
                'name': yarn.name,
                'country': yarn.country,
                'color': yarn.color,
                'quantity': yarn.quantity
            }
        )
    session.commit()
    
    # Сброс ID в новой таблице
    reset_ids_in_new_table(session, table_name)
    print(f"Таблица {table_name} создана.")

def reset_ids_in_new_table(session: Session, table_name: str):
    # Сбросить ID в новой таблице
    session.execute(text(f"""
        WITH updated AS (
            SELECT *, ROW_NUMBER() OVER () as new_id
            FROM {table_name}
        )
        UPDATE {table_name}
        SET id = updated.new_id
        FROM updated
        WHERE {table_name}.id = updated.id
    """))
    session.commit()