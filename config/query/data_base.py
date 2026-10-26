class DataBaseQuery:
    BALANCE: str = """
    CREATE TABLE "Balance" (
	"id"	INTEGER NOT NULL UNIQUE,
	"size_id"	INTEGER NOT NULL,
	"transaction_id"	INTEGER NOT NULL,
	"value"	REAL NOT NULL,
	"estimated"	REAL NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("size_id") REFERENCES "Balance_Size"("id"),
	FOREIGN KEY("transaction_id") REFERENCES "Transaction"("id")
    )
    """

    BALANCE_SIZE: str = """
    CREATE TABLE "Balance_Size" (
	"id"	INTEGER NOT NULL UNIQUE,
	"size"	REAL NOT NULL,
	"state"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
    )
    """

    CHART_IMAGE: str = """
    CREATE TABLE "Chart_Image" (
	"id"	INTEGER NOT NULL UNIQUE,
	"transaction_id"	INTEGER NOT NULL,
	"image"	BLOB NOT NULL,
	"extension"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("transaction_id") REFERENCES "Transaction"("id")
    )
    """

    CHART_LINK: str = """
    CREATE TABLE "Chart_Link" (
	"id"	INTEGER NOT NULL UNIQUE,
	"transaction_id"	INTEGER NOT NULL,
	"link"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("transaction_id") REFERENCES "Transaction"("id")
    )
    """

    NOTE: str = """
    CREATE TABLE "Note" (
	"id"	INTEGER NOT NULL UNIQUE,
	"transaction_id"	INTEGER NOT NULL UNIQUE,
	"note_text"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("transaction_id") REFERENCES "Transaction"("id")
    )
    """

    PARITY: str = """
    CREATE TABLE "Parity" (
	"id"	INTEGER NOT NULL UNIQUE,
	"platform_id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	UNIQUE("platform_id","name"),
	FOREIGN KEY("platform_id") REFERENCES "Platform"("id")
    )
    """

    PLATFORM: str = """
    CREATE TABLE "Platform" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
    )
    """

    STRATEGY: str = """
    CREATE TABLE "Strategy" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT NOT NULL UNIQUE,
	"description"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
    )
    """

    TRANSACTION: str = """
    CREATE TABLE "Transaction" (
	"id"	INTEGER NOT NULL UNIQUE,
	"platform_id"	INTEGER NOT NULL,
	"parity_id"	INTEGER NOT NULL,
	"date_of_entry"	TEXT NOT NULL,
	"long_short"	INTEGER NOT NULL,
	"rr"	REAL NOT NULL,
	"size"	REAL NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("parity_id") REFERENCES "Parity"("id"),
	FOREIGN KEY("platform_id") REFERENCES "Platform"("id")
    )
    """

    TRANSACTION_CLOSING: str = """
    CREATE TABLE "Transaction_Closing" (
	"id"	INTEGER NOT NULL UNIQUE,
	"transaction_id"	INTEGER NOT NULL UNIQUE,
	"date_of_exit"	TEXT NOT NULL,
	"tp_sl"	INTEGER NOT NULL,
	"result"	REAL NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("transaction_id") REFERENCES "Transaction"("id")
    )
    """

    DETAIL_CLOSING: str = """
    CREATE TABLE "Transaction_Detail_Closing" (
	"id"	INTEGER NOT NULL UNIQUE,
	"transaction_id"	INTEGER NOT NULL UNIQUE,
	"exit_price"	REAL NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("transaction_id") REFERENCES "Transaction"("id")
    )
    """

    DETAIL_OPEN: str = """
    CREATE TABLE "Transaction_Detail_Open" (
	"id"	INTEGER NOT NULL UNIQUE,
	"transaction_id"	INTEGER NOT NULL UNIQUE,
	"enter_price"	REAL NOT NULL,
	"target_price"	REAL NOT NULL,
	"stop_price"	REAL NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("transaction_id") REFERENCES "Transaction"("id")
    )
    """

    TRANSACTION_STRATEGY: str = """
    CREATE TABLE "Transaction_Strategy" (
	"id"	INTEGER NOT NULL UNIQUE,
	"transaction_id"	INTEGER NOT NULL,
	"strategy_id"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	UNIQUE("strategy_id","transaction_id"),
	FOREIGN KEY("strategy_id") REFERENCES "Strategy"("id"),
	FOREIGN KEY("transaction_id") REFERENCES "Transaction"("id")
    )
    """

    TABLE_LIST: list[str] = [
        PLATFORM, PARITY, TRANSACTION, STRATEGY, TRANSACTION_STRATEGY,
        DETAIL_OPEN, DETAIL_CLOSING, TRANSACTION_CLOSING, NOTE,
        CHART_IMAGE, CHART_LINK, BALANCE_SIZE, BALANCE,
    ]
