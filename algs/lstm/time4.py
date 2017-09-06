import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd, zipfile
import tensorflow as tf
from tensorflow.contrib import rnn

mfile = "/home/burak/Downloads/scikit-data/time_series_classif"

# Parameters
learning_rate = 0.001
training_iters = 100000
batch_size = 25
display_step = 10

# Network Parameters
n_input = 1 
n_steps = 152 # timesteps
#n_hidden = 128 # hidden layer num of features
n_hidden = 40 # hidden layer num of features
n_classes = 2

with zipfile.ZipFile('wafer.zip', 'r') as z:
      df_train =  pd.read_csv(z.open('Wafer/wafer_TRAIN.txt'),header=None)
      df_test =  pd.read_csv(z.open('Wafer/wafer_TEST.txt'),header=None)

def minibatches(batch_size,input="train"):
      df = None
      if input=="train": df=df_train
      if input=="test": df=df_test
      df = np.array(df)
      for i in range(len(df)):
            batch_x = []; batch_y = []
            for j in range(batch_size):
                  batch_x.append(list(df[i,1:]))
                  batch_y.append([int(df[i,0]==-1), int(df[i,0]==1) ])
            batch_x = np.array(batch_x).reshape(batch_size,n_steps,1)
            batch_y = np.array(batch_y).reshape(batch_size,2)
            yield batch_x, batch_y
                  
# tf Graph input
x = tf.placeholder("float", [None, n_steps, n_input])
y = tf.placeholder("float", [None, n_classes])

# Define weights
weights = {
    'out': tf.Variable(tf.random_normal([n_hidden, n_classes]))
}
biases = {
    'out': tf.Variable(tf.random_normal([n_classes]))
}

def RNN(x, weights, biases):
    # Prepare data shape to match `rnn` function requirements
    # Unstack to get a list of 'n_steps' tensors of shape (batch_size, n_input)
    x = tf.unstack(x, n_steps, 1)

    # Define a lstm cell with tensorflow
    lstm_cell = rnn.BasicLSTMCell(n_hidden)

    # Get lstm cell output
    outputs, states = rnn.static_rnn(lstm_cell, x, dtype=tf.float32)

    # Linear activation, using rnn inner loop last output
    return tf.matmul(outputs[-1], weights['out']) + biases['out']

pred = RNN(x, weights, biases)

# Evaluate model
correct_pred = tf.equal(tf.argmax(pred,1), tf.argmax(y,1))
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))
new_pred = tf.argmax(y,1)

def train():

      print 'cost'
      cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=y))
      print 'optimizer'
      optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)
      
      # Initializing the variables
      init = tf.global_variables_initializer()
      saver = tf.train.Saver()
      with tf.Session() as sess:
          sess.run(init)
          step = 1
          # Keep training until reach max iterations
          b_it = minibatches(batch_size)
          while step < int(1000 / batch_size):
                batch_x, batch_y = next(b_it)
                print batch_x.shape
                # Run optimization op (backprop)
                sess.run(optimizer, feed_dict={x: batch_x, y: batch_y})
                if step % display_step == 0:
                      # Calculate batch accuracy
                      acc = sess.run(accuracy, feed_dict={x: batch_x, y: batch_y})
                      # Calculate batch loss
                      loss = sess.run(cost, feed_dict={x: batch_x, y: batch_y})
                      print("Iter " + str(step) + ", Minibatch Loss= " + \
                            "{:.6f}".format(loss) + ", Training Accuracy= " + \
                            "{:.5f}".format(acc))
                step += 1

          print("Optimization Finished!")
          saver.save(sess, mfile) # not shown in the book

def test():      
      saver = tf.train.Saver()
      from sklearn import metrics
      real = []
      pred = []
      with tf.Session() as sess:
          saver.restore(sess, mfile)
          for batch_x, batch_y in minibatches(1,input="test"):
            res = sess.run(new_pred, feed_dict={x: batch_x, y: batch_y})
            pred.append(res[0])
            real.append(np.argmax(batch_y[0]))
          fpr, tpr, thresholds = metrics.roc_curve(np.array(real), np.array(pred))
          print metrics.auc(fpr, tpr)
      
train()
test()
