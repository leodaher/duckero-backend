from uuid import UUID


def is_valid_uuid(uuid):
    try:
        UUID(uuid)
    except ValueError:
        return False
    return True
