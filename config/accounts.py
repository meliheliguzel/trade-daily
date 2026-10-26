class AccountsConfig:

    GET_DATA_WARNING_MESSAGE: str = "Please fill in the required fields."

    ADD_SUCCESS_MESSAGE: str = "Account '{}' added successfully."
    UPDATE_SUCCESS_MESSAGE: str = "Account '{}' updated to '{}' successfully."

    REMOVE_MESSAGE_BOX_TITLE: str = "Delete Account"
    REMOVE_MESSAGE_BOX_TEXT: str = (
        "Are you sure you want to delete account '{}' and all its associated data?"
    )
    REMOVE_SUCCESS_MESSAGE: str = "Account '{}' deleted successfully."

    USER_CHANGE_SUCCESS_MESSAGE: str = "Active account changed: {}"

    INPUT_DURATION: int = 15
