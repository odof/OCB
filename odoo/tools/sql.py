# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

def existing_tables(cr, tablenames):
    """ Return the names of existing tables among ``tablenames``. """
    query = """
        SELECT c.relname
          FROM pg_class c
          JOIN pg_namespace n ON (n.oid = c.relnamespace)
         WHERE c.relname IN %s
           AND c.relkind IN ('r', 'v', 'm')
           AND n.nspname = current_schema
    """
    cr.execute(query, [tuple(tablenames)])
    return [row[0] for row in cr.fetchall()]

def table_exists(cr, tablename):
    """ Return whether the given table exists. """
    return len(existing_tables(cr, {tablename})) == 1

def drop_view_if_exists(cr, viewname):
    cr.execute("DROP view IF EXISTS %s CASCADE" % (viewname,))
    cr.commit()

def escape_psql(to_escape):
    return to_escape.replace('\\', r'\\').replace('%', '\%').replace('_', '\_')

def pg_varchar(size=0):
    """ Returns the VARCHAR declaration for the provided size:

    * If no size (or an empty or negative size is provided) return an
      'infinite' VARCHAR
    * Otherwise return a VARCHAR(n)

    :type int size: varchar size, optional
    :rtype: str
    """
    if size:
        if not isinstance(size, int):
            raise ValueError("VARCHAR parameter should be an int, got %s" % type(size))
        if size > 0:
            return 'VARCHAR(%d)' % size
    return 'VARCHAR'

def reverse_order(order):
    """ Reverse an ORDER BY clause """
    items = []
    for item in order.split(','):
        item = item.lower().split()
        direction = 'asc' if item[1:] == ['desc'] else 'desc'
        items.append('%s %s' % (item[0], direction))
    return ', '.join(items)
