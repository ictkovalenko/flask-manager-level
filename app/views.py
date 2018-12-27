from flask import render_template


def page_not_found(e):
    context = dict()
    context['error'] = e
    return render_template('404.html', context=context), 404


def server_error(e):
    context = dict()
    context['error'] = e
    return render_template('500.html', context=context), 500


def method_not_allowed(e):
    context = dict()
    context['error'] = e
    return render_template('403.html', context=context), 403
