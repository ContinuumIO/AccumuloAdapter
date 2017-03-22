#!/usr/bin/env python

import pyaccumulo
import logging
import sys


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(module)s] %(levelname)s: %(message)s')


def create_table(conn, name, start, stop):
    if conn.table_exists(name):
        conn.delete_table(name)
    logging.debug('Creating table "{}"...'.format(name))
    conn.create_table(name)

    writer = conn.create_batch_writer(name)
    logging.debug('Writing mutations...')
    for i in range(start, stop):
        if name == 'uints':
            value = '{0:06d}'.format(i)
        elif name == 'ints':
            value = '{0:06d}'.format(i)
        elif name == 'floats':
            value = '{0:07f}'.format(i + 0.5)
        elif name == 'strings':
            value = 'xxx' + str(i)
        elif name == 'missing_data':
            if i % 2 == 0:
                value = 'NA'
            elif i % 3 == 0:
                value = 'nan'
            else:
                value = '{0:06d}'.format(i)
        else:
            raise ValueError('invalid table name')
        m = pyaccumulo.Mutation('row{0:06d}'.format(i - start).encode('utf-8'))
        m.put(cf='f{0:06d}'.format(i - start).encode('utf-8'),
              cq='q{0:06d}'.format(i - start).encode('utf-8'),
              val=value.encode('utf-8'))
        #logging.debug('Adding Mutation(row={}, updates={})...'.format(m.row, [u.value for u in m.updates]))
        writer.add_mutation(m)
    writer.close()


def main():
    conn = pyaccumulo.Accumulo('0.0.0.0', port=42424, user='root', password='GisPwd')

    create_table(conn, 'uints', 0, 100000)
    create_table(conn, 'ints', -50000, 50000)
    create_table(conn, 'floats', -50000, 50000)
    create_table(conn, 'strings', 0, 100000)
    create_table(conn, 'missing_data', 0, 12)

    conn.close()


if __name__ == '__main__':
    sys.exit(main())
