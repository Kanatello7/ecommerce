from fastapi import HTTPException, status


class CartNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")


class CartItemNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found"
        )


class ProductNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )


class ProductNotAvailableException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Product is not available"
        )


class InsufficientStockException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient stock for requested quantity",
        )


class InvalidQuantityException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantity must be greater than 0",
        )


class EmptyCartException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Cart is empty"
        )


class CartValidationException(HTTPException):
    def __init__(self, errors: list):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Cart validation failed", "errors": errors},
        )
