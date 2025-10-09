import contextlib
from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture
def make_mock_get_db():
    def make(scalar_one_or_none=None, scalars_all=None, side_effect=None):
        mock_session = AsyncMock(spec=AsyncSession)
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = scalar_one_or_none
        mock_result.scalars.return_value.all.return_value = scalars_all
        mock_session.execute = AsyncMock(return_value=mock_result, side_effect=side_effect)

        @contextlib.asynccontextmanager
        async def get_db():
            yield mock_session

        return get_db, mock_session

    return make
