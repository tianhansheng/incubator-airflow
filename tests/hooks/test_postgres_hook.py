# -*- coding: utf-8 -*-
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

import mock
import unittest

from airflow.hooks.postgres_hook import PostgresHook


class TestPostgresHook(unittest.TestCase):

    def setUp(self):
        super(TestPostgresHook, self).setUp()

        self.cur = mock.MagicMock()
        self.conn = conn = mock.MagicMock()
        self.conn.cursor.return_value = self.cur

        class UnitTestPostgresHook(PostgresHook):
            conn_name_attr = 'test_conn_id'

            def get_conn(self):
                return conn

        self.db_hook = UnitTestPostgresHook()

    def test_copy_expert(self):
        m = mock.mock_open(read_data='{"some": "json"}')
        with mock.patch('airflow.hooks.postgres_hook.open', m):
            statement = "SQL"
            filename = "filename"

            self.cur.fetchall.return_value = None

            self.assertEqual(None, self.db_hook.copy_expert(statement, filename, open=m))

            self.conn.close.assert_called_once()
            self.cur.close.assert_called_once()
            self.conn.commit.assert_called_once()
            self.cur.copy_expert.assert_called_once_with(statement, m.return_value)
            self.assertEqual(m.call_args[0], (filename, "r+"))
