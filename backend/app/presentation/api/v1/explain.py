from fastapi import APIRouter, Depends, HTTPException
from app.application.commands.explain_code_command import ExplainCodeCommand
from app.application.dto.explain_result_dto import ExplainResultDTO
from app.application.dispatch import CommandDispatcher
from app.presentation.api.v1.models import ExplainCodeRequest
from app.presentation.dependencies import get_command_dispatcher
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/explain", tags=["explain"])


@router.post("/", response_model=ExplainResultDTO)
async def explain_code(
    request: ExplainCodeRequest,
    dispatcher: CommandDispatcher = Depends(get_command_dispatcher),
) -> ExplainResultDTO:
    """
    Explain a code snippet using AI.

    Args:
        request: The code explanation request
        dispatcher: Command dispatcher dependency

    Returns:
        Explanation result with metadata
    """
    logger.info(f"Explaining code snippet of {len(request.code)} characters")

    command = ExplainCodeCommand(code=request.code, language=request.language)

    result = await dispatcher.dispatch(command)
    return result
