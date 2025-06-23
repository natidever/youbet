# from requests import session
# import pytest

# @pytest.mock.path('app.util.db_utils.get_db_record_or_404')
# async def test_resolve_ticket_service(mock_get_db_record_or_404):
#     mock_get_db_record_or_404.return_value = {"id": 1, "ticket_code": 12345}
#     # Call the service function
#     result = await resolve_ticket_service(session, ticket_code=12345, current_user=current_user)
#     assert result == {"id": 1, "ticket_code": 12345}