from fastapi import HTTPException, status
from enum import Enum


class EXCEPTIONS(Enum):

    class AUTHENTICATION(Enum):

        NOT_AUTHENTICATED = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to this request",
        )

        INVALID_CREDENTIALS = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid auth credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    class AUTHORIZATION(Enum):
        NOT_ENOUGH_PERMISSION = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to this information",
        )

    class TOOLING(Enum):
        NOT_FOUND = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tooling not founded",
        )
        NO_STATUS_DESCRIPTION_AVAILABLE = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot request a tooling, for this year after all CFs close",
        )
        REQUESTED_BY_OTHER_USER = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot update a tooling, you don't requested it",
        )
        INVALID_UPDATE = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot update this tooling",
        )

    class CLIENT(Enum):
        NOT_FOUND = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not Founded",
        )

    class CF(Enum):
        NOT_FOUND = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CF not founded",
        )
        NOT_FOUND_RELATED_BP = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CF not founded for this BP",
        )

    class BP(Enum):
        NOT_FOUND = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CF not Founded",
        )

    class PRODUCT_TYPE(Enum):
        NOT_FOUND = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CF not Founded",
        )
