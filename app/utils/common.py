def paginate_params(page: int = 1, page_size: int = 20) -> tuple[int, int]:
    page = max(page, 1)
    page_size = max(min(page_size, 100), 1)
    offset = (page - 1) * page_size
    return offset, page_size
