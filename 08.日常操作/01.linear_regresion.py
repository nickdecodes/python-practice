# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : zhengdongqi
@Email   : dongqi.zheng@mxplayer.in
@Usage   :
@FileName: 03.linear_regresion.py
@DateTime: 2022/9/2 17:55
@SoftWare: PyCharm
"""

import fire
import logging
import numpy as np

MODEL_FILE = 'model.txt'
DATA_FILE = 'model.csv'

# create logger
logger = logging.getLogger("model")
handler = logging.FileHandler("model.log")
formatter = logging.Formatter('%(asctime)s [%(levelname)s] <%(lineno)d> %(funcName)s: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class LinearRegression(object):
    def __init__(self, data_file, model_file):
        self.data_file = data_file
        self.model_file = model_file
        self.learning_rate = 0.01
        self.num_iterations = 1000
        self.w = 0
        self.b = 0

    # prepare the data set
    def gen_data(self, size, gen_w, gen_b, max_x, min_x, max_eps=0.01, min_eps=0.0):
        with open(self.data_file, 'w+') as f:
            for i in range(size):
                x = np.random.uniform(min_x, max_x)
                # mean=0, std=0.1
                eps = np.random.normal(min_eps, max_eps)
                y = gen_w * x + gen_b + eps
                f.write('{},{}\n'.format(x, y))

    # add data at data_file
    def add_data(self, data_list):
        with open(self.data_file, 'a+') as f:
            for point in data_list:
                logger.info('add_data is {},{}'.format(point[0], point[1]))
                f.write('{},{}\n'.format(point[0], point[1]))

    # clear data set
    def clear_data(self):
        with open(self.data_file, 'w+') as f:
            logger.info('clear data!')

    # y = wx + b
    def compute_loss(self, points):
        total_error = 0
        for i in range(0, len(points)):
            x = float(points[i, 0])
            y = float(points[i, 1])
            # computer mean-squared-error
            total_error += (y - (self.w * x + self.b)) ** 2
        # average loss for each point
        loss = total_error / float(len(points))
        return loss

    # compute the gradient
    def compute_gradient(self, points):
        b_gradient = 0
        w_gradient = 0
        N = float(len(points))
        for i in range(0, len(points)):
            x = float(points[i, 0])
            y = float(points[i, 1])
            # grad_b = 2(wx+b-y)
            b_gradient += (2 / N) * ((self.w * x + self.b) - y)
            # grad_w = 2(wx+b-y)*x
            w_gradient += (2 / N) * x * ((self.w * x + self.b) - y)
        # update w', b'
        self.b = self.b - (self.learning_rate * b_gradient)
        self.w = self.w - (self.learning_rate * w_gradient)

    # gradient descent
    def gradient_descent(self, points):
        # update for several times
        for i in range(self.num_iterations):
            self.compute_gradient(np.array(points))

    # save model to file
    def save_model(self):
        with open(self.model_file, 'w+') as f:
            f.write('{},{}\n'.format(self.w, self.b))
            logger.info('save model is {},{}\n'.format(self.w, self.b))

    # load model from file
    def load_model(self, model_file=None):
        model_file = self.model_file if not model_file else model_file
        with open(model_file, 'r+') as f:
            w, b = f.readline().split(',')
            self.w, self.b = float(w), float(b)
            logger.info('load model is {},{}\n'.format(self.w, self.b))

    # training model
    def train(self, learning_rate=None, num_iterations=None):
        if learning_rate:
            self.learning_rate = learning_rate
        if num_iterations:
            self.num_iterations = num_iterations

        points = np.genfromtxt(self.data_file, delimiter=",")
        logger.info(
            "Starting gradient descent at b = {}, w = {}, error = {}"
            .format(self.b, self.w, self.compute_loss(points))
        )
        logger.info("Running...")
        self.gradient_descent(points)
        logger.info(
            "After {} iterations b = {}, w = {}, error = {}"
            .format(self.num_iterations, self.b, self.w, self.compute_loss(points))
        )
        self.save_model()
        self.clear_data()

    # update model
    def update(self, data_list=None, learning_rate=None, num_iterations=None):
        if learning_rate:
            self.learning_rate = learning_rate
        if num_iterations:
            self.num_iterations = num_iterations

        self.load_model()
        if not data_list:
            self.train()
        else:
            points = np.array(data_list)
            logger.info(
                "Starting gradient descent at b = {}, w = {}, error = {}"
                .format(self.b, self.w, self.compute_loss(points))
            )
            logger.info("Running...")
            self.gradient_descent(points)
            logger.info(
                "After {} iterations b = {}, w = {}, error = {}"
                .format(self.num_iterations, self.b, self.w, self.compute_loss(points))
            )
            self.save_model()
            self.add_data(data_list)

    # predit result
    def predict(self, x=0):
        with open(self.model_file, 'r+') as f:
            w, b = f.readline().split(',')
            self.w, self.b = float(w), float(b)
        return (x * float(self.w) + float(self.b))

    # calculate x by y
    def calculate(self, y):
        return round((y - self.b) / float(self.w))


if __name__ == '__main__':
    # fire.Fire(Main)
    # task count for Per worker in a second
    lr = LinearRegression(DATA_FILE, MODEL_FILE)
    lr.gen_data(1000, 0.00277778, 0.1, 5.0, 5000.0)
    # lr.train(learning_rate=0.00000001, num_iterations=1000)
    while True:
        # for _ in range(6):
        #     y, x = (int(_) for _ in raw_input('input: ').split())
        #     lr.add_data([[y, x]])
        #     t = int(raw_input('predict: '))
        #     print('predict task:{} need worker:{}'.format(t, lr.predict(t) * 600 / 2))
        #     print('predict task:{} need machine:{}'.format(t, lr.predict(t) * 600 / 2))
        # lr.update(learning_rate=0.00000001, num_iterations=1000)
        t = int(raw_input('predict: '))
        print('predict task:{} per 1s need worker : {}'.format(t, lr.predict(t)))
        print('predict task:{} per 60min need worker : {}'.format(t, lr.predict(t) * 600))
        print('predict task:{} per 60min need machine : {}'.format(t, lr.predict(t) * 600 / 2))
        print(lr.calculate(lr.predict(t)))
