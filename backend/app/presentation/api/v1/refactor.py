from fastapi import APIRouter, Depends, HTTPException, Response
from app.application.commands.refactor_code_command import RefactorCodeCommand
from app.application.dto.refactor_result_dto import RefactorResultDTO
from app.application.dispatch import CommandDispatcher
from app.presentation.api.v1.models import RefactorCodeRequest
from app.presentation.dependencies import get_command_dispatcher
import logging
import hashlib

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/refactor", tags=["refactor"])


@router.post("/", response_model=RefactorResultDTO)
async def refactor_code(
    request: RefactorCodeRequest,
    response: Response,
    dispatcher: CommandDispatcher = Depends(get_command_dispatcher),
) -> RefactorResultDTO:
    """
    Suggest refactoring for a code snippet using AI.

    Args:
        request: The code refactoring request
        response: FastAPI response object for headers
        dispatcher: Command dispatcher dependency

    Returns:
        Refactoring result with metadata
    """
    logger.info(f"Refactoring code snippet of {len(request.code)} characters")

    command = RefactorCodeCommand(
        code=request.code, language=request.language, goal=request.goal
    )

    result = await dispatcher.dispatch(command)

    # Add caching headers (refactoring suggestions are deterministic for same input)
    # Create ETag based on request content
    etag_content = f"{request.code}{request.language or ''}{request.goal or ''}"
    etag = hashlib.md5(etag_content.encode()).hexdigest()

    response.headers["ETag"] = f'"{etag}"'
    response.headers["Cache-Control"] = "public, max-age=1800"  # Cache for 30 minutes

    return result
