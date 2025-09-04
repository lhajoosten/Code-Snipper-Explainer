from fastapi import APIRouter, Depends, HTTPException, Response
from app.application.commands.generate_tests_command import GenerateTestsCommand
from app.application.dto.test_scaffold_result_dto import TestScaffoldResultDTO
from app.application.dispatch import CommandDispatcher
from app.presentation.api.v1.models import GenerateTestsRequest
from app.presentation.dependencies import get_command_dispatcher
import logging
import hashlib

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/tests", tags=["tests"])


@router.post("/", response_model=TestScaffoldResultDTO)
async def generate_tests(
    request: GenerateTestsRequest,
    response: Response,
    dispatcher: CommandDispatcher = Depends(get_command_dispatcher),
) -> TestScaffoldResultDTO:
    """
    Generate unit test scaffold for a code snippet using AI.

    Args:
        request: The test generation request
        response: FastAPI response object for headers
        dispatcher: Command dispatcher dependency

    Returns:
        Test scaffold result with metadata
    """
    logger.info(f"Generating tests for code snippet of {len(request.code)} characters")

    command = GenerateTestsCommand(
        code=request.code,
        language=request.language,
        test_framework=request.test_framework,
    )

    result = await dispatcher.dispatch(command)

    # Add caching headers (test scaffolds are deterministic for same input)
    # Create ETag based on request content
    etag_content = (
        f"{request.code}{request.language or ''}{request.test_framework or ''}"
    )
    etag = hashlib.md5(etag_content.encode()).hexdigest()

    response.headers["ETag"] = f'"{etag}"'
    response.headers["Cache-Control"] = "public, max-age=1800"  # Cache for 30 minutes

    return result
