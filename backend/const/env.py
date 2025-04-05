class DBEnv:
    user = "user"
    password = "password"
    host = "localhost"
    db_name = "gensin_db"
    db_pool_size = 10
    db_max_overflow = 40
    db_pool_recycle = 3600
    db_pool_pre_ping = True
    db_option = "charset=utf8mb4&collation=utf8mb4_general_ci"


# mysql+mysqlconnector://user:password@db_primary/manavis_db?charset=utf8mb4&collation=utf8mb4_general_ci
