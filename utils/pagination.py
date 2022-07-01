from django.core.paginator import Paginator


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


def make_pagination(request, query_set, per_page, range_size=4):

    try:
        current_page = int(request.GET.get('page', 1))
    except(ValueError):
        current_page = 1
    paginator = Paginator(query_set, per_page)
    page_obj = paginator.get_page(current_page)

    paginator_range = make_pagination_range(
        paginator.page_range,
        range_size,
        current_page
    )

    return page_obj, paginator_range
