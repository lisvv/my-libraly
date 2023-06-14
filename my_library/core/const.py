class BookStatus:
    AVAILABLE = "В наличии"
    ON_READING = "На прочтении"
    RESERVED = "Зарезервирована"


class BookAction:
    LIST = "list"
    RETRIEVE = "retrieve"
    UPDATE = "update"
    PARTIAL = "partial_update"
    DELETE = "delete"
    CHANGE_STATUS = "change_book_status"
    UPLOAD = "upload_books"
