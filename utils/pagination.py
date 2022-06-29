def make_pagination_range(page_range, qty_pages, current_page):

    total_pages = len(page_range)
    page_radius = (qty_pages//2)

    start_page = current_page - page_radius
    last_page = current_page + page_radius

    if start_page < 0:
        last_page += abs(start_page)
        start_page = 0

    if last_page > total_pages:
        start_page -= last_page - total_pages
    pagination = page_range[start_page:last_page]

    return {
        'pagination': pagination,
        'page_range': page_range,
        'qty_pages': qty_pages,
        'current_page': current_page,
        'total_pages': total_pages,
        'start_range': start_page,
        'stop_range': last_page,
        'first_page_out_of_range': current_page > page_radius,
        'last_page_out_of_range': last_page < total_pages
    }
