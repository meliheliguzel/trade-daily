class RecordConfig:

    UPDATE_DATA_LOAD_NOTICE_MESSAGE: str = "There is no process with this id value."

    LINK_REMOVE_SUCCES_MESSAGE: str = "Link deleted"
    LINK_REMOVE_WARNING_MESSAGE: str = "Select a link to delete"

    STRATEGY_REMOVE_SUCCES_MESSAGE: str = "Strategy deleted"
    STRATEGY_REMOVE_WARNING_MESSAGE: str = "Select a strategy to delete"

    IMAGE_REMOVE_SUCCES_MESSAGE: str = "The picture was deleted."
    IMAGE_REMOVE_WARNING_MESSAGE: str = "Select an image to delete"

    IMAGE_ADD_SUCCES_MESSAGE: str = "Picture added"
    IMAGE_ADD_WARNING_MESSAGE: str = "You haven't selected any images to add."
    IMAGE_ADD_TITLE: str = "Select the image or images you want to add"
    IMAGE_ADD_FILTER: str = "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"

    NEW: str = "new"
    CHANGE_BORDER_DURATION: int = 10

    STRATEGY_ADD_NOTICE_MESSAGE: str = "This strategy has already been added"

    TRANSACTION_ADD_SUCCES_MESSAGE: str = " transaction added to database."

    MISSING_AREA: str = "Fill in the fields marked in red."

    REMOVE_WARNING_TITLE: str = "You are about to delete a transaction record."
    REMOVE_WARNING_TEXT: str = "Do you want to delete transaction number "
    REMOVE_CANCEL_MESSAGE: str = "Delete transaction record canceled."
    REMOVE_SUCCES_MESSAGE: str = "Transaction record deleted"
    REMOVE_WARNING_MESSAGE: str = (
        "Transaction record number {} was not found in the database"
    )
    REMOVE_ERROR_MESSAGE: str = (
        "To delete any transaction record, you must first load that transaction record."
    )

    PLATFORM_NOT_FOUND_MESSAGE: str = "Platform '{}' not found in the list."
    PARITY_NOT_FOUND_MESSAGE: str = "Parity '{}' not found in the list."
