# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : zhengdongqi
@Email   : dongqi.zheng@mxplayer.in
@Usage   :
@FileName: 04.operate_util.py
@DateTime: 2022/9/2 18:57
@SoftWare: PyCharm
"""

from cassandra.cluster import Cluster, SimpleStatement, ExecutionProfile, EXEC_PROFILE_DEFAULT
from cassandra.query import BatchStatement, ValueSequence, named_tuple_factory, dict_factory
from cassandra.policies import RoundRobinPolicy, DowngradingConsistencyRetryPolicy
from cassandra import ConsistencyLevel
from elasticsearch import Elasticsearch, RequestsHttpConnection, helpers
import traceback
import fire
import json
import time
import sys
import boto3
import logging
import MySQLdb


class OperateCA(object):
    def __init__(self, config):
        self.config = config
        self.cluster = self.get_cluster()
        self.session = self.get_session()

    def get_cluster(self, contact_points=[]):
        try:
            if not contact_points:
                contact_points = self.config['servers']
            return Cluster(contact_points=contact_points, connect_timeout=60)
        except BaseException as e:
            print(str(e))
            return None

    def get_session(self, keyspace=''):
        try:
            if not keyspace:
                return self.cluster.connect(self.config['db'])
            return self.cluster.connect(keyspace)
        except BaseException as e:
            print(str(e))
            return None

    # 直接执行sql语句 'SELECT * FROM video where id=\'20000dtl4u\' limit 1'
    def single_execute(self, cql):
        try:
            return self.session.execute(cql, timeout=60)
        except BaseException as e:
            print('Exception is %s. SQL is %s. Error is %s.' % (str(traceback.format_exc()), cql, str(e)))
            return None

    # 匹配sql语句与值
    def match_execute(self, cql, value_list):
        try:
            query = SimpleStatement(cql)
            data = self.session.execute(query, value_list, timeout=0.1)
            return data
        except BaseException as e:
            print('Exception is %s. CQL is %s. Values is %s. Error is %s.' % (
            str(traceback.format_exc()), json.dumps(cql), value_list, str(e)))
            return None

    # 批量执行list
    def batch_execute(self, cql, k, value_list):
        cql_stmt = self.session.prepare(cql)
        batch_query = BatchStatement(consistency_level=ConsistencyLevel.ANY)

        for item in value_list:
            batch_query.add(cql_stmt, (k, item[0], int(-item[1])))
        try:
            self.session.execute(batch_query)
        except BaseException as e:
            print('Exception is %s. Error is %s.' % (str(traceback.format_exc()), str(e)))

    # 批量执行map
    def batch_execute_map(self, cql, value_map):
        cql_stmt = self.session.prepare(cql)
        batch_query = BatchStatement(consistency_level=ConsistencyLevel.ANY)

        for k, v in value_map.items():
            if not k or not v:
                continue
            batch_query.add(cql_stmt, (k, v))

        try:
            self.session.execute(batch_query)
        except BaseException as e:
            print("Exception is %s. Error is %s" % (str(traceback.format_exc()), str(e)))

    # 执行携带返回值
    def return_execute_value(self, cql_list):
        result_list = list()
        issue = ""
        try:
            for cql in cql_list:
                issue = cql
                data = self.session.execute(cql, timeout=10)
                result_list.append(data)
            return result_list
        except BaseException as e:
            print("Exception is %s. CSQL is %s. Error is %s." % (
            str(traceback.format_exc()), json.dumps(issue), str(e)))
            return result_list

    # 执行不带返回值
    def execute_with_list(self, cql_list):
        issue = ""
        try:
            for cql in cql_list:
                issue = cql
                data = self.session.execute(cql, timeout=10)
            return "Success"
        except BaseException as e:
            print("Exception is %s. CQL is %s. Error is %s." % (str(traceback.format_exc()), json.dumps(issue), str(e)))
            return None

    def __del__(self):
        if self.cluster:
            self.cluster.shutdown()
        if self.session:
            self.session.shutdown()
        self.cluster = None
        self.session = None


class OperateES(object):
    def __init__(self, config):
        self.config = config
        self.conn = self.get_connection()

    def get_connection(self):
        try:
            return Elasticsearch(
                hosts=[
                    {
                        'host': self.config['host'],
                        'port': 9200
                    }
                ],
                connection_class=RequestsHttpConnection
            )
        except BaseException as e:
            print(str(e))
            return None

    def search_scroll(self, query, index=None, doc_type=None):
        try:
            if not index:
                index = self.config['index']
            return helpers.scan(
                self.conn,
                query=query,
                index=index,
                doc_type=doc_type,
                scroll=u'1m',
                size=100,
                clear_scroll=True
            )
        except BaseException as e:
            print(str(e))
            return None


class OperateFile(object):
    @staticmethod
    def read_data_from_file(file_path):
        fp = open(file_path, 'r+')
        print ('文件名为: ', fp.name)

        data_list = []
        try:
            while True:
                line = fp.readline()
                # print line
                line = line.strip('\r')
                line = line.strip('\n')
                if len(line) == 0:
                    break
                # data_list.add(int(line))
                data_list.append(line)
            return data_list
        except BaseException as e:
            print(str(e))
            return None
        finally:
            fp.close()
            print("count:" + str(len(data_list)))

    @staticmethod
    def write_data_to_file(file_path, content):
        fp = None
        try:
            fp = open(file_path, 'w+')
            print(fp.name)
            for i in content:
                fp.write(str(i) + '\n')
        except BaseException as e:
            print(str(e))
            return None
        finally:
            fp.close() if fp is not None else None


class OperateMysql:
    def __init__(self, config):
        self.config = config
        self.conn = self.get_connection()

    def get_connection(self):
        try:
            return MySQLdb.connect(
                self.config['host'],
                self.config['user'],
                self.config['passwd'],
                self.config['database'],
                self.config['port']
            )
        except BaseException as e:
            print(str(e))
            return None

    def query(self, sql):
        try:
            conn = self.conn
            cursor = conn.cursor()

            cursor.execute(sql)
            res = cursor.fetchall()

            cursor.close()
            return [self.to_dict(cursor, record) for record in res]
        except BaseException as e:
            print(str(e))
            return None

    def query_one(self, sql):
        try:
            res = self.query(sql)
            return res[0] if res else []
        except BaseException as e:
            print(str(e))
            return None

    @staticmethod
    def to_dict(cursor, record):
        try:
            params = [info[0] for info in cursor.description]
            return {params[i]: record[i] for i in xrange(len(record))}
        except BaseException as e:
            print(str(e))
            return None

    @staticmethod
    def create_sql_tables_to_file(file_path, sql):
        try:
            f = open(file_path, 'a')

            for i in range(0, 100):
                index = ''
                if i in range(10):
                    index = '0' + str(i)
                else:
                    index = str(i)
                s = sql % (index)
                f.write(s)
        except BaseException as e:
            print(str(e))
            return None
        finally:
            f.close()

    def __del__(self):
        if self.conn:
            self.conn.close()


class OperateSQS(object):
    @staticmethod
    def get_queue_for_sqs(queue_name):
        try:
            sqs = boto3.resource("sqs", region_name='ap-south-1')
            queue = sqs.get_queue_by_name(QueueName=queue_name)
        except BaseException as e:
            print(str(e))
            return None
        return queue

    @staticmethod
    def get_client_for_s3():
        try:
            boto3.set_stream_logger('botocore', logging.WARNING)
            s3 = boto3.resource("s3")
        except BaseException as e:
            print(str(e))
            return None
        return s3
