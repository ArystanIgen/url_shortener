from fastapi import APIRouter

router = APIRouter()


@router.get('')
def health_check() -> None:   # pragma: no cover
    ...
