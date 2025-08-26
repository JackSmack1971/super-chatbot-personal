import pytest

from scripts.check_code_quality import QualityCheckError, run_checks


@pytest.mark.asyncio
async def test_run_checks_success() -> None:
    await run_checks([["python", "-c", "print('ok')"]])


@pytest.mark.asyncio
async def test_run_checks_failure() -> None:
    with pytest.raises(QualityCheckError):
        await run_checks([["python", "-c", "import sys; sys.exit(1)"]])
