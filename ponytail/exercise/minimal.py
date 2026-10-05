"""Small implementation of the adapted upstream sql-user contract."""

def get_user(conn, username):
    if not isinstance(username, str):
        raise TypeError("username must be a string")
    if not 1 <= len(username) <= 64 or "\x00" in username:
        raise ValueError("username must contain 1..64 characters without NUL")
    row = conn.execute(
        "SELECT id, username, email FROM users WHERE username = ?", (username,)
    ).fetchone()
    return tuple(row) if row is not None else None
