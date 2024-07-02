from drf_yasg import openapi

page = openapi.Parameter(
    "page",
    openapi.IN_QUERY,
    description="page number",
    type=openapi.IN_QUERY,
)
limit = openapi.Parameter(
    "limit", openapi.IN_QUERY, description="limit per page", type=openapi.IN_QUERY
)
search = openapi.Parameter(
    "search", openapi.IN_QUERY, description="search", type=openapi.IN_QUERY
)
user_status = openapi.Parameter(
    "user_status", openapi.IN_QUERY, description="user_status", type=openapi.IN_QUERY
)


page_length = openapi.Parameter(
    "page_length", openapi.IN_QUERY, description="Page Length", type=openapi.IN_QUERY
)

filter = openapi.Parameter(
    "filter", openapi.IN_QUERY, description="filter", type=openapi.IN_QUERY
)
start_date = openapi.Parameter(
    "start_date", openapi.IN_QUERY, description="Start Date", type=openapi.IN_QUERY
)
end_date = openapi.Parameter(
    "end_date", openapi.IN_QUERY, description="End Date", type=openapi.IN_QUERY
)

type = openapi.Parameter(
    "type", openapi.IN_QUERY, description="Type", type=openapi.IN_QUERY
)
id = openapi.Parameter("id", openapi.IN_QUERY, description="ID", type=openapi.IN_QUERY)
