import sqlite3
from domain.domain_item import FileDomainItem

create_file_table_sql = '''
CREATE TABLE IF NOT EXISTS file_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_path VARCHAR(1024),
    file_md5 CHAR(32) NOT NULL,
    file_name TEXT,
    file_type TEXT,
    file_size INTEGER,
    file_suffix TEXT,
    create_time TIMESTAMP,
    modify_time TIMESTAMP
)
'''
data_insert_sql = '''INSERT INTO file_info (file_path,file_md5,file_name,file_size,file_type,file_suffix,create_time,
modify_time) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}')'''
drop_sql = "DROP TABLE IF EXISTS file_info "
pic_query_sql = '''SELECT id,file_path FROM file_info WHERE file_type = 'pic' and file_md5 = 'tmp' LIMIT 20'''
conn = sqlite3.connect('./data/pandora.db')
cur = conn.cursor()


def add_file_info(file_domain_item: FileDomainItem):
    insert_sql = data_insert_sql.format(file_domain_item.file_path,
                                        file_domain_item.file_md5,
                                        file_domain_item.file_name,
                                        file_domain_item.file_size,
                                        file_domain_item.file_type,
                                        file_domain_item.file_suffix,
                                        file_domain_item.file_create_time,
                                        file_domain_item.file_modify_time)
    cur.execute(insert_sql)
    conn.commit()


def query_pic_list():
    cur.execute(pic_query_sql)
    return cur.fetchall()


def update_file_md5(id, md5):
    update_sql = '''UPDATE file_info SET file_md5 = '{}' WHERE id = '{}' '''.format(md5, id)
    cur.execute(update_sql)
    conn.commit()


def drop_db():
    cur.execute(drop_sql)
    conn.commit()


def init_db():
    cur.execute(create_file_table_sql)
    conn.commit()
