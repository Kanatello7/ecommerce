from fastapi import HTTPException

class ObjectNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Object not found")

class ObjectExistsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Object already exists")