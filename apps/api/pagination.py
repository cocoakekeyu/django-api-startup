# -*- coding: utf-8 -*-
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.utils.urls import replace_query_param


class LinkHeaderPagination(PageNumberPagination):
    page_size_query_param = 'per_page'

    def get_paginated_response(self, data):
        rels = 'first prev next last'.split()
        urls = (getattr(self, 'get_{}_link'.format(rel))() for rel in rels)

        links = []
        for rel, url in zip(rels, urls):
            if url:
                links.append('<{1}>; rel={0},'.format(rel, url))
        else:
            links[-1] = links[-1][:-1]

        headers = {
            'Link': ''.join(links),
            'X-Total': self.page.paginator.count,
            'X-Per-Page': self.get_page_size(self.request),
        }

        return Response(data, headers=headers)

    def get_prev_link(self):
        return self.get_previous_link()

    def get_last_link(self):
        if not self.page.has_next():
            return None
        url = self.request.build_absolute_uri()
        page_number = list(self.page.paginator.page_range)[-1]
        return replace_query_param(url, self.page_query_param, page_number)

    def get_first_link(self):
        url = self.request.build_absolute_uri()
        page_number = 1
        return replace_query_param(url, self.page_query_param, page_number)
