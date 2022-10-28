from logging import getLogger

from fastapi import APIRouter, Depends, Request, Response, status
from sqlalchemy.exc import DBAPIError, NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import UnmappedInstanceError

from ..database.database import get_db
from ..database.registrations import create, delete, update
from ..errors import InternalServerError, NotFoundError, TooManyRequestsError
from ..schemas.registration import Registration

log = getLogger(__name__)
registration_router = APIRouter(tags=["Registrations"], prefix="/registrations")


@registration_router.post(
    "",
    response_description="The created registration",
    response_model=Registration,
    responses={
        status.HTTP_429_TOO_MANY_REQUESTS: TooManyRequestsError.doc(),
        status.HTTP_500_INTERNAL_SERVER_ERROR: InternalServerError.doc(),
    },
    status_code=status.HTTP_201_CREATED,
)
async def add_registration(
    _: Request,
    registration: Registration,
    database: Session = Depends(get_db),
) -> Registration:
    """
    Create a new registration.
    """

    try:
        create(database, registration)
    except DBAPIError as err:
        raise InternalServerError(err) from err

    return registration


@registration_router.patch(
    "",
    response_description="The updated registration",
    responses={
        status.HTTP_404_NOT_FOUND: NotFoundError.doc(),
        status.HTTP_429_TOO_MANY_REQUESTS: TooManyRequestsError.doc(),
        status.HTTP_500_INTERNAL_SERVER_ERROR: InternalServerError.doc(),
    },
    response_model=Registration,
    status_code=status.HTTP_200_OK,
)
async def modify_registration(
    _: Request,
    registration: Registration,
    database: Session = Depends(get_db),
) -> Registration:
    """
    Update an existing registration.
    """

    try:
        updated = update(database, registration)
    except NoResultFound as err:
        raise NotFoundError(err) from err
    except Exception as err:
        raise InternalServerError(err) from err

    return Registration(
        client_id=updated.client_id,
        email=updated.email,
        organization=updated.organization,
    )


@registration_router.delete(
    "/{client_id}",
    responses={
        status.HTTP_404_NOT_FOUND: NotFoundError.doc(),
        status.HTTP_429_TOO_MANY_REQUESTS: TooManyRequestsError.doc(),
        status.HTTP_500_INTERNAL_SERVER_ERROR: InternalServerError.doc(),
    },
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_registration(
    _: Request,
    client_id: str,
    database: Session = Depends(get_db),
) -> Response:
    """
    Delete a registration.
    """

    try:
        delete(database, client_id)
    except UnmappedInstanceError as err:
        raise NotFoundError(err) from err
    except Exception as err:
        raise InternalServerError(err) from err

    return Response(status_code=status.HTTP_204_NO_CONTENT)
