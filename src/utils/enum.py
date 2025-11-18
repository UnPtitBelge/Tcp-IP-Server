class Cmd:
    """Commands for the requests and responses"""

    PING = "0"
    LOGIN = "1"
    SEND_MESSAGE = "2"
    GET_DATA = "3"


class Login:
    """Parameters for a Login try"""

    # For server response
    DONE = "0"
    SIZE = "1"

    # Use by both client and server
    USER = "2"
    PWD = "3"
    NEW_CONN = "4"
